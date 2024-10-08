from typing import List

from transactions.transaction_service import Transaction


class BaseParser:
    """
    Base class for parsing bank statement files.

    This class provides a blueprint for subclasses to implement specific parsing logic for different bank statements.
    """

    def parse(self, file_path: str) -> List[Transaction]:
        """
        Parse the bank statement file.

        This method should be implemented by subclasses to extract transaction data from the specified file.

        :param: file_path: The path to the bank statement file to be parsed.
        :returns: List[Transaction]: A list of dictionaries, each containing transaction data.
        :raise: NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError("Subclasses should implement this method")
