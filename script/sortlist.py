import argparse
import os


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


def write_to_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Sort lines in a file based on predefined key-value pairs.")
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("-o", "--output_file", type=str,
                        help="Path to the output file (optional)", default=None)
    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist.")
        return

    # 定义键值对
    key_value_pairs = {
        "keyword": "DOMAIN-KEYWORD",
        "domain": "DOMAIN-SUFFIX",
        "full": "DOMAIN",
        "regexp": "URL-REGEX",
        "ip-asn": "IP-ASN",
        "ip-cidr": "IP-CIDR"
    }

    # 对文件中的行进行排序
    sorted_lines = sort_lines_by_values(args.input_file, key_value_pairs)

    # 写入输出文件或覆盖原文件
    output_file = args.output_file if args.output_file else args.input_file
    write_to_file(output_file, sorted_lines)

    print(f"Sorted lines written to {output_file}")


if __name__ == "__main__":
    main()
