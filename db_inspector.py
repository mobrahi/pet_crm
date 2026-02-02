import streamlit as st
from sqlalchemy import create_engine, inspect

# Connect to SQLite database
engine = create_engine("sqlite:///./crm.db")
insp = inspect(engine)

def show_db_schema():
    st.title("📊 CRM Database Inspector")

    # List all tables
    tables = insp.get_table_names()
    st.sidebar.header("Tables")
    selected_table = st.sidebar.selectbox("Choose a table", tables)

    if selected_table:
        st.subheader(f"Table: {selected_table}")

        # Show columns
        columns = insp.get_columns(selected_table)
        st.write("### Columns")
        col_data = [
            {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default")
            }
            for col in columns
        ]
        st.table(col_data)

        # Show primary key
        pk = insp.get_pk_constraint(selected_table)
        st.write("**Primary Key:**", pk)

        # Show foreign keys
        fks = insp.get_foreign_keys(selected_table)
        st.write("**Foreign Keys:**", fks)

        # Show indexes
        indexes = insp.get_indexes(selected_table)
        st.write("**Indexes:**", indexes)

if __name__ == "__main__":
    show_db_schema()
