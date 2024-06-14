#!/usr/bin/env python3
""" module Auth"""
from flask import request
import re
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """For now, this class is empty and inherits everything from Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
        header for Basic Authentication."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 part of the Authorization header."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user email and password from the Base64 decoded value.
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on the provided email and password.
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request."""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
