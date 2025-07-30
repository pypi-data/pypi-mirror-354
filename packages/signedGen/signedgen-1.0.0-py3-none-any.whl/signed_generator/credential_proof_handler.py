import json


class CredentialHandler:
    """
    Handle credential json and add transaction and merkle proof
    data in each credential.
    """

    def add_proof(self, merkle_proof: dict, single_certificate_json: dict):
        """
        This Method will add merkle proof generated after trasnaction
        into each json file of credential

        Args:
            merkle_proof (dict): Merkle proof after transaction.
            single_certificate_json (json): Signed certificate json file

        Return:
            Return signed credential
        """
        certificate_json = single_certificate_json
        certificate_json["signature"] = merkle_proof

        # Json content of issued certificate
        cert_json = json.dumps(certificate_json)

        return cert_json


class CredentialBatchHandler(object):
    """
    Manages a batch of certificates. Responsible for iterating certificates in a consistent order.

    In this case, certificates are initialized as an Ordered Dictionary,
     and we iterate in insertion order.
    """

    def __init__(self, certificate_handler, merkle_tree, unsigned_list):
        self.certificate_handler = certificate_handler
        self.merkle_tree = merkle_tree
        self.unsigned_list = unsigned_list

    def prepare_batch(self):
        """
        Propagates exception on failure

        Return:
            Return byte array to put on the blockchain
        """
        self.merkle_tree.populate(self.get_certificate_generator())
        return self.merkle_tree.get_blockchain_data()

    def get_certificate_generator(self):
        """
        Get array to issue of credential in the batch.

        Return:
            Returns a generator (1-time iterator)
        """
        count = 0
        unsigned_list = self.unsigned_list
        for _ in unsigned_list:
            single_certificate_json = json.loads(unsigned_list[count])
            data_to_issue = single_certificate_json
            count += 1
            yield data_to_issue

    def finish_batch(self, tx_id: str, chain):
        """
        Complete and add generated merkle proof in unsigned credential.

        Args:
            tx_id: Transaction id of the transaction.
            chain (str): Chain of credentiak,

        Return:
            Return signed credentials with merkle proof.
        """
        proof_generator = self.merkle_tree.get_proof_generator(tx_id, chain)

        count = 0
        signed_json = []
        for _, metadata in self.certificates_to_issue.items():
            single_certificate_json = json.loads(self.unsigned_list[count])

            proof = next(proof_generator)
            cert_json = self.certificate_handler.add_proof(
                metadata, proof, single_certificate_json
            )

            signed_json.append(cert_json)
            count += 1

        return signed_json
