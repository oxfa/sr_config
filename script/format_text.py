#!/usr/bin/env python3

from pathlib import Path
import re
import sys

fileName = sys.argv[1]
op_type = sys.argv[2]

try:
    final_text = ""
    fd = open(fileName, 'r+')
    if op_type == "DIRECT" or op_type == "REJECT":
        lines = fd.readlines()
        pattern = re.compile(r'^(full:|regexp:)?(.*)$')
        for line in lines:
            matchObj = re.match(pattern, line)
            url_type = matchObj.group(1)
            # URL-REGEX DOMAIN DOMAIN-SUFFIX
            if url_type == "full:":
                prefix = "DOMAIN"
            elif url_type == "regexp:":
                prefix = "URL-REGEX"
            else:
                prefix = "DOMAIN-SUFFIX"
            line_text = prefix + ',' + matchObj.group(2) + ',' + op_type + '\n'
            final_text = final_text + line_text
        part_info = "### " + op_type + " part ###" + '\n'
        final_text = re.sub(r"^", part_info, final_text)
    elif op_type == "DOMAIN_DNS":
        final_text = fd.read()
        dns_server = sys.argv[3]
        dns_info = " = server:" + dns_server
        preface_info = "#!name=" + Path(fd.name).stem + "\n\n[Host]\n"
        replaced_info = "\g<1>" + dns_info + '\n' + "*.\g<1>" + dns_info
        final_text = re.sub(r"^(.+)$", replaced_info, final_text, sys.maxsize, re.MULTILINE)
        final_text = re.sub(r"^", preface_info, final_text)
    else:  # DOMAIN_HOST
        pass

    fd.seek(0)
    fd.write(final_text)

finally:
    fd.close()
