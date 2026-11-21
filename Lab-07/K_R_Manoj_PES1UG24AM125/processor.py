"""Coffee Shop Order Processor - Hardened Implementation.
Student Name: K R Manoj
SRN: PES1UG24AM125
Course: Software Engineering (5th Sem) - Lab 7
"""


def lookup_drink_code(code_string):
    """Look up drink base price by its 3-letter menu prefix.

    Defensive against None, non-string, whitespace, unknown codes, and casing.
    """
    if not isinstance(code_string, str) or not code_string.strip():
        return None

    code_prefix = code_string.strip().upper()[:3]
    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00,
    }
    return menu_prices.get(code_prefix, None)


def calculate_average_shot_cost(pricing_csv):
    """Calculate the average price across comma-separated espresso shot prices.

    Defensive against None, non-string, empty strings, malformed tokens,
    non-numeric elements, negative prices, and zero-division errors.
    """
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return 0.0

    prices = []
    for token in pricing_csv.split(","):
        cleaned = token.strip()
        if not cleaned:
            continue
        try:
            val = float(cleaned)
            if val >= 0:
                prices.append(val)
        except ValueError:
            continue

    if not prices:
        return 0.0

    return sum(prices) / len(prices)


def parse_order_modifiers(order_spec):
    """Parse key:value beverage modification specs separated by semicolons.

    Defensive against None, non-string, empty strings, missing colons,
    extra delimiters, trailing semicolons, and malformed pairs.
    """
    modifier_dict = {}
    if not isinstance(order_spec, str) or not order_spec.strip():
        return modifier_dict

    items = order_spec.split(";")
    for item in items:
        cleaned = item.strip()
        if not cleaned:
            continue
        if ":" in cleaned:
            parts = cleaned.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key:
                modifier_dict[key] = value

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
