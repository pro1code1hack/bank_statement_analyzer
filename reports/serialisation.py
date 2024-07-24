import os
from typing import Callable, Dict

import pandas as pd


class BaseSerialiser:
    """
    Base class for serializing data into different formats.
    """

    @staticmethod
    def serialise_csv(df: pd.DataFrame, output_path: str) -> None:
        """
        Serialise a DataFrame to CSV format.

        Args:
            df (pd.DataFrame): DataFrame to serialise.
            output_path (str): Path to save the CSV file.
        """
        df.to_csv(output_path, index=False)
        print(f"Data exported to {output_path} as CSV file.")

    @staticmethod
    def serialise_json(df: pd.DataFrame, output_path: str) -> None:
        """
        Serialise a DataFrame to JSON format.

        Args:
            df (pd.DataFrame): DataFrame to serialise.
            output_path (str): Path to save the JSON file.
        """
        df.to_json(output_path, orient="records", date_format="iso")
        print(f"Data exported to {output_path} as JSON file.")


class BankOfScotlandSerialiser(BaseSerialiser):
    """
    Serialiser class for Bank of Scotland data.
    """

    @staticmethod
    def serialise(expense_df: pd.DataFrame, income_df: pd.DataFrame, output_dir: str, export_format: str) -> None:
        """
        Serialise data based on the specified format.

        Args:
            expense_df (pd.DataFrame): DataFrame containing expense data.
            income_df (pd.DataFrame): DataFrame containing income data.
            output_dir (str): Directory to save the serialised files.
            export_format (str): Format to export the data ('csv' or 'json').
        """
        os.makedirs(output_dir, exist_ok=True)

        handlers: Dict[str, Callable[[pd.DataFrame, str], None]] = {
            "csv": BaseSerialiser.serialise_csv,
            "json": BaseSerialiser.serialise_json
        }

        if export_format in handlers:
            expense_output_path = os.path.join(output_dir, f"expenses.{export_format}")
            income_output_path = os.path.join(output_dir, f"incomes.{export_format}")

            handlers[export_format](expense_df, expense_output_path)
            handlers[export_format](income_df, income_output_path)
        else:
            print(f"Unsupported export format: {export_format}")
