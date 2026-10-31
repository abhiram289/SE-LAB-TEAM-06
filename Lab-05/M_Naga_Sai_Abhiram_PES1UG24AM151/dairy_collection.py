"""Dairy collection ledger with basic reporting and farmer utilities."""

import hashlib
import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE milk (
        id INTEGER PRIMARY KEY,
        farmer TEXT,
        litres REAL,
        fat REAL,
        day TEXT
    )
    """
)


def record_milk(db_conn, farmer, litres, fat, day):
    """Record a farmer's milk delivery."""
    db_conn.execute(
        """
        INSERT INTO milk (farmer, litres, fat, day)
        VALUES (?, ?, ?, ?)
        """,
        (farmer, litres, fat, day),
    )
    db_conn.commit()


def farmer_token(farmer):
    """Generate a SHA-256 digest for a farmer's name."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(db_conn, day):
    """Calculate the total litres collected on a given day."""
    rows = db_conn.execute(
        "SELECT litres FROM milk WHERE day = ?", (day,)
    ).fetchall()
    total = sum(row[0] for row in rows)
    return f"Total: {total:.1f} litres"


def top_farmer(db_conn):
    """Return the farmer with the greatest total milk delivery."""
    rows = db_conn.execute(
        """
        SELECT farmer, SUM(litres)
        FROM milk
        GROUP BY farmer
        """
    ).fetchall()

    if not rows:
        return None

    top_record = max(rows, key=lambda row: row[1])
    return top_record[0]


def print_slip(farmer):
    """Display a milk collection slip message."""
    print(f"Printing slip for {farmer}")


def low_fat(db_conn):
    """Return farmers whose recorded milk fat is below 3.5 or missing."""
    rows = db_conn.execute("SELECT farmer, fat FROM milk").fetchall()
    return [
        farmer
        for farmer, fat in rows
        if fat is None or fat < 3.5
    ]


def main():
    """Run a sample dairy collection demonstration."""
    record_milk(conn, "Gopal", 12.5, 4.1, "Mon")
    record_milk(conn, "Lata", 20.0, 3.2, "Mon")

    print(daily_total(conn, "Mon"), top_farmer(conn), low_fat(conn))
    print_slip("Gopal")
    print(farmer_token("Lata"))


if __name__ == "__main__":
    main()
