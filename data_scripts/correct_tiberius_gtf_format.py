import argparse

def main(input_file, output_file):
    with open(input_file) as fin, open(output_file, "w") as fout:
        current_gene_id = None
        for line in fin:
            if line.startswith("#") or line.strip() == "":
                fout.write(line)
                continue

            fields = line.strip().split("\t")
            feature_type = fields[2]

            # If it's a gene, store the gene_id (from column 9 or column 8 if needed)
            if feature_type == "gene":
                current_gene_id = fields[8].strip()
                fout.write(line)
            elif feature_type == "transcript":
                # Extract transcript ID from column 9
                transcript_id = fields[8].strip()
                if current_gene_id is None:
                    raise ValueError("No gene_id found before transcript line!")

                # Replace attributes column with proper key-value format
                attributes = f'transcript_id "{transcript_id}"; gene_id "{current_gene_id}";'
                fields[8] = attributes
                fout.write("\t".join(fields) + "\n")
            else:
                fout.write(line)


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', required=True)
parser.add_argument('-o', '--output-file', required=True)
args = parser.parse_args()
main(args.input_file, args.output_file)

