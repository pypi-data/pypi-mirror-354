import hashlib
import json
import logging
from datetime import datetime

from merkletools import MerkleTools
from pycoin.serialize import h2b


class MerkleTreeGenerator(object):
    """
    A class representing a Merkel Tree.
    """

    def __init__(self):
        self.tree = MerkleTools(hash_type="sha256")

    def hash_byte_array(data):
        """This function is used to convert data of credential into hash.

        Args:
            data (str): Data of the credential

        Return:
            Return hash of the credential
        """
        data_info = json.dumps(data, separators=(",", ":")).encode("utf-8")
        hashed = hashlib.sha256(data_info).hexdigest()
        return hashed

    def ensure_string(value):
        """This function is used to ensure merkle tree id

        Args:
            value (str): Merkle tree convert string

        Return:
            Return decoded string
        """
        if isinstance(value, str):
            return value
        return value.decode("utf-8")

    def populate(self, node_generator):
        """
        Populate Merkle Tree with data from node_generator.
        This requires that node_generator yield byte[] elements.
        Hashes, computes hex digest, and adds it to the Merkle Tree
        :param node_generator:
        :return:
        """
        for data in node_generator:
            hashed = self.hash_byte_array(data)
            self.tree.add_leaf(hashed)

    def get_blockchain_data(self):
        """
        Finalize tree and return byte array to issue on blockchain
        :return:
        """
        self.tree.make_tree()
        merkle_root = self.tree.get_merkle_root()
        return h2b(self.ensure_string(merkle_root))

    def tx_to_blink(self, chain, tx_id):
        """
        Convert a transaction ID to a BLINK ID based on the blockchain network.

        Args:
            chain (str): The blockchain network name.
                Possible values: "ethereum_ropsten", "ethereum_mainnet",
                "ethereum_sepolia", "polygon_mainnet", "polygon_testnet",
                "evrc_testnet".
            tx_id (str): The transaction ID.

        Returns:
            str: The BLINK ID corresponding to the given transaction ID and blockchain network.
        """
        blink = "blink:"
        if chain == "ethereum_ropsten":
            blink += "eth:ropsten:"
        elif chain == "ethereum_mainnet":
            blink += "eth:mainnet:"
        elif chain == "ethereum_sepolia":
            blink += "eth:sepolia:"
        elif chain == "polygon_mainnet":
            blink += "poly:mainnet:"
        elif chain == "polygon_testnet":
            blink += "poly:testnet:"
        elif chain == "evrc_testnet":
            blink += "evrc:testnet:"
        elif chain == "polygon_amoy":
            blink += "poly:amoy:"

        return blink + tx_id

    def get_proof_generator(
        self, tx_id, chain, verification_method
    ):
        """
        Returns a generator (1-time iterator) of proofs in insertion order.

        :param tx_id: blockchain transaction id
        :return:
        """
        root = self.ensure_string(self.tree.get_merkle_root())
        node_count = len(self.tree.leaves)
        for index in range(0, node_count):
            proof = self.tree.get_proof(index)
            proof2 = []

            for p in proof:
                dict2 = dict()
                for key, value in p.items():
                    dict2[key] = self.ensure_string(value)
                proof2.append(dict2)
            target_hash = self.ensure_string(self.tree.get_leaf(index))

            # Merkle json for json file
            merkle_json = {
                "type": "MerkleProof2019",
                "path": proof2,
                "merkleRoot": root,
                "targetHash": target_hash,
                "anchors": [self.tx_to_blink(chain, tx_id)],
            }

            # Merkle proof value
            logging.info("merkle_json: %s", str(merkle_json))

            CRED_TYPE = ""
            PROOF_ALGORITHM = "Ed25519Signature2020"
            ED25519_SIGNATURE_PUBLIC_KEY = (
                "qripMkR2QeI1Iqf44H4JR+eCIEhe5stidmg4F7cO2MI="
            )
            merkle_proof = {
                "type": CRED_TYPE,
                "cryptosuite": PROOF_ALGORITHM,
                "created": datetime.now().isoformat(),
                "proofPurpose": "assertionMethod",
                "verificationMethod": f"{verification_method}#{ED25519_SIGNATURE_PUBLIC_KEY}",
                "merkleProof": merkle_json,
            }

            yield merkle_proof
