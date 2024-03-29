import sys


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
        line_tag = line[last_colon_index + 1:].strip()
        return exp_type, expression, line_tag


def remove_domains(a_path, b_path):
    with open(b_path, 'r') as f:
        lines = f.readlines()

    has_add = '# ADD\n' in lines
    has_remove = '# REMOVE\n' in lines

    to_remove = set()

    if has_add and has_remove:
        start = lines.index('# ADD\n') + 1
        end = lines.index('# REMOVE\n')
        to_remove = set(split_line(line.strip())[
                        1] for line in lines[start:end] if split_line(line.strip())[1])
    elif has_add and not has_remove:
        to_remove = set(split_line(line.strip())[1] for line in lines if split_line(
            line.strip())[1] and line.strip() != '# ADD')
    elif not has_add and not has_remove:
        to_remove = set(split_line(line.strip())[
                        1] for line in lines if split_line(line.strip())[1])

    with open(a_path, 'r') as f:
        a_lines = f.readlines()

    updated_lines = [line for line in a_lines if split_line(line.strip())[
        1] not in to_remove]

    with open(a_path, 'w') as f:
        f.writelines(updated_lines)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_a> <path_to_b>")
    else:
        remove_domains(sys.argv[1], sys.argv[2])
