import argparse
from mappings import LIST_CLASH_RULESET_MAPPING


def process_line(line):
    try:
        type, content = line.split(":", 1)
        if type == "ip-cidr" or type == "ip-cidr6" or type == "ip-asn":
            if not content.endswith(",no-resolve"):
                content += ",no-resolve"
        return f"{LIST_CLASH_RULESET_MAPPING[type]},{content}"
    except ValueError:
        return f"DOMAIN-SUFFIX,{line}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Input file")
    parser.add_argument("-o", "--outputFile", help="Output file")
    parser.add_argument("-t", "--outputFiletype", help="Output file type")

    args = parser.parse_args()

    outputFile = args.outputFile if args.outputFile else args.inputFile
    outputFileType = args.outputFiletype if args.outputFiletype else "txt"

    with open(args.inputFile, 'r') as file:
        lines = [line.strip() for line in file if not line.strip().startswith('#')]
        if outputFileType == "yaml":
            output_data = "payload:\n"
            for line in lines:
                processed_line = process_line(line)
                if processed_line:
                    output_data += f"  - {processed_line}\n"
        elif outputFileType == "txt":
            output_data = ""
            for line in lines:
                output_data += process_line(line) + "\n"
        else:
            pass

    with open(outputFile, 'w') as file:
        file.write(output_data)
