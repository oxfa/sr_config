import argparse
import os


def sort_lines_by_key_values(file_path, key_value_pairs):
    try:
        # 读取文件
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except IOError as e:
        raise Exception(f"Error reading file: {e}")

    # 反转键值对，以便根据值查找键
    value_to_key = {v: k for k, v in key_value_pairs.items()}

    # 根据键值对中的键进行排序
    sorted_lines = sorted(lines, key=lambda line: list(
        key_value_pairs.keys()).index(value_to_key.get(line.split()[0], "")))

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

    key_value_pairs = {
        "keyword": "DOMAIN-KEYWORD",
        "domain": "DOMAIN-SUFFIX",
        "full": "DOMAIN",
        "regexp": "URL-REGEX",
        "ip-asn": "IP-ASN",
        "ip-cidr": "IP-CIDR"
    }

    try:
        sorted_lines = sort_lines_by_key_values(
            args.input_file, key_value_pairs)
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
