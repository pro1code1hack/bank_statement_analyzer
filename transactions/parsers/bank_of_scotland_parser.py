from datetime import datetime
from typing import List, Dict

from PyPDF2 import PdfReader

from transactions.parsers.base_parser import BaseParser
from transactions.transaction_service import Transaction


class BankOfScotlandParser(BaseParser):
    """
    Parser for Bank of Scotland bank statements.

    This parser extracts transaction data from Bank of Scotland PDF statements.
    """

    def __init__(self) -> None:
        """
        Initialize the BankOfScotlandParser.
        """
        self.transactions: List[Transaction] = []
        self.current_transaction: Dict[str, str] = {}

    def parse(self, file_path: str) -> List[Transaction]:
        """
        Parse the bank statement file.

        :param: file_path: The path to the bank statement file to be parsed.
        :returns: List[Transaction]: A list of transactions extracted from the bank statement.
        """
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            lines = text.split('\n')

            in_transactions_section = False

            for line in lines:
                if 'Your Transactions' in line:
                    in_transactions_section = True
                    continue

                if in_transactions_section:
                    self.process_line(line)

        return self.transactions

    def process_line(self, line: str) -> None:
        """
        Process a line from the bank statement.

        :param: line: A line of text from the bank statement.
        """
        if 'Date' in line:
            self.reset_current_transaction()
            return

        if self.current_transaction.get('date') is None:
            self.current_transaction['date'] = self.format_date(self.extract_value(line))
            return

        if self.current_transaction.get('description') is None:
            self.current_transaction['description'] = self.extract_value(line)
            return

        if self.current_transaction.get('type') is None:
            self.current_transaction['type'] = self.extract_value(line)
            return

        if self.current_transaction.get('money_in') is None:
            self.current_transaction['money_in'] = self.extract_money_value(line)
            return

        if self.current_transaction.get('money_out') is None:
            self.current_transaction['money_out'] = self.extract_money_value(line)
            return

        if self.current_transaction.get('balance') is None:
            self.current_transaction['balance'] = self.extract_money_value(line)
            self.add_transaction()

    def reset_current_transaction(self) -> None:
        """
        Reset the current transaction dictionary.
        """
        self.current_transaction = {
            'date': None,
            'description': None,
            'type': None,
            'money_in': None,
            'money_out': None,
            'balance': None
        }

    @staticmethod
    def extract_value(line: str) -> str:
        """
        Extract a value from a line of text.

        :param: line: A line of text.
        :returns: str: The extracted value.
        """
        return line.split('.')[0].strip()

    @staticmethod
    def extract_money_value(line: str) -> str:
        """
        Extract a money value from a line of text.

        :param: line: A line of text.
        :returns: str: The extracted money value.
        """
        parts = line.split('.')
        if parts[0].strip() == 'blank':
            return '0.0'
        return parts[0].strip() + '.' + parts[1].strip()

    @staticmethod
    def format_date(date_str: str) -> str:
        """
        Format a date string to YYYY-MM-DD format.

        :param: date_str: The date string to format.
        :returns: str: The formatted date string.
        """
        try:
            date_obj = datetime.strptime(date_str, "%d %b %y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return date_str

    def add_transaction(self) -> None:
        """
        Add the current transaction to the list of transactions.
        """
        transaction: Transaction = {
            "date": self.current_transaction['date'],
            "description": self.current_transaction['description'],
            "type": self.current_transaction['type'],
            "money_in": float(self.current_transaction['money_in'].replace(',', '')),
            "money_out": float(self.current_transaction['money_out'].replace(',', '')),
            "balance": float(self.current_transaction['balance'].replace(',', '')),
        }

        self.transactions.append(transaction)
