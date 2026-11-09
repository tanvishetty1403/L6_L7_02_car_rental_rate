import math

def sanitize_license_plate(plate):
    if not isinstance(plate, str):
        return ""
    plate = plate.strip()
    for ch in ['-', ' ', '_', '#']:
        plate = plate.replace(ch, '')
    return plate.upper()

def parse_trip_mileage(mileage_csv):
    if not isinstance(mileage_csv, str):
        return []
    result = []
    for part in mileage_csv.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            value = float(part)
        except ValueError:
            continue
        if math.isfinite(value) and value >= 0:
            result.append(value)
    return result

def format_rental_invoice(record):
    if not isinstance(record, str):
        return "Invalid record"
    parts = record.split(':')
    if len(parts) != 3:
        return "Invalid record"
    driver, days_str, category = (p.strip() for p in parts)
    if not driver or not category:
        return "Invalid record"
    try:
        days = int(days_str)
    except (ValueError, OverflowError):
        return "Invalid record"
    if not 1 <= days <= 365:
        return "Invalid record"
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"

def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    print("Sanitized Plate:", sanitize_license_plate(raw_plate))

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    print("Parsed Mileage List:", parse_trip_mileage(csv_input))

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    print("Rental Invoice:", format_rental_invoice(record_input))

if __name__ == "__main__":
    main()
