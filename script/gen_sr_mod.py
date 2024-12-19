#!/usr/bin/env python3

import re
import sys
import argparse
from pathlib import Path
from mappings import CLASH_RULESET_SR_RULESET_MAPPING


def is_valid_domain(domain):
    pattern = re.compile(
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}')
    return bool(pattern.fullmatch(domain))

def format_rule(file_in, op_type, optional_val):
    formatted_text = ""
    lines = file_in.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            # 尝试分割字符串
            exp_type, expression = line.split(",", 1)
        except ValueError:
            # 捕获分割不足两部分时的异常
            print(f"Skipping invalid line: {line}, {' '.join(args.args)}")
            sys.exit(1)
        # exp_type, expression = line.split(",", 1)
        if not exp_type:
            continue

        prefix = CLASH_RULESET_SR_RULESET_MAPPING.get(exp_type, None)

        if prefix:
            op_text_full = op_type + f",{optional_val}" if optional_val else op_type
            formatted_text += f"{prefix},{expression},{op_text_full}\n"

    return formatted_text


def format_host(file_in, op_type, dns_server):
    formated_text = ""
    if op_type == "DOMAIN-HOST":
        pass
    elif op_type == "DOMAIN-DNS":
        dns_info = " = server:" + dns_server
        lines = file_in.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                # 尝试分割字符串
                exp_type, expression = line.split(",", 1)
            except ValueError:
                # 捕获分割不足两部分时的异常
                print(f"Skipping invalid line: {line}, {' '.join(args.args)}")
                sys.exit(1)
            if exp_type == "DOMAIN":
                if is_valid_domain(expression):
                    formated_text += f"{expression}{dns_info}\n"
            elif exp_type == "DOMAIN-SUFFIX":
                if is_valid_domain(expression):
                    formated_text += f"*.{expression}{dns_info}\n"
            else:
                sys.exit(
                    f"Invalid exp_type2: '{exp_type}', exp: {expression}, line: {line}, dns: {dns_server}")
    else:
        pass
    return formated_text


def format_module(file_in, sec_type, op_type, optional_val):
    preface_info = f"#!name={Path(file_in.name).stem}\n\n[{sec_type}]\n"

    if sec_type == "RULE":
        formatted_text = format_rule(file_in, op_type, optional_val)
    elif sec_type == "HOST":
        formatted_text = format_host(file_in, op_type, optional_val)
    else:
        return ""

    return preface_info + formatted_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("sec_type", help="Output file type")
    parser.add_argument("op_type", help="Output file type")
    parser.add_argument("--optional_val", help="optional value")
    parser.add_argument("-o", "--output_file", help="Output file")

    args = parser.parse_args()

    with open(args.input_file, 'r') as file_in:
        final_text = format_module(file_in, args.sec_type, args.op_type, args.optional_val)

    output_file  = args.output_file if args.output_file else args.input_file
    with open(output_file, 'w') as file_out:
        file_out.seek(0)
        file_out.write(final_text)
        file_out.truncate()
