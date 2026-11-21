CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

def parse_income(income):
    return int(income.replace(',', ''))

def monthly_emi(details):
    principal, rate, years = details.split(',')
    r = int(rate) / 1200
    n = int(years) * 12
    return round(int(principal) * r * (1 + r) ** n / ((1 + r) ** n - 1), 2)

def pan_category(pan):
    return CATEGORIES[pan[3].upper()]

def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result)

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result)

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result)

if __name__ == "__main__":
    main()
