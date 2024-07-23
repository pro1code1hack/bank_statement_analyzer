from datetime import datetime

from PyPDF2 import PdfReader

from transactions.parsers.base_parser import BaseParser


class BankOfScotlandParser(BaseParser):
    def __init__(self):
        self.transactions = []
        self.current_transaction = {}

    def parse(self, file_path):
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

    def process_line(self, line):
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

    def reset_current_transaction(self):
        self.current_transaction = {
            'date': None,
            'description': None,
            'type': None,
            'money_in': None,
            'money_out': None,
            'balance': None
        }

    @staticmethod
    def extract_value(line):
        return line.split('.')[0].strip()

    @staticmethod
    def extract_money_value(line):
        parts = line.split('.')
        if parts[0].strip() == 'blank':
            return '0.0'
        return parts[0].strip() + '.' + parts[1].strip()

    @staticmethod
    def format_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d %b %y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return date_str

    def add_transaction(self):
        transaction = {
            "date": self.current_transaction['date'],
            "description": self.current_transaction['description'],
            "type": self.current_transaction['type'],
            "money_in": float(self.current_transaction['money_in'].replace(',', '')),
            "money_out": float(self.current_transaction['money_out'].replace(',', '')),
            "balance": float(self.current_transaction['balance'].replace(',', '')),
        }

        self.transactions.append(transaction)
