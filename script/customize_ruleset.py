import argparse

def split_line(line):
    """
    解析一行，支持以逗号分隔的格式：
    - DOMAIN-SUFFIX,deviantart.com
    返回两部分：类型（type）、内容（expression）。
    """
    if ',' not in line:
        return "", line.strip()
    exp_type, expression = line.split(",", 1)
    return exp_type.strip(), expression.strip()

def join_line(exp_type, expression):
    """
    拼接一行，按照逗号分隔的格式：
    - DOMAIN-SUFFIX,deviantart.com
    """
    return ",".join([exp_type, expression])

def process_file(inputFile, customFile, mode):
    add_lines = []
    remove_lines = set()
    current_section = None

    with open(inputFile, 'r') as file_a:
        content_a = file_a.read().splitlines()

    with open(customFile, 'r') as file_b:
        if mode == "remove_domains":
            for line in file_b:
                line = line.strip()
                if line and not line.startswith('#'):
                    remove_lines.add(line)
        elif mode == "add_domains":
            content_a = [line.strip() for line in file_b if not line.strip().startswith('#')]
        else:
            for line in file_b:
                line = line.strip()
                if line == "# ADD":
                    current_section = 'add'
                elif line == "# REMOVE":
                    current_section = 'remove'
                else:
                    if line and not line.startswith('#'):
                        exp_type, expression = split_line(line)
                        if current_section == 'add':
                            # 确保 expression 不重复
                            if all(split_line(x.strip())[1] != expression for x in content_a):
                                add_lines.append(join_line(exp_type, expression))
                        elif current_section == 'remove':
                            remove_lines.add(expression)

    # 移除和添加内容
    content_a = [line for line in content_a if split_line(line.strip())[1] not in remove_lines]
    content_a.extend(add_lines)

    # 写回文件
    with open(inputFile, 'w') as file_a:
        file_a.write("\n".join(content_a))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="input file")
    parser.add_argument("customFile", help="customization file")
    parser.add_argument("-m", "--mode", help="mode")
    args = parser.parse_args()

    process_file(args.inputFile, args.customFile, args.mode)