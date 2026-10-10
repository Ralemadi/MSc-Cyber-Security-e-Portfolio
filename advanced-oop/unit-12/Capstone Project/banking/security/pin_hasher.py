from __future__ import annotations
import hashlib
import hmac
import secrets

from banking.config import PBKDF2_ITERATIONS


#Encapsulate secure password hashing and verification.
class PinHasher:

    #Generate a random salt and derive the stored PBKDF2 password hash.
    @staticmethod
    def hash_pin(pin: str) -> tuple[str, str]:
        if not isinstance(pin, str) or not pin:
            raise ValueError("Password cannot be empty.")

        # Every customer receives an independent cryptographically random salt.
        salt = secrets.token_bytes(16)

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS,
        )

        return salt.hex(), digest.hex()

    #Derive and compare the supplied password hash using constant-time comparison.
    @staticmethod
    def verify_pin(
        pin: str,
        salt_hex: str,
        expected_hash_hex: str,
    ) -> bool:
        if not isinstance(pin, str):
            return False

        salt = bytes.fromhex(salt_hex)

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS,
        ).hex()

        # Constant-time comparison reduces timing side-channel leakage.
        return hmac.compare_digest(
            candidate,
            expected_hash_hex,
        )
