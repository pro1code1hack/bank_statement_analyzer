import sqlite3
from sqlite3 import Error

accounts = [
    {
        "user_id": 1,
        "account_number": "1234567890",
        "iban": "DE89370400440532013000",
        "bic": "DEUTDEFF",
        "sort_code": "10020030",
        "balance": 5000.00
    },
    {
        "user_id": 2,
        "account_number": "0987654321",
        "iban": "GB33BUKB20201555555555",
        "bic": "BUKBGB22",
        "sort_code": "20205060",
        "balance": 1200.50
    },
    {
        "user_id": 3,
        "account_number": "1122334455",
        "iban": "FR7630006000011234567890189",
        "bic": "AGRIFRPP",
        "sort_code": "30001007",
        "balance": 750.75
    }
]