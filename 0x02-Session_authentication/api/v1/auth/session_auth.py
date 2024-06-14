#!/usr/bin/env python3
""" module Auth"""

from flask import request
import re
import os
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

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

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
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
