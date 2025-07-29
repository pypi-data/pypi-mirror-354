# microdatabase

**microdatabase** is a lightweight SQLite toolkit with schema enforcement, row-level control, and Pythonic querying using lambda functions.

- Minimal and dependency-free
- Typed schema via `DatabaseParameter`
- Full row object access, with `.edit()` and `.delete()`
- Python-native query filtering (no SQL required)
- Stores files under a local `_databases/` directory

---

## Installation

```bash
pip install dbkit


````
from dbkit import Database, DatabaseParameter, DatabaseParameterType

db = Database("users", [
    DatabaseParameter("username", DatabaseParameterType.STRING),
    DatabaseParameter("age", DatabaseParameterType.INT),
    DatabaseParameter("active", DatabaseParameterType.BOOLEAN),
])

db.setup()

# Insert data
db.add_row(username="Karl", age=53, active=True)
db.add_row(username="Lilly", age=17, active=False)

# Query
adults = db.query(lambda r: r.age >= 18 and r.active)

for user in adults:
    print(user.username, user.age)

    # Edit a row
    user.edit(age=user.age + 1)

    # Delete a row
    if user.username == "Karl":
        user.delete()