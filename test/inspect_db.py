from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///./crm.db")
insp = inspect(engine)

for table in insp.get_table_names():
    print(f"\n=== {table} ===")
    for col in insp.get_columns(table):
        print(f"{col['name']} - {col['type']} - nullable={col['nullable']} - default={col.get('default')}")
    print("PK:", insp.get_pk_constraint(table))
    print("FKs:", insp.get_foreign_keys(table))
    print("Indexes:", insp.get_indexes(table))
