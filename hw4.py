import sys
import os
import pickle


def load_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: Cannot find file '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def display_data(data):
    for entry in data:
        print(entry)
    print(f"Total entries: {len(data)}")


def filter_by_state(data, state_abbr): # Filters counties by abbreviation
    filtered = [county for county in data if county.get("State") == state_abbr]
    print(f"Filter: state == {state_abbr} ({len(filtered)} entries)")
    return filtered


def filter_gt(data, field, value): # Filters counties by field value (greater)

    filtered = [county for county in data if county.get(field, 0) > value]
    print(f"Filter: {field} gt {value} ({len(filtered)} entries)")
    return filtered


def filter_lt(data, field, value): # Filters counties by field value (lesser)
    filtered = [county for county in data if county.get(field, 0) < value]
    print(f"Filter: {field} lt {value} ({len(filtered)} entries)")
    return filtered


def population_total(data): # Prints the total 2014 population of all counties
    total_population = sum(county.get("2014 Population", 0) for county in data)
    print(f"2014 population: {total_population}")


def population_sub_field(data, field):
   #Prints the total sub-population for a percentage-based field.
    total = sum(
        county.get("2014 Population", 0) * (county.get(field, 0) / 100)
        for county in data
    )
    print(f"2014 {field} population: {total}")


def percent_field(data, field):
    # Prints the percentage of the total population in a sub-population for a field.
    total_population = sum(county.get("2014 Population", 0) for county in data)
    if total_population == 0:
        print(f"2014 {field} percentage: 0")
        return
    sub_population = sum(
        county.get("2014 Population", 0) * (county.get(field, 0) / 100)
        for county in data
    )
    percentage = (sub_population / total_population) * 100
    print(f"2014 {field} percentage: {percentage}")


def process_operations(file_path, data):
    # Reads the operations file and executes commands in order.
    try:
        with open(file_path, 'r') as f:
            operations = f.readlines()
    except FileNotFoundError:
        print(f"Error: Operations file '{file_path}' not found.")
        sys.exit(1)

    for line_num, line in enumerate(operations, 1):
        line = line.strip()
        if not line or line.startswith("#"):  # Skip blank lines or comments
            continue

        try:
            parts = line.split(":")
            command = parts[0]

            if command == "display":
                display_data(data)
            elif command == "filter-state":
                state_abbr = parts[1]
                data = filter_by_state(data, state_abbr)
            elif command == "filter-gt":
                field, value = parts[1], float(parts[2])
                data = filter_gt(data, field, value)
            elif command == "filter-lt":
                field, value = parts[1], float(parts[2])
                data = filter_lt(data, field, value)
            elif command == "population-total":
                population_total(data)
            elif command == "population":
                field = parts[1]
                population_sub_field(data, field)
            elif command == "percent":
                field = parts[1]
                percent_field(data, field)
            else:
                print(f"Error: Unknown command on line {line_num}: {line}")
        except (IndexError, ValueError) as e:
            print(f"Error: Malformed operation on line {line_num}: {line} ({e})")
            continue


def main():
    # Check for command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python hw4.py <operations_file>")
        sys.exit(1)

    # Load the dataset
    dataset_path = "county_demographics.data"  # Path to  dataset file
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found.")
        sys.exit(1)

    data = load_data(dataset_path)
    print(f"Number of entries: {len(data)}")

    # Process the operations file
    operations_file = sys.argv[1]
    process_operations(operations_file, data)


if __name__ == "__main__":
    main()