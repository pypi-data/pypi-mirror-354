"""
Module to generate signed certificate data.

This module defines the signedCertGenerator class, which is responsible for generating
the data required for creating signed certificates.
"""

import json
from typing import Any, Dict, Optional

from credential_proof_handler import CredentialBatchHandler, CredentialHandler
from merkle_proof_gen import MerkleTreeGenerator
from issue_certificate_gen import IssueCertficateGenerator
from transactify.blockchain import (
    create_transaction,
    get_address_nonce,
    send_transaction,
    sign_transactions,
)
from signed_generator.schema import Issuer

from .utils import Utils


class SignedCertGenerator:
    """
    Class to generate signed certificate data.

    Methods:
        generate_signed_cert_data: Generate the dictionary of data required for
        generating signed certificates.
        _create_base_template: Create the base template for signed certificate data.
    """

    def generate_signed_cert_templated_data(
        self,
        issuer: Issuer,
        unsigned_json: str,
        private_key: str,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Dict[str, Any]:
        # TODO: Validate the date for valid form and valid until
        Utils.validate_validity(valid_from=valid_from, valid_until=valid_until)
        # TODO: Encryt private key
        private_key = Utils.encrypt_string(private_key)
        unsigned_json = json.loads(unsigned_json)
        # TODO: Generate base signed template
        signed_cert_data = self.generate_signed_cert_data(
            issuer=issuer, private_key=private_key, unsigned_json=unsigned_json
        )
        return signed_cert_data

    def generate_signed_cert_data(
        self,
        issuer: Issuer,
        private_key: str,
        unsigned_json: dict,
    ):
        """
        Generate data for a signed certificate.

        Args:
            unique_batch_id (str): Unique identifier for the certificate batch.
            issuer (Issuer): The issuer object representing the entity issuing the certificate.
            main_body (dict): The main body of data related to the certificate.
            unsigned_json (str): JSON data of the unsigned certificate.
            credential_type (IssuerProfileType): The type of credential (e.g., W3C or OpenBadge).
            filters (dict): Filters containing user-specific data.

        Returns:
            dict: A dictionary containing all the necessary data for generating signed certificates.
        """
        signed_cert_data = {
            "issuing_address": issuer.crypto_address,
            "chain": issuer.mode.name,
            "wallet_chain": issuer.mode.name,
            "private_key": private_key,
            "unsigned_json": unsigned_json,
            "issuer_did": issuer.did,
        }
        return signed_cert_data

    def generate_transaction(
        issuer: Issuer,
        signed_cert_data: dict,
        gasprice: int,
        gaslimit: int,
        unsigned_json: str,
    ):
        merkle_tree = MerkleTreeGenerator()
        certificate_handler = CredentialHandler()
        unsigned_list = json.loads(unsigned_json)

        blockchain_bytes = CredentialBatchHandler(
            certificate_handler=certificate_handler,
            merkle_tree=merkle_tree,
            unsigned_list=unsigned_list,
        ).prepare_batch()

        nonce = get_address_nonce(issuer.mode.name, signed_cert_data.issuing_address)
        metadata = {
            "chain": issuer.mode.name,
            "toaddress": signed_cert_data.issuing_address,
            "gasprice": gasprice,
            "gaslimit": gaslimit,
            "value": 1000000000000000000,
            "skey": signed_cert_data.private_key,
        }
        transaction = create_transaction(blockchain_bytes, metadata, nonce, 1)
        signed_tx = sign_transactions(
            transaction, signed_cert_data.private_key, issuer.mode.name
        )
        tx_hash = send_transaction(signed_tx, issuer.mode.name)
        return tx_hash

    def generate_signed_certificate(signed_cert_data: dict, tx_hash: str):
        signed_json = IssueCertficateGenerator().issue_certificate(
            signed_cert_data=signed_cert_data, tx_hash=tx_hash
        )

        return signed_json
