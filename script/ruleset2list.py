import argparse


def process_file(filename, append_text=None):
    replace_dict = {
        "DOMAIN,": "full:",
        "DOMAIN-SUFFIX,": "domain:",
        "URL-REGEX,": "regexp:",
        "IP-CIDR,": "ip-cidr:",
        "DOMAIN-KEYWORD,": "keyword:"
    }

    with open(filename, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("#"):
            continue
        for key, value in replace_dict.items():
            line = line.replace(key, value)
        if append_text:
            line = line.strip() + ":" + append_text + '\n'
        new_lines.append(line)

    with open(filename, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a text file.")
    parser.add_argument(
        "filename", help="The name of the file to be processed")
    parser.add_argument("-t", "--tag", type=str, default=None,
                        help="Optional text to append at the end of each processed line")

    args = parser.parse_args()
    process_file(args.filename, args.tag)
