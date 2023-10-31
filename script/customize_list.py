import argparse


def split_line(line):
    first_colon_index = line.find(":")
    last_colon_index = line.rfind(":")

    # No colon present
    if first_colon_index == -1:
        return "", line.strip(), ""

    # Single colon
    elif first_colon_index == last_colon_index:
        exp_type = line[:first_colon_index].strip()
        expression = line[first_colon_index + 1:].strip()

        if expression.startswith("@"):
            return "", exp_type, expression
        else:
            return exp_type, expression, ""

    # Multiple colons
    else:
        exp_type = line[:first_colon_index].strip()
        expression = line[first_colon_index + 1:last_colon_index].strip()
        tag = line[last_colon_index + 1:].strip()
        return exp_type, expression, tag


def join_line(exp_type, expression, tag):
    return ":".join(filter(bool, [exp_type, expression, tag]))


def process_file(file_a_path, file_b_path, tag=None):
    with open(file_a_path, 'r') as file_a:
        content_a = file_a.read().splitlines()
    add_lines = []
    remove_lines = set()
    current_section = None

    with open(file_b_path, 'r') as file_b:
        for line in file_b:
            line = line.strip()
            if not line:
                continue
            if line == "# ADD":
                current_section = 'add'
            elif line == "# REMOVE":
                current_section = 'remove'
            else:
                exp_type, expression, tag = split_line(line)
                if tag and tag != tag:
                    continue
                if current_section == 'add':
                    if all(split_line(x.strip())[1] != expression for x in content_a):
                        add_lines.append(join_line(exp_type, expression, tag))
                elif current_section == 'remove':
                    remove_lines.add(expression)

    content_a = [line for line in content_a if split_line(line.strip())[
        1] not in remove_lines]
    content_a.extend(add_lines)

    with open(file_a_path, 'w') as file_a:
        file_a.write("\n".join(content_a))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_a_path", help="Path to File A")
    parser.add_argument("file_b_path", help="Path to File B")
    parser.add_argument("-t", "--tag", help="Optional tag to filter lines")
    args = parser.parse_args()

    process_file(args.file_a_path, args.file_b_path, args.tag)
