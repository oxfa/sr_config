import re
import argparse
import subprocess  # 用于调用外部脚本


def process_file_in_place(file_path, tag=None):
    domain_pattern = re.compile(
        r'^(?!-)[a-zA-Z0-9-]+(?<!-)(?:\.(?!-)[a-zA-Z0-9-]+(?<!-))*\.[a-zA-Z]{2,63}$')

    prefixes = ["DOMAIN,", "DOMAIN-SUFFIX,",
                "URL-REGEX,", "IP-CIDR,", "DOMAIN-KEYWORD,"]

    with open(file_path, "r") as f_in:
        lines = f_in.readlines()

    if any(line.startswith(tuple(prefixes)) for line in lines):
        # 调用 ruleset2list.py 进行转换
        subprocess_args = ["python", "ruleset2list.py", file_path]
        if tag:
            subprocess_args.extend(["-t", tag])
        subprocess.run(subprocess_args)
        return

    with open(file_path, "w") as f_out:
        for line in lines:
            line = line.strip()
            if line.startswith(("domain:", "full:", "regexp:", "ip-cidr:", "keyword:")):
                f_out.write(f"{line}{':' + tag if tag else ''}\n")
            else:
                if domain_pattern.match(line):
                    f_out.write(f"domain:{line}{':' + tag if tag else ''}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Filter lines without specified prefixes and add "domain:" prefix to valid domain lines.')
    parser.add_argument('file_path', type=str,
                        help='The path of the text file to be modified in-place.')
    parser.add_argument('-t', '--tag', type=str, default=None,
                        help='Optional tag to append at the end of each line.')

    args = parser.parse_args()
    process_file_in_place(args.file_path, args.tag)
