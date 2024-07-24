import sqlite3
from sqlite3 import Error

statements = [
   {
        "account_id": 1,
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "opening_balance": 5000.00,
        "closing_balance": 7500.00,
        "money_out": 500.00,
        "money_in": 3000.00
    },
    {
        "account_id": 2,
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "opening_balance": 1500.00,
        "closing_balance": 2500.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 3,
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "opening_balance": 2000.00,
        "closing_balance": 3000.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 1,
        "start_date": "2023-02-01",
        "end_date": "2023-02-28",
        "opening_balance": 7500.00,
        "closing_balance": 8000.00,
        "money_out": 500.00,
        "money_in": 1000.00
    },
    {
        "account_id": 2,
        "start_date": "2023-02-01",
        "end_date": "2023-02-28",
        "opening_balance": 2500.00,
        "closing_balance": 3500.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 3,
        "start_date": "2023-02-01",
        "end_date": "2023-02-28",
        "opening_balance": 3000.00,
        "closing_balance": 4000.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 1,
        "start_date": "2023-03-01",
        "end_date": "2023-03-31",
        "opening_balance": 8000.00,
        "closing_balance": 8500.00,
        "money_out": 500.00,
        "money_in": 1000.00
    },
    {
        "account_id": 2,
        "start_date": "2023-03-01",
        "end_date": "2023-03-31",
        "opening_balance": 3500.00,
        "closing_balance": 4500.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 3,
        "start_date": "2023-03-01",
        "end_date": "2023-03-31",
        "opening_balance": 4000.00,
        "closing_balance": 5000.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 1,
        "start_date": "2023-04-01",
        "end_date": "2023-04-30",
        "opening_balance": 8500.00,
        "closing_balance": 9000.00,
        "money_out": 500.00,
        "money_in": 1000.00
    },
    {
        "account_id": 2,
        "start_date": "2023-04-01",
        "end_date": "2023-04-30",
        "opening_balance": 4500.00,
        "closing_balance": 5500.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 3,
        "start_date": "2023-04-01",
        "end_date": "2023-04-30",
        "opening_balance": 5000.00,
        "closing_balance": 6000.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 1,
        "start_date": "2023-05-01",
        "end_date": "2023-05-31",
        "opening_balance": 9000.00,
        "closing_balance": 9500.00,
        "money_out": 500.00,
        "money_in": 1000.00
    },
    {
        "account_id": 2,
        "start_date": "2023-05-01",
        "end_date": "2023-05-31",
        "opening_balance": 5500.00,
        "closing_balance": 6500.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
    {
        "account_id": 3,
        "start_date": "2023-05-01",
        "end_date": "2023-05-31",
        "opening_balance": 6000.00,
        "closing_balance": 7000.00,
        "money_out": 500.00,
        "money_in": 1500.00
    },
]