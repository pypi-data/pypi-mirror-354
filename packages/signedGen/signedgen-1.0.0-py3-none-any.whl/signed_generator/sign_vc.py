import base64
import hashlib
import json

import merkletools
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def generate_keys():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    return (
        base64.b64encode(private_bytes).decode(),
        base64.b64encode(public_bytes).decode(),
    )


def sign_data(private_key_b64, data):
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
        base64.b64decode(private_key_b64)
    )
    signature = private_key.sign(data.encode())
    return base64.b64encode(signature).decode()


def verify_signature(public_key_b64, signature_b64, data):
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(
        base64.b64decode(public_key_b64)
    )
    try:
        public_key.verify(base64.b64decode(signature_b64), data.encode())
        return True
    except:
        return False


def create_merkle_proof(data_list):
    mt = merkletools.MerkleTools()
    mt.add_leaf([hashlib.sha256(d.encode()).hexdigest() for d in data_list], True)
    mt.make_tree()
    proof = mt.get_proof(0)
    return proof


def create_verifiable_credential(subject_did, public_key, holder_did, issuer_did):
    credential = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential"],
        "issuer": {"id": issuer_did, "issuerProfile": "https://"},
        "holder": {"id": holder_did, "holderProfile": "https://"},
        "credentialSubject": {
            "id": subject_did,
            "publicKey": [
                {
                    "id": f"{subject_did}#key1",
                    "type": "Ed25519VerificationKey2018",
                    "controller": subject_did,
                    "publicKeyBase58": public_key,
                }
            ],
            "name": "Ishita Reddy",
            "email": "ishita_reddy@example.com",
            "Certificate_Title": "Certificate of Achievement",
            "Date_Issued": "2023-11-21T12:09:00+05:30",
            "Issued_By": "Viitorcloud Technologies Pvt. Ltd.",
            "Award_Id": "VC-AWARD-Q1-002",
            "displayHtml": "<div>",
        },
    }

    private_key, _ = generate_keys()
    signature_value = sign_data(private_key, json.dumps(credential, sort_keys=True))
    merkle_proof = create_merkle_proof([signature_value])

    credential["proof"] = {
        "type": "Ed25519Signature2018",
        "created": "2023-11-21T12:09:00+05:30",
        "verificationMethod": f"{subject_did}#key1",
        "signatureValue": signature_value,
        "merkleProof": merkle_proof,
    }

    return credential


subject_did = "did:evrc:subject:uuid-DID"
private_key, public_key = generate_keys()
holder_did = "did:evrc:holder:uuid-DID"
issuer_did = "did:evrc:issuer:network-type:uuid-DID"

verifiable_credential = create_verifiable_credential(
    subject_did, public_key, holder_did, issuer_did
)
print(json.dumps(verifiable_credential, indent=2))
