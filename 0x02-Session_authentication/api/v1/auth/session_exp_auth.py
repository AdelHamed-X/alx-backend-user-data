#!/usr/bin/env python3
""" module Auth"""

from flask import request
import re
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""
    user_id_by_session_id = {}
    session_duration = 0

    def __init__(self):
        """Constructor"""
        self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if 'created_at' not in session_dictionary:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        time_span = timedelta(seconds=self.session_duration)
        if (datetime.now() - created_at) > time_span:
            return None
        return session_dictionary.get('user_id')

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
