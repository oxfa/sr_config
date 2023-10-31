import argparse


def split_line(line):
    segments = line.split(":")
    if len(segments) == 1:
        return "", segments[0].strip(), ""
    elif len(segments) == 2:
        if segments[1].strip().startswith('@'):
            return "", segments[0].strip(), segments[1].strip()
        else:
            return segments[0].strip(), segments[1].strip(), ""
    else:
        return segments[0].strip(), segments[1].strip(), segments[2].strip()


def join_line(A, B, C):
    if A and B and C:
        return f"{A}:{B}:{C}\n"
    elif A and B:
        return f"{A}:{B}\n"
    elif B and C:
        return f"{B}:{C}\n"
    else:
        return f"{B}\n"


def process_file(file_a_path, file_b_path, tag=None):
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

                if tag and C != tag:
                    continue

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
    parser = argparse.ArgumentParser()
    parser.add_argument("file_a_path", help="Path to File A")
    parser.add_argument("file_b_path", help="Path to File B")
    parser.add_argument("-t", "--tag", help="Optional tag to filter lines")
    args = parser.parse_args()

    process_file(args.file_a_path, args.file_b_path, args.tag)
