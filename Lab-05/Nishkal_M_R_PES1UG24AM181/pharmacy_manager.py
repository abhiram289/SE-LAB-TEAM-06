"""Small pharmacy stock and billing example for static analysis lab 5."""

from datetime import date, datetime
import hashlib
import hmac
import json
import math
import os
from pathlib import Path
import re
import secrets


medicines = {}


def _check_name(name):
    """Require a non-empty medicine name."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be non-empty text")


def _check_quantity(qty):
    """Require a positive whole-number quantity."""
    if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
        raise ValueError("Quantity must be a positive whole number")


def _parse_expiry(expiry):
    """Validate an ISO format expiry date."""
    if not isinstance(expiry, str):
        raise ValueError("Expiry must be a YYYY-MM-DD date")
    try:
        parsed = date.fromisoformat(expiry)
    except ValueError as error:
        raise ValueError("Expiry must be a YYYY-MM-DD date") from error
    if parsed.isoformat() != expiry:
        raise ValueError("Expiry must be a YYYY-MM-DD date")
    return parsed


def add_medicine(name, qty, price, expiry, audit=None):
    """Add stock after checking its name, quantity, price, and expiry."""
    _check_name(name)
    _check_quantity(qty)
    if (isinstance(price, bool) or not isinstance(price, (int, float))
            or not math.isfinite(price) or price < 0):
        raise ValueError("Price must be a non-negative number")
    _parse_expiry(expiry)
    if name in medicines:
        existing = medicines[name]
        if existing["price"] != price or existing["expiry"] != expiry:
            raise ValueError("Existing stock has a different price or expiry")
        existing["qty"] += qty
    else:
        medicines[name] = {"qty": qty, "price": price, "expiry": expiry}
    if audit is None:
        audit = []
    audit.append(
        f"{datetime.now().isoformat()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense available, unexpired stock or explain why it cannot be used."""
    _check_name(name)
    _check_quantity(qty)
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if is_expired(name):
        raise ValueError(f"Medicine has expired: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError(f"Insufficient stock: {name}")
    medicines[name]["qty"] -= qty
    if medicines[name]["qty"] == 0:
        del medicines[name]


def get_quantity(name):
    """Return the available quantity of a medicine."""
    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine's expiry date has passed."""
    return _parse_expiry(medicines[name]["expiry"]) < date.today()


def bill_amount(prescription):
    """Calculate a bill for available, unexpired prescription items."""
    total = 0.0
    requested = {}
    for name, qty in prescription:
        _check_quantity(qty)
        if is_expired(name):
            raise ValueError(f"Cannot bill expired medicine: {name}")
        requested[name] = requested.get(name, 0) + qty
        if requested[name] > get_quantity(name):
            raise ValueError(f"Insufficient stock: {name}")
        total += medicines[name]["price"] * qty
    return total


def calculate_dosage(formula):
    """Accept only a multiplication of two non-negative dosage numbers."""
    if not isinstance(formula, str):
        raise ValueError("Dosage must be text")
    match = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)\s*", formula
    )
    if match is None:
        raise ValueError("Dosage must be two non-negative numbers multiplied")
    result = float(match.group(1)) * float(match.group(2))
    if not math.isfinite(result):
        raise ValueError("Dosage is too large")
    return result


def patient_id(name, phone):
    """Make a repeatable identifier without using the weak MD5 hash."""
    return hashlib.sha256(f"{name}\0{phone}".encode()).hexdigest()


def generate_rx_number():
    """Generate a six-digit prescription number with secure randomness."""
    return f"RX-{100000 + secrets.randbelow(900000)}"


def save_stock(file="pharmacy.json"):
    """Save medicine records as JSON instead of executable pickle data."""
    with Path(file).open("w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=2)


def load_stock(file="pharmacy.json"):
    """Load and validate medicine records from JSON."""
    with Path(file).open("r", encoding="utf-8") as stock_file:
        loaded = json.load(stock_file)
    if not isinstance(loaded, dict):
        raise ValueError("Stock file must contain a medicine dictionary")
    checked = {}
    for name, record in loaded.items():
        _check_name(name)
        if (not isinstance(record, dict)
                or set(record) != {"qty", "price", "expiry"}):
            raise ValueError(f"Invalid stock record: {name}")
        _check_quantity(record["qty"])
        price = record["price"]
        if (isinstance(price, bool) or not isinstance(price, (int, float))
                or not math.isfinite(price) or price < 0):
            raise ValueError(f"Invalid price: {name}")
        _parse_expiry(record["expiry"])
        checked[name] = record
    medicines.clear()
    medicines.update(checked)


def print_label(name):
    """Print a label without passing medicine text to a shell."""
    print("Dispensing label:", name)


def expiring_soon(days=30):
    """List unexpired medicines that expire within the given number of days."""
    if isinstance(days, bool) or not isinstance(days, int) or days < 0:
        raise ValueError("Days must be a non-negative whole number")
    today = date.today()
    return [
        name for name, record in medicines.items()
        if 0 <= (_parse_expiry(record["expiry"]) - today).days <= days
    ]


def pharmacist_login(password):
    """Check a password supplied through the environment."""
    configured = os.getenv("PHARMACY_PASSWORD")
    return (
        isinstance(password, str)
        and bool(configured)
        and hmac.compare_digest(password, configured)
    )


def print_stock():
    """Print a short stock report."""
    print("===== Pharmacy Stock Report =====")
    for name, record in medicines.items():
        print(
            f"{name} -> {record['qty']} units, Rs. {record['price']} "
            f"exp {record['expiry']}"
        )


def main():
    """Run a short example and show rejected input clearly."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")
    for name, qty in [("Cetirizine 10mg", -10), (404, 25)]:
        try:
            add_medicine(name, qty, 2.0, "2027-03-31")
        except ValueError as error:
            print("Rejected stock:", error)
    dispense_medicine("Paracetamol 500mg", 30)
    try:
        dispense_medicine("Insulin", 2)
    except KeyError as error:
        print("Rejected dispensing:", error.args[0])
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 10),
                                ("Cetirizine 10mg", 5)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login configured:", bool(os.getenv("PHARMACY_PASSWORD")))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
