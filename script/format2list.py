import re
import argparse


def process_file_in_place(file_path, tag_arg=None):
    domain_pattern = re.compile(
        r'^(?!-)[a-zA-Z0-9-]+(?<!-)(?:\.(?!-)[a-zA-Z0-9-]+(?<!-))*\.[a-zA-Z]{2,63}$')

    replace_dict = {
        "DOMAIN,": "full:",
        "DOMAIN-SUFFIX,": "domain:",
        "URL-REGEX,": "regexp:",
        "IP-CIDR,": "ip-cidr:",
        "IP-ASN,": "ip-asn:",
        "DOMAIN-KEYWORD,": "keyword:"
    }

    with open(file_path, "r") as f_in:
        lines = f_in.readlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                continue

            if line.startswith(("domain:", "full:", "regexp:", "ip-cidr:", "ip-asn:", "keyword:")):
                pass
            elif line.startswith(tuple(tuple(replace_dict.keys()))):
                for key, value in replace_dict.items():
                    line = line.replace(key, value)
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
