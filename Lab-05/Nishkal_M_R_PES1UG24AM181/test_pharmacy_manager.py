"""Behavior checks for the cleaned pharmacy example."""

from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pharmacy_manager as pharmacy


class PharmacyTests(unittest.TestCase):
    """Check the behavior that the original demo got wrong."""

    def setUp(self):
        pharmacy.medicines.clear()
        self.future = (date.today() + timedelta(days=60)).isoformat()
        self.past = (date.today() - timedelta(days=1)).isoformat()

    def test_invalid_stock_is_rejected_without_mutation(self):
        """Negative quantities and numeric names must not enter stock."""
        for name, qty in [("A", -1), (404, 1)]:
            with self.subTest(name=name, qty=qty):
                with self.assertRaises(ValueError):
                    pharmacy.add_medicine(name, qty, 2.0, self.future)
        self.assertEqual(pharmacy.medicines, {})

    def test_dispensing_missing_or_expired_stock_fails(self):
        """The program must report failed dispensing attempts."""
        with self.assertRaises(KeyError):
            pharmacy.dispense_medicine("Missing", 1)
        pharmacy.add_medicine("Expired", 2, 1.0, self.past)
        with self.assertRaises(ValueError):
            pharmacy.dispense_medicine("Expired", 1)
        self.assertEqual(pharmacy.get_quantity("Expired"), 2)

    def test_billing_checks_combined_quantity_and_expiry(self):
        """Repeated bill lines cannot exceed available quantity."""
        pharmacy.add_medicine("A", 3, 2.0, self.future)
        with self.assertRaises(ValueError):
            pharmacy.bill_amount([("A", 2), ("A", 2)])
        pharmacy.add_medicine("Expired", 1, 2.0, self.past)
        with self.assertRaises(ValueError):
            pharmacy.bill_amount([("Expired", 1)])

    def test_dosage_does_not_execute_code(self):
        """Only numeric multiplication is accepted."""
        self.assertEqual(pharmacy.calculate_dosage("250 * 2"), 500.0)
        with self.assertRaises(ValueError):
            pharmacy.calculate_dosage("__import__('os').getcwd()")

    def test_json_round_trip_and_validation(self):
        """Stock can be saved and loaded without pickle deserialization."""
        pharmacy.add_medicine("A", 3, 2.0, self.future)
        with TemporaryDirectory() as directory:
            path = Path(directory) / "stock.json"
            pharmacy.save_stock(path)
            pharmacy.medicines.clear()
            pharmacy.load_stock(path)
            self.assertEqual(pharmacy.get_quantity("A"), 3)
            path.write_text('{"A": {"qty": -1}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                pharmacy.load_stock(path)
            self.assertEqual(pharmacy.get_quantity("A"), 3)


if __name__ == "__main__":
    unittest.main()
