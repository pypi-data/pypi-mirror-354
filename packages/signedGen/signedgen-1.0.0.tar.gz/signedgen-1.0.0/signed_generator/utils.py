"""
Utility functions for the unsigned_generator package.
"""

from datetime import datetime
from typing import Any

import pandas as pd
from cryptography.fernet import Fernet
from everycred.api.crypt import encrypt, get_wallet_credentials
from jsonpath_rw import Child, Fields, Root, par
from schema import Subject


class Utils:
    """
    A collection of utility methods for the unsigned_generator package.
    """

    @staticmethod
    def validate_validity(valid_from: str, valid_until: str):
        """Validate the validity period of credentials.

        This function checks if the provided validity period is valid or not.

        Args:
            valid_from (str): A string representing the starting date of the validity period.
            valid_until (str): A string representing the ending date of the validity period.

        Returns:
            Response or None: If the validity period is invalid (starting date is after the ending date),
                it returns a Response object with status code 400 and a message indicating the issue.
                If the validity period is valid or incomplete, it returns None.

        """

        # Validate validty period
        if valid_from and valid_until:
            from_date = Utils().convert_to_datetime(valid_from)
            until_date = Utils().convert_to_datetime(valid_until)

            if from_date and until_date:
                if from_date > until_date:
                    raise ValueError("Date is not valid!")
        else:
            return None

    @staticmethod
    def convert_to_datetime(datetime_str: str):
        if datetime_str == "None" or "":
            response = None
        else:
            try:
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
                response = datetime_obj
            except Exception as e:
                response = None
        return response

    @staticmethod
    def process_private_key(private_key: str):
        """
        Process the private key for certificate issuance.

        This function checks if the 'private_key' is present in the input 'body'. If it is not present, it retrieves the
        encrypted private key from the issuer's wallet based on the issuer's mode. If the 'private_key' is provided in the
        input 'body', it encrypts the user-submitted private key and updates the 'body' with the encrypted private key.

        Args:
            body (dict): The input request parameters.
            issuer (object): An object representing the issuer with relevant information.

        Returns:
            dict: The updated 'body' dictionary with the private key handling logic applied.
        """

        encrypted_key = Utils.encrypt_string(private_key)
        private_key = encrypted_key.decode()

        return private_key

    @staticmethod
    def encrypt_string(message: str):
        """Function to encrypt message or wallet private key

        Args:
            message (str): Message to encrypt
            wallet_type (str): Mode of wallet(ethereum_testnet, ethereum_mainnte, etc)

        Retrun:
            Encrypted message
        """
        # Read secret key
        CRYPT_SECRET_KEY = ""

        try:
            encoded_message = message.encode()
            fernet = Fernet(CRYPT_SECRET_KEY)
            return fernet.encrypt(encoded_message)
        except Exception as exp:
            raise ValueError(str(exp)) from exp
