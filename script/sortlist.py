import argparse
import os
from mappings import LIST_RULESET_MAPPING


def sort_lines_by_key_values(file_path, key_value_pairs):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 确保每行都以换行符结束
        lines = [line if line.endswith(
            '\n') else line + '\n' for line in lines]

    except IOError as e:
        raise Exception(f"Error reading file: {e}")

    # 为不在列表中的键指定一个默认索引
    default_index = len(key_value_pairs)

    sorted_lines = sorted(
        lines,
        key=lambda line: list(key_value_pairs.keys()).index(
            line.split(':')[0].strip()) if line.split(':')[0].strip() in key_value_pairs else default_index
    )

    return sorted_lines


def write_to_file(file_path, lines):
    try:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    except IOError as e:
        raise Exception(f"Error writing file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Sort lines in a file based on key-values.")
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("-o", "--output_file", type=str,
                        help="Path to the output file (optional)", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist.")
        return

    try:
        sorted_lines = sort_lines_by_key_values(
            args.input_file, LIST_RULESET_MAPPING)
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
