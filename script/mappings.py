
LIST_SR_RULESET_MAPPING = {
    "keyword": "DOMAIN-KEYWORD",
    "full": "DOMAIN",
    "domain": "DOMAIN-SUFFIX",
    "regexp": "URL-REGEX",
    "ip-cidr": "IP-CIDR",
    "ip-cidr6": "IP-CIDR",
    "ip-asn": "IP-ASN"
}

LIST_CLASH_RULESET_MAPPING = {
    "keyword": "DOMAIN-KEYWORD",
    "full": "DOMAIN",
    "domain": "DOMAIN-SUFFIX",
    "regexp": "DOMAIN-REGEX",
    "ip-cidr": "IP-CIDR",
    "ip-cidr6": "IP-CIDR6",
    "ip-asn": "IP-ASN"
}

SR_RULESET_LIST_MAPPING = {v: k for k, v in LIST_SR_RULESET_MAPPING.items()}

CLASH_RULESET_LIST_MAPPING = {v: k for k,
                              v in LIST_CLASH_RULESET_MAPPING.items()}
