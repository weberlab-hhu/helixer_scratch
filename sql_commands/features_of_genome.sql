-- number of genes per genome
SELECT genome.species, count(distinct(super_locus.id)) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and transcript.longest = 1
GROUP BY genome.id
ORDER BY count(super_locus.id) DESC;

-- number of transcripts per genome
SELECT genome.species, count(distinct(transcript.id)) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA'
GROUP BY genome.id
ORDER BY count(transcript.id) DESC;

-- genome sizes and fragmentation
SELECT genome.species, sum(coordinate.length) / 1000000000.0 as total_length, count(coordinate.id) as n_fragments FROM coordinate
JOIN genome on coordinate.genome_id = genome.id
GROUP BY genome.id
ORDER BY sum(coordinate.length) DESC;

-- length of genes
SELECT genome.species, coordinate.seqid, abs(feature.start - feature.end) len_longest_transcript FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and transcript.longest = 1 and feature.type = 'geenuff_transcript';

-- average length of longest transcripts grouped by genome
SELECT genome.species, round(avg(abs(feature.start - feature.end))) avg_transcript_length from feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and transcript.longest = 1 and feature.type = 'geenuff_transcript'
GROUP BY genome.id
ORDER BY round(avg(abs(feature.start - feature.end))) DESC;

-- all super loci with their number of transcripts for one genome
SELECT super_locus.given_name, count(distinct(transcript.id)) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and genome.species = 'Athaliana'
GROUP BY super_locus.id
ORDER BY count(distinct(transcript.id)) DESC
LIMIT 100;

-- average number of transcripts per super loci for all genomes
SELECT genome.species, count(distinct(transcript.id)) * 1.0 / count(distinct(super_locus.id)) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA'
GROUP BY genome.id
ORDER BY count(distinct(transcript.id)) DESC
LIMIT 100;

-- features of a gene
SELECT start, end, feature.type FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus on transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and super_locus.given_name = 'AT1G01073.TAIR10'
ORDER BY feature.type, start;

-- too short intron errors by species
SELECT genome.species, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE feature.type == 'geenuff_intron' and abs(feature.start - feature.end) < 60
GROUP BY genome.id
ORDER BY count(feature.id);

-- feature count by species
SELECT genome.species, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
GROUP BY genome.id
ORDER BY count(feature.id)

-- feature types of one coordinate
SELECT start, end, feature.type FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
WHERE coordinate.seqid = '1' and feature.is_plus_strand = 1;

-- feature type counts for one genome
SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana')
GROUP BY feature.type;

-- super loci of coordinate
SELECT distinct(super_locus.id) from feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE coordinate.seqid = 'Contig28439';

-- transcript of super loci
SELECT distinct(transcript.id) from feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE super_locus.id = 3005484;

-- transcript_pieces of super loci
SELECT distinct(transcript_piece.id) from feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE super_locus.id = 3005484;

-- overreaching features
SELECT species, seqid, coordinate.length, super_locus.id, feature.type, feature.is_plus_strand, feature.start, feature.end, transcript.id, transcript.type, transcript.given_name from feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' AND transcript.type = 'mRNA' AND transcript.longest = 1 and genome.species = 'ornithorhynchus_anatinus'
and feature.type = 'geenuff_transcript'
and ((feature.is_plus_strand = 1 and feature.end > coordinate.length + 1) or
       (feature.is_plus_strand = 0 and feature.start + 1 > coordinate.length));

-- average intron length per genome
SELECT genome.species, avg(abs(feature.start - feature.end)) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE super_locus.type = 'gene' AND transcript.type = 'mRNA' AND transcript.longest = 1
	AND feature.type = 'geenuff_intron'
GROUP BY genome.id
ORDER BY avg(abs(feature.start - feature.end)) DESC;

-- intron proportion
SELECT species, sum(intron_sum), sum(length), sum(intron_sum) * 1.0 / sum(length) FROM (
	SELECT genome.species, sum(abs(feature.start - feature.end)) as intron_sum, coordinate.length FROM feature
	JOIN coordinate ON feature.coordinate_id = coordinate.id
	JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
	JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
	JOIN transcript ON transcript_piece.transcript_id = transcript.id
	JOIN genome ON genome.id = coordinate.genome_id
	JOIN super_locus on transcript.super_locus_id = super_locus.id
	WHERE super_locus.type = 'gene' and transcript.type = 'mRNA' and transcript.longest = 1 and feature.type = 'geenuff_intron'
	GROUP BY coordinate.id
)
GROUP BY species;

-- gene extends plus strand
SELECT coordinate.seqid, min(feature.start), max(feature.end), count(distinct(transcript.id)) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE genome.species IN ('Athaliana') AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
	AND feature.type = 'geenuff_transcript' AND feature.is_plus_strand = 1
GROUP BY super_locus.id;

-- gene extends minus strand (with flipped start/end)
SELECT coordinate.seqid, min(feature.end) + 1, max(feature.start) + 1, count(distinct(transcript.id)) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE genome.species IN ('Athaliana') AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
	AND feature.type = 'geenuff_transcript' AND feature.is_plus_strand = 0
GROUP BY super_locus.id;
