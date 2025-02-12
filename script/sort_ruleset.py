import argparse
import os
from mappings import MHM_RULESET_SR_RULESET_MAPPING


def sort_lines_by_key_values(file_path, key_value_pairs):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            lines = [line.rstrip('\n') for line in lines if (not line.startswith('#')) and (not line.startswith('PROCESS-NAME,')) ]

            unique_lines = list(set(lines))

            default_index = len(key_value_pairs)

            sorted_lines = sorted(
                unique_lines,
                key=lambda line: list(key_value_pairs.keys()).index(
                    line.split(',')[0].strip()) if line.split(',')[0].strip() in key_value_pairs else default_index
            )

            sorted_lines = [line + '\n' for line in sorted_lines]

        return sorted_lines

    except IOError as e:
        raise Exception(f"Error reading file: {e}")


def write_to_file(file_path, lines):
    try:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    except IOError as e:
        raise Exception(f"Error writing file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Sort lines in a file based on key-values and remove duplicates.")
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("-o", "--output_file", type=str,help="Path to the output file (optional)", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist.")
        return

    try:
        sorted_lines = sort_lines_by_key_values(args.input_file, MHM_RULESET_SR_RULESET_MAPPING)
    except Exception as e:
        print(e)
        return

    output_file = args.output_file if args.output_file else args.input_file
    try:
        write_to_file(output_file, sorted_lines)
    except Exception as e:
        print(e)
        return

    print(f"Sorted lines written to {output_file}")


if __name__ == "__main__":
    main()
