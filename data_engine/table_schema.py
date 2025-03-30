from typing import List, Optional, Union
import pandas as pd
from column_schema import ColumnSchema


class TableSchema:
    """"
    A TableSchema defines the columns in a table. It is a construction of a collection of ColumnSchema objects.
    """
    def __init__(self, columns: Optional[List[ColumnSchema]] = None):
        self.columns = columns

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



# Example usage:
if __name__ == "__main__":
    # Create a table schema with some columns
    table_schema = TableSchema()
    table_schema.add_column(ColumnSchema("CustomerID", datatype="int"))
    table_schema.add_column(ColumnSchema("Name", datatype="string"))
    table_schema.add_column(ColumnSchema("Email", datatype="string", completeness=0.25))
    
    # Generate a DataFrame with 5 rows
    df = table_schema.generate(5)
    print(df)