LIST_RULESET_MAPPING = {
    "full": "DOMAIN",
    "domain": "DOMAIN-SUFFIX",
    "regexp": "DOMAIN-REGEX",
    "ip-cidr": "IP-CIDR",
    "ip-cidr6": "IP-CIDR6",
    "ip-asn": "IP-ASN",
    "keyword": "DOMAIN-KEYWORD"
}

RULESET_LIST_MAPPING = {v: k for k, v in LIST_RULESET_MAPPING.items()}
