from pathlib import Path

# Application paths
BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = BASE_DIR / "db" / "banksecure.db"
DEFAULT_AUDIT_PATH = BASE_DIR / "audit" / "audit.jsonl"

# Public identifier formats
ACCOUNT_PREFIX = "QTR"
ACCOUNT_ID_DIGITS = 8
TRANSACTION_PREFIX = "TXN"
TRANSACTION_ID_DIGITS = 8

# Authentication and password security
PBKDF2_ITERATIONS = 200_000
PASSWORD_MIN_LENGTH = 9
PASSWORD_MAX_LENGTH = 128
MAX_FAILED_LOGIN_ATTEMPTS = 5
TEMPORARY_LOCKOUT_MINUTES = 5

# Banking configuration
ALLOWED_ACCOUNT_TYPES = (
    "CURRENT",
    "SAVINGS",
    "SALARY",
)

# A single transfer above 5,000.00 is rejected by the local risk strategy.
DEFAULT_TRANSFER_REVIEW_LIMIT_CENTS = 500_000

# The daily limit is a business policy and is separate from fraud scoring.
DEFAULT_DAILY_TRANSFER_LIMIT_CENTS = 1_000_000
