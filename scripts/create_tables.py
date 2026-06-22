import sqlite3

conn = sqlite3.connect(
    "data/nifty100.db"
)

with open(
    "db/schema.sql",
    "r"
) as file:

    schema = file.read()

conn.executescript(schema)

print(
    "All tables created successfully"
)

conn.commit()
conn.close()