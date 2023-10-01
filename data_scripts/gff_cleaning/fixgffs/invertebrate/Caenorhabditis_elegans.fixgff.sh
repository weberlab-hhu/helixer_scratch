mv ncRNA_filtered.gff3 ncRNA_filtered.gff3.bu
# there is some random extra primary_transcripts, spot check
# seems to overlap with otherwise OK gene model, so just
# removing extraneous entries and crossing fingers (correct primary transcripts have ;Parent=)
cat ncRNA_filtered.gff3.bu | grep -v 'primary_transcript.*ID=[^;]*;Dbx' > ncRNA_filtered.gff3
