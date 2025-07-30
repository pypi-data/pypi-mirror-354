"""
Module to generate issue signed certificates.

This module defines the IssueCertficateGenerator class, which is responsible for generating
the data required for creating signed certificates.
"""

import json

import requests
from merkle_proof_gen import MerkleTreeGenerator


class IssueCertficateGenerator:
    """
    Class to generate issue signed certificate.

    Methods:
        generate_signed_cert_data: Generate the dictionary of data required for
        generating signed certificates.
        _create_base_template: Create the base template for signed certificate data.
    """

    def issue_certificate(self, signed_cert_data: dict, tx_hash: str):
        """
        This function is used to create merkle proof for each credential and
        update in each credentials in batch.

        Args:
            signed_cert_data (dict): Request param for signed cert data

        Return:
            Return list of signed credentials
        """
        # Generate Merkle proofusing tx_hash
        unsigned_list = signed_cert_data["unsigned_list"]
        chain = signed_cert_data["chain"]

        # Get DID of Issuer for w3c credential
        verification_method = signed_cert_data["issuer_did"]
        proof_generator = MerkleTreeGenerator().get_proof_generator(
            tx_id=tx_hash, chain=chain, verification_method=verification_method
        )

        # proof generator
        response_list = self.proof_generator(unsigned_list=unsigned_list)

        count = 0
        signed_json = []
        for unsigned, response_data in zip(unsigned_list, response_list):

            single_certificate_json = json.loads(unsigned)
            uuid = single_certificate_json["id"]

            # Add proof
            merkle_proof = next(proof_generator)
            single_certificate_json["proof"] = merkle_proof
            single_certificate_json["proof"]["proofValue"] = response_data[uuid]
            cert_json = json.dumps(single_certificate_json, ensure_ascii=False)
            signed_json.append(cert_json)
            count += 1

        return signed_json

    def proof_generator(self, unsigned_list):
        # proof generator api
        try:
            SERVICE_API_URL = "https://evrc-signing.everycred.com/sign-data"
            credList = {
                "data": unsigned_list,
            }

            # Headers of the api
            headers = {
                "Content-Type": "application/json",
            }

            response = requests.post(SERVICE_API_URL, json=credList, headers=headers)
        except Exception as exp:
            raise ValueError(str(exp)) from exp

        # Check the api is given successfull response
        if response["statusCode"] != 200:
            # Retrive data from the response of the api
            response_list = response["data"]
            if not response_list:
                raise ValueError(
                    "An error occurred while attempting to generate the proofValue."
                )
        return response_list
