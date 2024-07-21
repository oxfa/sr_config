import argparse
from mappings import CLASH_RULESET_LIST_MAPPING


def replace_mapping(line, mapping):
    line = line.strip()
    if not line:
        return None

    if line.startswith("#"):
        return line

    parts = line.split(',', 1)
    if len(parts) != 2:
        return None

    key, value = parts[0].strip(), parts[1].strip()
    if key in mapping:
        return f"{mapping[key]}:{value}"
    return None


def process_file(input_lines, mapping):
    output_lines = []
    for line in input_lines:
        result = replace_mapping(line, mapping)
        if result is not None:
            output_lines.append(result)
    return output_lines


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='Process a file with mapping replacements.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, nargs='?',
                        help='Path to the output file (optional)')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as infile:
        input_lines = infile.readlines()

    output_lines = process_file(input_lines, CLASH_RULESET_LIST_MAPPING)

    output_file = args.output_file if args.output_file else args.input_file

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    main()
