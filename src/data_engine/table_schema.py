import os
import sys

# Dynamically add the 'src' folder to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, ".."))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from typing import List, Optional, Union
import pandas as pd
from data_engine.column_schema import ColumnSchema


class TableSchema:
    """"
    A TableSchema defines the columns in a table. It is a construction of a collection of ColumnSchema objects.
    """
    def __init__(self, columns: Optional[List[ColumnSchema]] = None):
        self.columns = columns

    def __str__(self):
        return f"TableSchema(columns={self.columns})"

    def generate(self, num_rows: int = 10) -> pd.DataFrame:
        """
        Generates a representation of the table with the specified number of rows.

        Args:
            num_rows (int): The number of rows to generate.

        Raises:
            ValueError: If no columns are defined in the table schema.
        """
        if self.columns is None:
            raise ValueError("No columns defined in the table schema.")

        col_names = [c.name for c in self.columns]
        count = 0
        data = []
        while count < num_rows:
            row = [c.generate() for c in self.columns]
            data.append(row)
            count += 1
        return pd.DataFrame(data, columns=col_names)
    
    def add_column(self, column: ColumnSchema | str) -> None:
        """
        Adds a new column to the table schema.
        """
        # If we only provide the column name, we need to create a new ColumnSchema object.
        if isinstance(column, str):
            column = ColumnSchema(name=column)

        # If the columns list is None, we need to initialize it.
        if self.columns is None:
            self.columns = []
        self.columns.append(column)

    def remove_column(self, column_name: str) -> None:
        """
        Removes a column from the table schema by its name.
        """
        if self.columns is not None:
            self.columns = [col for col in self.columns if col.name != column_name]

    def select_columns(self, column_names: List[str]) -> "TableSchema":
        """
        Selects a list of columns based on the provided names and returns a new TableSchema object.
        """
        if self.columns is None:
            cols = []
        cols = [col for col in self.columns if col.name in column_names]
        return TableSchema(cols)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "TableSchema":
        """
        Creates a TableSchema object from a DataFrame.
        """
        columns = []
        for _, r in df.iterrows():
            row = {k: (v if pd.notna(v) else None) for k, v in r.items()}
            col = ColumnSchema(
                name=row["name"],
                datatype=row["datatype"],
                length=row["length"],
                domain=row["domain"],
                max_value=row["max"],
                min_value=row["min"],
                completeness=row["completeness"]
            )
            columns.append(col)
        table_schema = cls(columns)
        return table_schema


# Example usage:
if __name__ == "__main__":
    print(sys.path)
    # Create a table schema with some columns
    print("Creating table schema...")
    table_schema = TableSchema()
    table_schema.add_column(ColumnSchema("CustomerID", datatype="int"))
    table_schema.add_column(ColumnSchema("Name", datatype="string"))
    table_schema.add_column(ColumnSchema("Email", datatype="string", completeness=0.25))
    table_schema.add_column(ColumnSchema("Age", datatype="int", min_value=18, max_value=65))
    table_schema.add_column(ColumnSchema("Country", datatype="category", categories=["USA", "Canada", "UK"]))
    
    # Generate a DataFrame with 5 rows
    df = table_schema.generate(5)
    print(df)

    config_df = pd.DataFrame({
        "name": ["ID",  "Name", "Email", "Age", "Country"],
        "datatype": ["Integer", "String", "String", "Integer", "Category"],
        "length": [None, None, None, None, None],
        "domain": [None, None, None, None, None],
        "max": [None, None, None, 65, None],
        "min": [None, None, None, 18, None],
        "completeness": [1, 1, 0.25, 1, 1],
    })

    table_schema = TableSchema.from_dataframe(config_df)
    print(table_schema)
    generated_df = table_schema.generate(5)
    print(generated_df)