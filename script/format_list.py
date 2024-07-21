import re
import argparse
from mappings import LIST_SR_RULESET_MAPPING


def process_file_in_place(file_path, tag_arg=None):
    domain_pattern = re.compile(
        r'^(?!-)[a-zA-Z0-9-]+(?<!-)(?:\.(?!-)[a-zA-Z0-9-]+(?<!-))*\.[a-zA-Z]{2,63}$')

    with open(file_path, "r") as f_in:
        lines = f_in.readlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue

            if line.startswith(tuple(f"{value}:" for value in LIST_SR_RULESET_MAPPING.keys())):
                pass
            else:
                # for key, value in CLASH_RULESET_LIST_MAPPING.items():
                #     if line.startswith(f"{key},"):
                #         line = line.replace(f"{key},", f"{value}:")
                #         break

                if line.startswith(("ip-cidr:", "ip-cidr6", "ip-asn:")):
                    line = line.rstrip(",no-resolve")

                elif domain_pattern.match(line):
                    line = f"domain:{line}"
                else:
                    print(f"Invalid line: {line}")
                    continue

            if tag_arg:
                line = f"{line}:{tag_arg}"
            new_lines.append(line + '\n')

    with open(file_path, "w") as f_out:
        f_out.writelines(new_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Filter lines without specified prefixes and add "domain:" prefix to valid domain lines.')
    parser.add_argument('file_path', type=str,
                        help='The path of the text file to be modified in-place.')
    parser.add_argument('-t', '--tag', type=str, default=None,
                        help='Optional tag to append at the end of each line.')

    args = parser.parse_args()
    process_file_in_place(args.file_path, args.tag)
