import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal


class Visualizer:
    """
    Class for visualizing transactions:
    1. Visualize expenses and incomes by category
    2. Visualize expenses vs incomes over time
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def visualize_by_category(self, transactions_df: pd.DataFrame, transactions_type: Literal["expenses", "incomes"]):
        """
        Generate a figure object and export it

        Group by the transaction type and apply sum
        Create a figure object of a pie chart with both percentages and numerical values

        The figure must be labeled with the most early date of transaction in the df to the latest and category report
        """
        start_date = transactions_df["date"].min().strftime('%Y-%m-%d')
        end_date = transactions_df["date"].max().strftime('%Y-%m-%d')

        if transactions_type == "incomes":
            balance_delta_column = "money_in"
            transactions_type_label = "Income"
        else:
            balance_delta_column = "money_out"
            transactions_type_label = "Expense"

        title = f"{start_date} - {end_date} {transactions_type_label} Summary by Category"

        transactions_by_category = transactions_df.groupby("category")[balance_delta_column].sum()

        # Function to display both percentage and actual value
        def autopct_format(values):
            def inner_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f'{pct:.1f}%\n(${val:,})'
            return inner_autopct

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 6))
        transactions_by_category.plot.pie(
            y=balance_delta_column,
            ax=ax,
            autopct=autopct_format(transactions_by_category),
            startangle=140,
            legend=False
        )
        ax.set_ylabel('')
        ax.set_title(title, pad=20)
        plt.tight_layout()

        self.__export_figure(fig, transactions_type_label)

    def visualize_income_vs_expense(self, transactions_df: pd.DataFrame):
        """
        Generate a figure object and export it
        Visualize monthly income vs expenses
        """
        transactions_df['month_year'] = transactions_df['date'].dt.to_period('M')
        monthly_summary = transactions_df.groupby('month_year').agg({'money_in': 'sum', 'money_out': 'sum'}).reset_index()

        # Creating the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_summary.plot(x='month_year', y=['money_in', 'money_out'], kind='bar', stacked=False, ax=ax)
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Monthly Income and Expenses')
        ax.legend(['Income', 'Expenses'])
        ax.grid(axis='y')
        plt.tight_layout()

        self.__export_figure(fig, 'monthly_income_expenses')

    def __export_figure(self, figure, file_name):
        file_path = os.path.join(self.output_dir, f"{file_name}.png")
        figure.savefig(file_path)

