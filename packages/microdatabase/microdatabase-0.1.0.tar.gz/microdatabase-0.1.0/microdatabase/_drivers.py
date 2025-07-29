import os
import sqlite3


class Row:
    def __init__(self, db, rowid, **entries):
        self._db = db
        self._rowid = rowid
        self.__dict__.update(entries)

    def __getitem__(self, key):
        return self.__dict__[key]

    def edit(self, **new_values):
        keys = [param.key for param in self._db.parameters]
        updates = []
        values = []

        for key in keys:
            if key in new_values:
                val = new_values[key]
                updates.append(f"{key} = ?")
                values.append(int(val) if isinstance(val, bool) else val)

        if not updates:
            return  # nothing to change

        query = f"UPDATE data SET {', '.join(updates)} WHERE rowid = ?"
        values.append(self._rowid)

        conn = sqlite3.connect(self._db.db_path)
        conn.execute(query, values)
        conn.commit()
        conn.close()

        self.__dict__.update(new_values)

    def delete(self):
        query = "DELETE FROM data WHERE rowid = ?"
        conn = sqlite3.connect(self._db.db_path)
        conn.execute(query, (self._rowid,))
        conn.commit()
        conn.close()


def _setup_db(db):
    conn = sqlite3.connect(db.db_path)
    c = conn.cursor()

    columns = ", ".join(f"{p.key} {p.valueType.value}" for p in db.parameters)
    c.execute(f"CREATE TABLE IF NOT EXISTS data ({columns})")

    conn.commit()
    conn.close()


def _insert_row(db, values: dict):
    keys = [p.key for p in db.parameters]
    placeholders = ", ".join("?" for _ in keys)
    query = f"INSERT INTO data ({', '.join(keys)}) VALUES ({placeholders})"

    row_data = [int(values[k]) if isinstance(values[k], bool) else values[k] for k in keys]

    conn = sqlite3.connect(db.db_path)
    conn.execute(query, row_data)
    conn.commit()
    conn.close()


def _fetch_all_rows(db) -> list[Row]:
    conn = sqlite3.connect(db.db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM data")
    raw_rows = cursor.fetchall()
    conn.close()

    rows = []
    for row in raw_rows:
        row_dict = dict(row)
        rowid = row_dict.pop("rowid")
        rows.append(Row(db, rowid, **row_dict))
    return rows
