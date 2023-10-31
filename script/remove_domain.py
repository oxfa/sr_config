import sys


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
