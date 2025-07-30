# Signed Generator

A Python package for generating and handling signed verifiable credentials with merkle proof generation capabilities.

## Installation

```bash
pip install -r requirements.txt
```

## Features

-   Generate and issue verifiable credentials
-   Create and verify credential proofs
-   Handle merkle proof generation
-   Sign verifiable credentials
-   Schema validation and management
-   Attribute handling for credentials

## Package Structure

```
signed_generator/
├── __init__.py
├── attribute.py
├── constants.py
├── credential_proof_handler.py
├── issue_certificate_gen.py
├── merkle_proof_gen.py
├── schema.py
├── sign_vc.py
├── signed_gen.py
├── utils.py
├── tests/
└── requirements.txt
```

## Core Components

### Credential Generation and Signing

-   `signed_gen.py`: Main module for generating signed credentials
-   `sign_vc.py`: Handles the signing process for verifiable credentials
-   `issue_certificate_gen.py`: Manages certificate generation and issuance

### Proof Generation and Handling

-   `merkle_proof_gen.py`: Generates merkle proofs for credentials
-   `credential_proof_handler.py`: Handles credential proof operations

### Supporting Modules

-   `schema.py`: Defines and validates credential schemas
-   `attribute.py`: Manages credential attributes
-   `utils.py`: Utility functions for the package
-   `constants.py`: Package-wide constants

## Usage Example

```python

from signed_generator import SignedCertGenerator, Issuer


issuer = Issuer(
    name="Test Issuer",
    website="https://issuer.example.com",
    email="issuer@example.com",
    did="did:example:123",
    profile_link="https://issuer.example.com/profile",
    revocation_list="https://issuer.example.com/revocation",
    crypto_address="123abc"
)

# Initialize the generator
generator = SignedCertGenerator()
unsigned_json = "[{}]"

signed_cert_data = generator.generate_signed_cert_templated_data(
    issuer=issuer,
    unsigned_json=unsigned_json,
    private_key="private_key",
    valid_from="valid_from",
    valid_until="valid_until",
)

# Create sign transaction hash
tx_hash = generator.generate_transaction(
    issuer=issuer,
    signed_cert_data=signed_cert_data,
    gasprice=gasprice,
    gaslimit=gaslimit,
    unsigned_json=unsigned_json
)

# Create and sign a credential
signed_json = generator.generate_signed_certificate(
    signed_cert_data=signed_cert_data, 
    tx_hash=tx_hash
)
print(signed_json)

```

## Requirements

See `requirements.txt` for package dependencies.

## Testing

The package includes a test suite in the `tests/` directory. To run the tests:

```bash
python -m pytest tests/
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Contact

[Add contact information here]
