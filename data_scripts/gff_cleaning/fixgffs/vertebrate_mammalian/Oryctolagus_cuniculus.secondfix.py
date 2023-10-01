# example abandoned mRNA
#NC_013677.1	Gnomon	mRNA	62198404	62253586	.	-	.	ID=rna-XM_017343633.1;Parent=gene-USP14;Dbxref=GeneID:100009078,Genbank:XM_017343633.1;Name=XM_017343633.1;gbkey=mRNA;gene=USP14;model_evidence=Supporting evidence includes similarity to: 1 EST%2C 1 Protein%2C and 100%25 coverage of the annotated genomic feature by RNAseq alignments%2C including 29 samples with support for all annotated introns;product=ubiquitin specific peptidase 14%2C transcript variant X1;transcript_id=XM_017343633.1
#NC_013677.1	BestRefSeq	mRNA	62199928	62253377	.	-	.	ID=rna-NM_001082257.1;Parent=gene-USP14;Dbxref=GeneID:100009078,Genbank:NM_001082257.1;Name=NM_001082257.1;Note=The RefSeq transcript has 2 substitutions compared to this genomic sequence;exception=annotated by transcript or proteomic data;gbkey=mRNA;gene=USP14;inference=similar to RNA sequence%2C mRNA (same species):RefSeq:NM_001082257.1;product=ubiquitin specific peptidase 14;transcript_id=NM_001082257.1
# example gene line
#NC_013669.1	Gnomon	gene	11622	29640	.	+	.	ID=gene-WDR31;Dbxref=GeneID:100345553;Name=WDR31;gbkey=Gene;gene=WDR31;gene_biotype=protein_coding

# inserts the gene entry for USP14 above the orphan mRNA entries, when it hits the first one
# this is basically manual, but stored in a script
patch = ['NC_013677.1', 'Gnomon', 'gene', '62198404', '62253586', '.', '-', '.', 'ID=gene-USP14;Dbxref=GeneID:100009078;gene_biotype=protein_coding']
with open('ncRNA_filtered.gff3.bu2') as f:
    for line in f:
        line = line.rstrip()
		if line.contains('ID=rna-XM_017343633.1;Parent=gene-USP14'):
			print('\t'.join(patch))
		print(line)

