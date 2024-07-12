import sys
import argparse
from mappings import LIST_RULESET_MAPPING


def process_line(line, tag_filter=None):
    first_colon_index = line.find(":")
    last_colon_index = line.rfind(":")

    # 当字符串中没有冒号
    if first_colon_index == -1:
        return line, "", ""

    A = line[:first_colon_index]

    # 当有两个或以上的冒号
    if first_colon_index != last_colon_index:
        B = line[first_colon_index+1:last_colon_index]
        C = line[last_colon_index+1:]
    else:
        # 当只有一个冒号
        B = line[first_colon_index+1:]
        C = ""

    if A in LIST_RULESET_MAPPING:
        new_A = LIST_RULESET_MAPPING[A]
    else:
        return None

    if tag_filter and (C != tag_filter):
        return None

    return f"{new_A},{B}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domainFile", help="Input domain file")
    parser.add_argument("outputFile", help="Output YAML file")
    parser.add_argument(
        "-t", "--tag", help="Optional tag filter", default=None)
    args = parser.parse_args()

    with open(args.domainFile, 'r') as file:
        lines = [line.strip()
                 for line in file if not line.strip().startswith('#')]

    output_data = "payload:\n"
    for line in lines:
        processed_line = process_line(line, args.tag)
        if processed_line:
            output_data += f"  - {processed_line}\n"

    with open(args.outputFile, 'w') as file:
        file.write(output_data)
