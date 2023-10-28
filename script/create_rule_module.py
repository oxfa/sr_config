#!/usr/bin/env python3

from pathlib import Path
import re
import sys


def format_rule(fd, op_type):
    match op_type:
        case "DIRECT":
            op_text = op_type
        case "REJECT":
            op_text = op_type
        case "REJECT-DROP":
            op_text = op_type
        case "PROXY-FALLBACK" | "PROXY-WARP":
            extra_arg = sys.argv[5]
            if extra_arg == "force-remote-dns":
                op_text = op_type + "," + extra_arg
            else:  # TODO
                pass
        case _:
            pass
    formated_text = ""
    lines = fd.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        op_text_full = op_text
        first_colon_index = line.find(":")
        last_colon_index = line.rfind(":")
        # URL-REGEX DOMAIN DOMAIN-SUFFIX
        if first_colon_index != -1:
            url_type = line[:first_colon_index]
            if url_type == "full":
                prefix = "DOMAIN"
            elif url_type == "domain":
                prefix = "DOMAIN-SUFFIX"
            elif url_type == "regexp":
                prefix = "URL-REGEX"
            elif url_type == "ip-cidr":
                prefix = "IP-CIDR"
                op_text_full += ",no-resolve"
            elif url_type == "keyword":
                prefix = "DOMAIN-KEYWORD"
            elif url_type == "#":
                continue
            else:
                sys.exit("Error: No such url_type!")
            expression = line[first_colon_index +
                              1:last_colon_index] if last_colon_index > first_colon_index else line[first_colon_index + 1:]
        else:
            if line.startswith('#'):
                continue
            prefix = "DOMAIN-SUFFIX"
            expression = line
        line_text = prefix + ',' + \
            expression + ',' + op_text_full + '\n'
        formated_text += line_text
    return formated_text


def format_host(fd, op_type):
    if op_type == "DOMAIN-HOST":
        pass
    elif op_type == "DOMAIN-DNS":
        text = fd.read()
        dns_server = sys.argv[5]
        dns_info = " = server:" + dns_server
        replaced_info = "\g<1>" + dns_info + '\n' + "*.\g<1>" + dns_info
        formated_text = re.sub(r"^(.+)$", replaced_info,
                               text, sys.maxsize, re.MULTILINE)
    else:
        pass
    return formated_text


def format_text(fd, sec_type, op_type):
    if sec_type == "RULE":
        return format_rule(fd, op_type)
    elif sec_type == "HOST":
        return format_host(fd, op_type)
    else:
        pass
    pass


def format_module(fd, sec_type, op_type):
    preface_info = "#!name=" + Path(fd.name).stem
    if sec_type == "RULE":
        preface_info += "\n\n[Rule]\n"
        formated_text = format_rule(fd, op_type)
    elif sec_type == "HOST":
        preface_info += "\n\n[Host]\n"
        formated_text = format_host(fd, op_type)
    else:
        pass
    return preface_info + formated_text


if __name__ == "__main__":
    # File Name
    file_name = sys.argv[1]
    # Target name: TEXT or MODULE
    tgt_type = sys.argv[2]
    # Section Type: RULE or HOST
    sec_type = sys.argv[3]
    # Opreation Type:
    op_type = sys.argv[4]

    try:
        fd = open(file_name, 'r+')
        if tgt_type == "TEXT":
            final_text = format_text(fd, sec_type, op_type)
        elif tgt_type == "MODULE":
            final_text = format_module(fd, sec_type, op_type)
        else:
            pass
        fd.seek(0)
        fd.write(final_text)

    finally:
        fd.close()
