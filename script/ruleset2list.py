import argparse


def process_file(filename, append_text=None):
    # 创建一个字典存储对应关系
    replace_dict = {
        "DOMAIN,": "full:",
        "DOMAIN-SUFFIX,": "domain:",
        "URL-REGEX,": "regexp:",
        "IP-CIDR,": "ip-cidr:",
        "DOMAIN-KEYWORD,": "keyword:"
    }

    # 读取文件
    with open(filename, "r") as f:
        lines = f.readlines()

    # 进行替换和删除操作
    new_lines = []
    for line in lines:
        # 删除以 "#" 开始的行
        if line.startswith("#"):
            continue

        # 替换内容
        for key, value in replace_dict.items():
            line = line.replace(key, value)

        # 添加指定文本（如果有）
        if append_text:
            line = line.strip() + ":" + append_text + '\n'

        new_lines.append(line)

    # 写回文件
    with open(filename, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a text file.")
    parser.add_argument(
        "filename", help="The name of the file to be processed")
    parser.add_argument("tag", nargs="?", default=None,
                        help="Optional text to append at the end of each processed line")

    args = parser.parse_args()
    process_file(args.filename, args.tag)
