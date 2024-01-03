import argparse


def sort_lines_by_values(file_path, key_value_pairs):
    # 读取文件
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 创建一个字典来存储键值对应的排序值
    value_order = {k: v for k, v in key_value_pairs.items()}

    # 根据键值对中的值进行排序
    sorted_lines = sorted(
        lines, key=lambda line: value_order.get(line.split()[0], line))

    return sorted_lines


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Sort lines in a file based on predefined key-value pairs.")
    parser.add_argument("file_path", type=str, help="Path to the input file")
    args = parser.parse_args()

    # 定义键值对
    key_value_pairs = {
        "full": "DOMAIN",
        "domain": "DOMAIN-SUFFIX",
        "regexp": "URL-REGEX",
        "ip-cidr": "IP-CIDR",
        "ip-asn": "IP-ASN",
        "keyword": "DOMAIN-KEYWORD"
    }

    # 对文件中的行进行排序
    sorted_lines = sort_lines_by_values(args.file_path, key_value_pairs)

    # 输出排序后的结果
    for line in sorted_lines:
        print(line.strip())


if __name__ == "__main__":
    main()
