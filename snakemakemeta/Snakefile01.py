import glob
configfile: "config.yml"


# find the things
# I think there is a more native snakemake glob-thing
# less sure on what it would gain right now...
sp = config['species']
datpath = config['datpath']
run_BUSCO = config['run_BUSCO']
lineage = config['lineage']
genome_fa_gz = glob.glob(f'{datpath}/{sp}/*/assembly/*.fa.gz')[0] 
annotation_gff3_gz = glob.glob(f'{datpath}/{sp}/*/annotation/*.gff3.gz')[0]
genome_fa = genome_fa_gz.replace('.gz', '')
annotation_gff3 = annotation_gff3_gz.replace('.gz', '')
anno_outdir = glob.glob(f'{datpath}/{sp}/*/annotation')[0]


def busco_input(wildcards):
    if wildcards.mode == 'tran':
        fasta = f'{anno_outdir}/transcripts.fa'
    elif wildcards.mode == 'geno':
        fasta = genome_fa
    elif wildcards.mode == 'prot':
        fasta = f'{anno_outdir}/proteins.fa'
    else:
        raise(ValueError(f'{wildcards.mode} not recognized mode in tran/geno/prot'))
    return fasta



rule all:
    input:
        f'{datpath}/{sp}/done_at.txt'


rule fin:
    output:
        f'{datpath}/{sp}/done_at.txt' 
    input:
        # multiple unnamed inputs will just be concatenated with white space
        # or accessed with [0], [1], ...
        f'{anno_outdir}/transcripts.fa',
        f'{anno_outdir}/cds.fa',
        f'{anno_outdir}/proteins.fa',
        f'{datpath}/{sp}/meta_collection/quast/geno',
        f'{datpath}/{sp}/meta_collection/gff_features/counts.txt',
        expand(f'{datpath}/{sp}/meta_collection/jellyfish/k{{k}}mer_counts.tsv', k=list(range(1,8))),
        expand(f'{datpath}/{sp}/meta_collection/busco/{{mode}}', mode=['geno', 'tran', 'prot'])
    shell:
        'ls {input} && date > {output}'


# prep files for the meta-data measuring tools
rule decomp:
    shell:
        'zcat {input} > {output}'

use rule decomp as decom_anno with:
    input:
        annotation_gff3 + '.gz'

    output:
        annotation_gff3

use rule decomp as decom_fa with:
    input:
        genome_fa + '.gz'
    output:
        genome_fa

rule gffread:
    input:
        genome = genome_fa, 
        gff = annotation_gff3 
    output:
        transcripts = f'{anno_outdir}/transcripts.fa',
        cds = f'{anno_outdir}/cds.fa',
        proteins =  f'{anno_outdir}/proteins.fa'
    shell:
        'gffread {input.gff} -g {input.genome} -w {output.transcripts} '
        '-x {output.cds} -y {output.proteins}'

# begin metadata
rule quast:
    input:
        genome_fa
    output:
        directory(f'{datpath}/{sp}/meta_collection/quast/geno')
    shell:
        'quast.py -o {output} {input}' 

rule count_gff:
    input:
        annotation_gff3
    output:
        f'{datpath}/{sp}/meta_collection/gff_features/counts.txt'
    shell:
        'cat {input}|grep -v "^#"|cut -f3|sort |uniq -c > {output}'

rule jellyfish:
    input:
        genome_fa
    output:
        tsv = f'{datpath}/{sp}/meta_collection/jellyfish/k{{k}}mer_counts.tsv',
        jf = f'{datpath}/{sp}/meta_collection/jellyfish/k{{k}}mer_counts.jf'
    wildcard_constraints:
        k = "[2-9]"  # would have to be fancier to allow larger k, but 0 or 1 is trouble
    shell:
        'jellyfish count -m {wildcards.k} -C -s 1000M -o {output.jf} {input};'
        "jellyfish dump {output.jf} |tr '\n' '\t' | sed 's/>/\\n/g' | grep '\w' > {output.tsv}"

rule onemers:
    input:
        genome_fa
    output:
        f'{datpath}/{sp}/meta_collection/jellyfish/k1mer_counts.tsv'
    shell:
        'python scripts/count_1mers.py {input} > {output}'


rule busco:
    input:
        fasta = busco_input
    output:
        directory(f'{datpath}/{sp}/meta_collection/busco/{{mode}}')
    shell:
        f'{run_BUSCO} -i {{input.fasta}} -o busco_{sp}_{{wildcards.mode}} -m {{wildcards.mode}} -l {lineage} -t tmp/busco_{sp}_{{wildcards.mode}}; '
        f'mv run_busco_{sp}_{{wildcards.mode}} {{output}}'
