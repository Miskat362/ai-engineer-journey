import sqlite3


def create_database():
    with sqlite3.connect("company.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary INTEGER NOT NULL
            )
        """)

        # Delete old data to avoid duplicates
        cursor.execute("DELETE FROM employees")

        fake_employees = [
            ("Rafi", "Engineering", 75000),
            ("Anika", "Engineering", 82000),
            ("Siam", "HR", 50000),
            ("Nabila", "Marketing", 60000),
            ("Tanvir", "Engineering", 90000),
            ("Karim", "HR", 55000),
        ]

        cursor.executemany(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            fake_employees,
        )
        conn.commit()
    print("Database 'company.db' updated successfully!")


if __name__ == "__main__":
    create_database()
