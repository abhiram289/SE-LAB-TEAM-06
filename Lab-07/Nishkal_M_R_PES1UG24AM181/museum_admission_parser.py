def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    Assumes name contains at least one word.
    """
    parts = name.split()
    return parts[-1].title() + ', ' + ' '.join(parts[:-1]).title()

def parse_group_ages(text):
    """
    Parses space-separated ages into a list of ints.
    Assumes every value is a whole number.
    """
    return [int(age) for age in text.split()]

def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Assumes text is a valid date with two dashes.
    """
    year, month, day = text.strip().split('-')
    return int(year), int(month), int(day)

def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))

if __name__ == "__main__":
    main()
