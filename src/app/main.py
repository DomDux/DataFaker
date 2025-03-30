import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os
import sys

# Ensure the 'src' directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
print(src_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from data_engine.table_schema import TableSchema
from data_engine.column_schema import ColumnSchema 
from data_engine.datatypes import Datatype


st.set_page_config(
    page_title="Data Faker",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Data Faker")
st.write("Generate synthetic data for your applications.")

# Define possible datatypes
DATATYPES = list(Datatype._registry.keys())

def config_from_dataframe(df, table_name: str = "default"):
    """
    Function to configure the grid options from a dataframe.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, groupable=True, value=True, enableRowGroup=True, enablePivot=True)
    gb.configure_column("datatype", editable=True, cellEditor="agSelectCellEditor", cellEditorParams={"values": DATATYPES})
    gb.configure_column("name", editable=True, cellEditor="agTextCellEditor")
    gb.configure_column("length", editable=True, cellEditor="agNumberCellEditor")
    gb.configure_column("domain", editable=True, cellEditor="agTextCellEditor")
    gb.configure_column("max", editable=True, cellEditor="agNumberCellEditor")
    gb.configure_column("min", editable=True, cellEditor="agNumberCellEditor")
    gb.configure_column("completeness", editable=True, cellEditor="agNumberCellEditor")

    gb.configure_auto_height(True)
    
    # Show the table in AgGrid
    response = AgGrid(
        df,
        gridOptions=gb.build(),
        editable=True,
        fit_columns_on_grid_load=True,
        gridheight=None,
        reload_data=True
    )
    st.session_state.tables_grid[table_name] = response

    schema = {
        "name": pd.StringDtype(),
        "datatype": pd.StringDtype(),
        "length": pd.Int64Dtype(),
        "domain": pd.StringDtype(),
        "max": pd.Int64Dtype(),
        "min": pd.Int64Dtype(),
        "completeness": pd.Float64Dtype(),
    }

    # Get the updated data from the table
    updated_df = pd.DataFrame(response['data']).astype(schema)

    return updated_df


def update_function(table_name: str = "default") -> callable:
    """
    Function searches the session state for the table name and returns a function which updates the table schema.
    """
    if table_name not in st.session_state.tables:
        st.session_state.tables[table_name] = pd.DataFrame({
            "name": ["ID"],
            "datatype": ["Integer"],
            "length": [None],
            "domain": [None],
            "max": [None],
            "min": [None],
            "completeness": [1],
        })
    
    def update_table_schema() -> pd.DataFrame:
        """
        Function to update the table schema in the session state.
        """
        updated_df = config_from_dataframe(st.session_state.tables[table_name])
        st.session_state.tables[table_name] = updated_df
        return updated_df
    update_table_schema.__name__ = table_name
    return update_table_schema

def add_row(table_name: str) -> None:
    """
    Function to add a new row to the table configured in the session state.
    
    This function can be tied to a widget to add a new row to the table.
    """
    if table_name not in st.session_state.tables:
        raise ValueError(f"Table {table_name} not found in session state.")
    
    new_row = pd.DataFrame({
        "name": ["New Column"],
        "datatype": ["String"],
        "length": [None],
        "domain": [None],
        "max": [None],
        "min": [None],
        "completeness": [None],
    })
    st.session_state.tables[table_name] = pd.concat([st.session_state.tables[table_name], new_row], ignore_index=True)

@st.cache_data
def get_initial_table():
    return pd.DataFrame({
        "name": ["ID"],
        "datatype": ["Integer"],
        "length": [None],
        "domain": [None],
        "max": [None],
        "min": [None],
        "completeness": [1],
    })

# Create a cache of tables if none exists
if "tables" not in st.session_state:
    st.session_state.tables = {"default": get_initial_table()}
if "tables_grid" not in st.session_state:
    st.session_state.tables_grid = {}


def table_section(table_name: str) -> None:
    """"
    Function to create a section in the Streamlit app for each table.
    """
    with st.expander(f"Table: `{table_name}`", expanded=False):
        st.button("Add Row", key=f"add_row_{table_name}", on_click=add_row, args=(table_name,))

        update_table_schema = update_function(table_name)
        updated_df = update_table_schema()

        # # Button to display the final dataframe
        # if st.button(f"Update Table: {table_name}", key=f"update_{table_name}"):
        #     st.session_state[f"update{table_name}"] = True

        # if st.session_state.get(f"update{table_name}", False):
        #     st.write("Updated Table:")
        #     st.write(updated_df)
        #     st.session_state[f"update{table_name}"] = False

        if st.button(f"Generate Data for {table_name}", key=f"generate_{table_name}"):
            table_schema = TableSchema.from_dataframe(updated_df)
            df = table_schema.generate()
            st.write("Generated Data:")
            st.write(df)
            
# -------- Streamlit app layout --------
# # Create a text input widget for the user to enter a table name
new_table_name = st.text_input("Enter a new table name:", key="new_table_name")

# Create a button to trigger the update_function with the entered table name
if st.button("Add Table"):
    if new_table_name.strip():  # Ensure the input is not empty
        if new_table_name in st.session_state.tables:
            st.warning(f"Table '{new_table_name}' already exists!")
        else:
            update_function(new_table_name)  # Call the update_function with the input
            st.success(f"Table '{new_table_name}' added successfully!")
    else:
        st.error("Please enter a valid table name.")
for table_name in st.session_state.tables.keys():
    table_section(table_name)
    st.write("---")