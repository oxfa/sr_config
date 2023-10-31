#!/usr/bin/env python3

from pathlib import Path
import re
import sys


def is_valid_domain(domain):
    pattern = re.compile(
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}')
    return bool(pattern.fullmatch(domain))


def split_line(line):
    segments = line.split(":")
    if len(segments) == 1:
        return "", segments[0].strip(), ""
    elif len(segments) == 2:
        return segments[0].strip(), segments[1].strip(), ""
    else:
        return segments[0].strip(), segments[1].strip(), segments[2].strip()


def format_rule(fd, op_type):
    formatted_text = ""
    lines = fd.readlines()

    for line in lines:
        if line.startswith("#"):
            continue

        exp_type, expression, _ = split_line(line.strip())
        if not exp_type:
            continue

        prefix = {
            "full": "DOMAIN",
            "domain": "DOMAIN-SUFFIX",
            "regexp": "URL-REGEX",
            "ip-cidr": "IP-CIDR",
            "keyword": "DOMAIN-KEYWORD",
        }.get(exp_type, None)

        if prefix is None:
            sys.exit(f"Invalid exp_type1: {exp_type}, line text: {line}")

        op_text_full = op_type
        if exp_type == "ip-cidr":
            op_text_full += ",no-resolve"

        formatted_text += f"{prefix},{expression},{op_text_full}\n"

    return formatted_text


def format_host(fd, op_type):
    formated_text = ""
    if op_type == "DOMAIN-HOST":
        pass
    elif op_type == "DOMAIN-DNS":
        if len(sys.argv) < 6:
            sys.exit("Missing DNS server info in sys.argv[5]")
        dns_server = sys.argv[5]
        dns_info = " = server:" + dns_server
        lines = fd.read().splitlines()
        for line in lines:
            exp_type, expression, _ = split_line(line)
            if exp_type == "full":
                if is_valid_domain(expression):
                    formated_text += f"{expression}{dns_info}\n"
            elif exp_type == "domain":
                if is_valid_domain(expression):
                    formated_text += f"*.{expression}{dns_info}\n"
            elif exp_type == "domain&full":
                if is_valid_domain(expression):
                    formated_text += f"{expression}{dns_info}\n"
                    formated_text += f"*.{expression}{dns_info}\n"
            else:
                buf = ""
                for i in lines:
                    buf += i
                sys.exit(
                    f"Invalid exp_type2: '{exp_type}', exp: {expression}, line: {line}, dns: {dns_server}, buf: {buf}, ")
    else:
        pass
    return formated_text


def format_module(fd, sec_type, op_type):
    preface_info = f"#!name={Path(fd.name).stem}\n\n[{sec_type}]\n"

    if sec_type == "RULE":
        formatted_text = format_rule(fd, op_type)
    elif sec_type == "HOST":
        formatted_text = format_host(fd, op_type)
    else:
        return ""

    return preface_info + formatted_text


def format_text(fd, sec_type, op_type):
    if sec_type == "RULE":
        return format_rule(fd, op_type)
    elif sec_type == "HOST":
        return format_host(fd, op_type)
    else:
        pass


if __name__ == "__main__":
    file_name = sys.argv[1]
    tgt_type = sys.argv[2]
    sec_type = sys.argv[3]
    op_type = sys.argv[4]

    with open(file_name, 'r+') as fd:
        if tgt_type == "TEXT":
            final_text = format_text(fd, sec_type, op_type)
        elif tgt_type == "MODULE":
            final_text = format_module(fd, sec_type, op_type)
        else:
            sys.exit("Unknown target type")

        fd.seek(0)
        fd.write(final_text)
        fd.truncate()
