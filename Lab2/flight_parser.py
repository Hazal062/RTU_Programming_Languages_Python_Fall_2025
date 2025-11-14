import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

STUDENT_ID = "231ADB264"
FIRST_NAME = "Hazal"
LAST_NAME = "Guc"

DATE_FORMAT = "%Y-%m-%d %H:%M"


def validate_flight_id(flight_id: str) -> str | None:
    if not (2 <= len(flight_id) <= 8) or not flight_id.isalnum():
        return "flight_id must be 2-8 alphanumeric characters"
    return None


def validate_airport(code: str, field_name: str) -> str | None:
    if len(code) != 3 or not code.isalpha() or not code.isupper():
        return f"{field_name} must be 3 uppercase letters"
    return None


def parse_datetime_str(dt_str: str, field_name: str) -> Tuple[datetime | None, str | None]:
    try:
        return datetime.strptime(dt_str, DATE_FORMAT), None
    except ValueError:
        return None, f"{field_name} has invalid format (expected YYYY-MM-DD HH:MM)"


def validate_price(price_str: str) -> Tuple[float | None, str | None]:
    try:
        price = float(price_str)
        if price <= 0:
            return None, "price must be positive"
        return price, None
    except ValueError:
        return None, "price must be a number"


def validate_row(row: List[str]) -> Tuple[Dict, List[str]]:
    errors: List[str] = []

    if len(row) != 6:
        return {}, ["missing required fields"]

    flight_id, origin, destination, dep_str, arr_str, price_str = row

    err = validate_flight_id(flight_id)
    if err:
        errors.append(err)

    for code, name in [(origin, "origin"), (destination, "destination")]:
        err = validate_airport(code, name)
        if err:
            errors.append(err)

    dep_dt, dep_err = parse_datetime_str(dep_str, "departure_datetime")
    arr_dt, arr_err = parse_datetime_str(arr_str, "arrival_datetime")

    if dep_err:
        errors.append(dep_err)
    if arr_err:
        errors.append(arr_err)

    if dep_dt and arr_dt and arr_dt <= dep_dt:
        errors.append("arrival_datetime must be after departure_datetime")

    price, price_err = validate_price(price_str)
    if price_err:
        errors.append(price_err)

    if errors:
        return {}, errors

    flight = {
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "departure_datetime": dep_str,
        "arrival_datetime": arr_str,
        "price": price,
    }
    return flight, []


def parse_csv_file(path: Path) -> Tuple[List[Dict], List[str]]:
    valid_flights: List[Dict] = []
    error_lines: List[str] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, start=1):
            if not row:
                continue

            joined = ",".join(row).strip()

            if joined.startswith("#"):
                continue

            if line_no == 1 and "flight_id" in row[0].lower():
                continue

            flight, errs = validate_row(row)
            if errs:
                msg = f"Line {line_no}: {joined} -> " + "; ".join(errs)
                error_lines.append(msg)
            else:
                valid_flights.append(flight)

    return valid_flights, error_lines


def write_db_json(flights: List[Dict], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(flights, f, indent=4)


def write_errors(error_lines: List[str], path: Path) -> None:
    if not error_lines:
        return
    with path.open("w", encoding="utf-8") as f:
        for line in error_lines:
            f.write(line + "\n")


def parse_all_sources(input_file: str | None, directory: str | None) -> Tuple[List[Dict], List[str]]:
    csv_files: List[Path] = []

    if input_file:
        csv_files.append(Path(input_file))

    if directory:
        csv_files.extend(Path(directory).glob("*.csv"))

    if not csv_files:
        raise ValueError("No CSV files provided. Use -i or -d arguments.")

    all_valid: List[Dict] = []
    all_errors: List[str] = []

    for csv_path in csv_files:
        valid, errors = parse_csv_file(csv_path)
        all_valid.extend(valid)
        all_errors.extend(errors)

    return all_valid, all_errors


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Flight schedule parser"
    )
    parser.add_argument("-i", "--input", help="Path to single CSV file")
    parser.add_argument("-d", "--directory", help="Path to folder with CSV files")
    parser.add_argument("-o", "--output", help="Output JSON path for valid flights (db.json)")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    default_db_path = base_dir / "db.json"
    errors_path = base_dir / "errors.txt"

    try:
        flights, errors = parse_all_sources(args.input, args.directory)
    except ValueError as e:
        print(e)
        return

    output_path = Path(args.output) if args.output else default_db_path

    write_db_json(flights, output_path)
    write_errors(errors, errors_path)

    print(f"Student: {STUDENT_ID} {FIRST_NAME} {LAST_NAME}")
    print(f"Valid flights: {len(flights)}")
    print(f"JSON written to: {output_path}")
    if errors:
        print(f"Errors written to: {errors_path}")
    else:
        print("No invalid lines found.")


if __name__ == "__main__":
    main()
