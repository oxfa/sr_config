import re
import argparse


def process_file_in_place(file_path):
    # 正则表达式用于匹配域名
    domain_pattern = re.compile(
        r'^(?!-)[a-zA-Z0-9-]+(?<!-)(?:\.(?!-)[a-zA-Z0-9-]+(?<!-))*\.[a-zA-Z]{2,63}$')

    # 读取文件内容
    with open(file_path, "r") as f_in:
        lines = f_in.readlines()

    # 处理内容并写回到文件
    with open(file_path, "w") as f_out:
        for line in lines:
            line = line.strip()
            if line.startswith(("domain:", "full:", "regexp:", "ip-cider:", "keyword:")):
                f_out.write(f"{line}\n")
            else:
                if domain_pattern.match(line):
                    f_out.write(f"domain:{line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Filter lines without specified prefixes and add "domain:" prefix to valid domain lines.')
    parser.add_argument('file_path', type=str,
                        help='The path of the text file to be modified in-place.')

    args = parser.parse_args()
    process_file_in_place(args.file_path)
