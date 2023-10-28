import sys


def split_line(line):
    first_colon_index = line.find(":")
    last_colon_index = line.rfind(":")

    # 当字符串中没有冒号
    if first_colon_index == -1:
        return line, "", ""

    # 当只有一个冒号
    if first_colon_index == last_colon_index:
        A = line[:first_colon_index]
        B = line[first_colon_index+1:]
        C = ""
        return A, B, C

    # 当有两个或以上冒号
    A = line[:first_colon_index]
    B = line[first_colon_index+1:last_colon_index]
    C = line[last_colon_index+1:]

    return A, B, C


def join_line(A, B, C):
    if C:
        return f"{A}:{B}:{C}\n"
    else:
        return f"{A}:{B}\n"


def process_file(file_a_path, file_b_path):
    with open(file_a_path, 'r') as file_a:
        content_a = file_a.readlines()

    add_lines = []
    remove_lines = []
    current_section = None

    with open(file_b_path, 'r') as file_b:
        for line in file_b:
            line = line.strip()
            if line == "# ADD":
                current_section = 'add'
            elif line == "# REMOVE":
                current_section = 'remove'
            else:
                A, B, C = split_line(line)

                if current_section == 'add':
                    if all(split_line(x.strip())[1] != B for x in content_a):
                        add_lines.append(join_line(A, B, C))

                elif current_section == 'remove':
                    remove_lines.append(B)

    content_a = [line for line in content_a if split_line(line.strip())[
        1] not in remove_lines]
    content_a.extend(add_lines)

    with open(file_a_path, 'w') as file_a:
        file_a.writelines(content_a)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_A_path> <file_B_path>")
        sys.exit(1)

    file_a_path = sys.argv[1]
    file_b_path = sys.argv[2]
    process_file(file_a_path, file_b_path)
