import fitz 
import re
from typing import List, Dict

class MonzoBankParser():
    """
    Parser for Monzo bank statements.
    This parser extracts transaction data from Monzo PDF bank statements.
    """
    def __init__(self) -> None:
        """
        Initialize the MonzoParser.
        """
        self.transactions: List[Dict[str, str]] = []
        self.current_transaction: Dict[str, str] = {}

    def parse_pdf(self, file_path: str, start_line:str) -> str:
        """
        Parse the bank statement file.
        :param: 
            file_path: The path to the bank statement file to be parsed.
            start_line: Words from which the extraction will start.
        :returns: 
            string: A string of all text contains transactions extracted from the bank statement.
        """
        reader = fitz.open(file_path)
        all_text = ""
        for page_num in reader:
            page = page_num.get_text()
            lines = page.split("\n")
            text = " ".join(lines)
            all_text += text
        # Find the start index for slicing
        try:
            start_index = all_text.index(start_line)
        except ValueError:
            return "Not found a start line in the text"
        return all_text[start_index:]

    # Find all matches
    def extract_dates(self, text: str) -> List[str]:
        """
        Extract all the dates from the text of the bank statement.
        :param: 
            text: A string of all text contains transactions extracted from the bank statement.
        :returns: 
            List[Dates]: A list consists of date strings (one str per transaction).
        """
        regex_date_pattern = re.compile(r'(\d{2}/\d{2}/\d{4})\s')
        dates_list = regex_date_pattern.findall(text)
        return dates_list
    
    def extract_amounts_balances(self, text: str) -> List[str]:
        """
        Extract all the amounts and balances from the text of the bank statement.
        :param: 
            text: A string of all text contains transactions extracted from the bank statement.
            start_line: Words from which the extractioin starts.
        :returns: 
            List[Amounts & Balances]: A list consists of strings with amount and balance (one str per transaction).
        """
        regex_amount_balance_pattern = re.compile(r'-?\d{1,3}(?:,\d{3})*\.\d{2} -?\d{1,3}(?:,\d{3})*\.\d{2}\s')
        amounts_balances_list = regex_amount_balance_pattern.findall(text)
        return amounts_balances_list
    
    def add_transactions(self, date, description, amount, balance):
        amount_value = float(amount.replace(',', ''))
        balance_value = float(balance.replace(',', ''))

        if amount_value < 0:
            return {
                "date": date,
                "description": description,
                "money_out": abs(amount_value),
                "money_in": 0.00,
                "balance": balance_value
            }
        return {
            "date": date,
            "description": description,
            "money_out": 0.00,
            "money_in": abs(amount_value),
            "balance": balance_value
        }
    
    def extract_transactions(self, text:str, dates_list: list, amounts_list:list):
        text_list = text.split(" ")

        # Create copies of the lists to avoid modifying the originals
        dates_copy = dates_list[:]  
        amounts_copy = [amount.strip().split()[0] for amount in amounts_list]  
        balances_copy = [balance.strip().split()[-1] for balance in amounts_list]
  
        while dates_copy:
            # Get the first date and amount from the copies
            date = dates_copy.pop(0)
            amount = amounts_copy.pop(0).replace(',', '')
            balance = balances_copy.pop(0).replace(',', '')
            
            # Find the start index of the current date
            try:
                start_index = text_list.index(date)
            except ValueError:
                print(f"Date not found date: {date}")
                continue
            
            # Find the end index of the current amount
            try:
                end_index = text_list.index(amount, start_index)
            except ValueError:
                print(f"Amount not found amount: {amount}")
                continue

            # Extract the description
            if end_index > start_index:
                description = " ".join(text_list[start_index + 1:end_index]).strip()

                # Remove the processed text from the data
                text_list = text_list[:start_index] + text_list[end_index + 1:]

                # Add the transaction to the list
                transaction = self.add_transactions(date, description, amount, balance)
                self.transactions.append(transaction)
        return self.transactions
