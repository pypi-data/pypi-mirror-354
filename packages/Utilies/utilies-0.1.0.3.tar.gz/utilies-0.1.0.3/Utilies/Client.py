# -*- coding: utf-8 -*-
"""
Created on Mon May  19  2025

@author: Krishna Murthy S (krishnamurthy.s@hpe.com)
"""
import re

'''importing libraries'''
import os
from os.path import dirname
from os.path import join, exists, basename
from pathlib import Path

from O365 import FileSystemTokenBackend, Account


# Custom exception for authentication errors
class AuthenticationError(Exception):
    pass


# Client class to hold client details
class Client:
    def __init__(self, name, email_id, client_id, client_secret, token_file_path):
        self.NAME = name
        self.EMAIL_ID = email_id
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.TOKEN_PATH = token_file_path


# Authentication class handling token generation and authentication
class Auth:
    GRAPH_API_SCOPE = [
        'https://graph.microsoft.com/TeamsActivity.Send',
        'https://graph.microsoft.com/User.Read',
        'https://graph.microsoft.com/TeamsApp.Read',
        'https://graph.microsoft.com/TeamsApp.ReadWrite',
        'basic', 'mailbox', 'mailbox_shared', 'message_send',
        'message_send_shared', 'message_all', 'message_all_shared','users', 'onedrive',
        'onedrive_all', 'sharepoint'

    ]

    DEFAULT_TOKEN_NAME = 'o365_token_chandru.txt'

    def __init__(self, client):
        self.client = client

    def generate_token(self):
        """Generate or load a token for authentication."""
        token_backend = FileSystemTokenBackend(
            token_path=dirname(self.client.TOKEN_PATH),
            token_filename=basename(self.client.TOKEN_PATH)
        )
        account = Account(
            credentials=(self.client.CLIENT_ID, self.client.CLIENT_SECRET),
            token_backend=token_backend
        )

        # If token doesn't exist, authenticate and save it
        if not exists(self.client.TOKEN_PATH):
            if account.authenticate(scopes=self.GRAPH_API_SCOPE):
                save = join(str(Path(__file__).resolve().parent), self.DEFAULT_TOKEN_NAME)
                if exists(save):
                    os.rename(save, self.client.TOKEN_PATH)

        return account

def has_matches(pattern, text):
    """Check if the text matches the pattern, with wildcard support."""
    if "*" in pattern:
        result = re.search(pattern, text, re.IGNORECASE)
        return bool(result and result.group(0))
    else:
        return pattern == text
