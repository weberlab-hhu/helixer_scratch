--number of genes per genome
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

--number of transcripts per genome
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

--genome sizes and fragmentation
SELECT genome.species, sum(coordinate.length) / 1000000000.0 as total_length, count(coordinate.id) as n_fragments FROM coordinate
JOIN genome on coordinate.genome_id = genome.id
GROUP BY genome.id
ORDER BY sum(coordinate.length) DESC;

--all super loci with their number of transcripts for one genome
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

--average number of transcripts per super loci for all genomes
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



SELECT feature.id FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND coordinate.id IN (
	SELECT DISTINCT feature.coordinate_id AS feature_coordinate_id
	FROM feature
)
AND genome.species IN ('Olucimarinus')
ORDER BY genome.species, coordinate.length DESC;




SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Olucimarinus')
ORDER BY genome.species, coordinate.length DESC;

SELECT count(feature.id) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE transcript.longest = 1 AND genome.species IN ('gallus_gallus') and super_locus.type = 'gene' and transcript.type = 'mRNA'
ORDER BY genome.species, coordinate.length DESC;

SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE transcript.longest = 1 AND genome.species IN ('gallus_gallus') and super_locus.type = 'gene' and transcript.type = 'mRNA'
ORDER BY genome.species, coordinate.length DESC;

SELECT feature.id AS feature_id, feature.given_name AS feature_given_name, feature.type AS feature_type, feature.start AS feature_start, feature.start_is_biological_start AS feature_start_is_biological_start, feature."end" AS feature_end, feature.end_is_biological_end AS feature_end_is_biological_end, feature.is_plus_strand AS feature_is_plus_strand, feature.score AS feature_score, feature.source AS feature_source, feature.phase AS feature_phase, feature.coordinate_id AS feature_coordinate_id, coordinate.id AS coordinate_id, coordinate.length AS coordinate_length, coordinate.genome_id AS coordinate_genome_id
FROM feature JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('caenorhabditis_elegans') and super_locus.type = 'gene' and transcript.type = 'mRNA'
ORDER BY genome.species, coordinate.length DESC;

SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('MpusillaCCMP1545')
ORDER BY genome.species, coordinate.length DESC;

SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana')
ORDER BY genome.species, coordinate.length DESC;




SELECT genome.species, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
GROUP BY genome.id
ORDER BY count(feature.id)




SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana')
GROUP BY feature.type;

SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Athaliana')
GROUP BY feature.type;

SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Gmax')
GROUP BY feature.type;

SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Olucimarinus')
GROUP BY feature.type;

SELECT feature.type, count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Athaliana') AND super_locus.given_name == 'AT5G06750.TAIR10' and transcript.longest == 1
GROUP BY feature.type;



SELECT feature.start, feature.end, coordinate.seqid FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Gmax') and feature.type == 'too_short_intron'
ORDER BY seqid, feature.start;



explain query plan SELECT feature.id AS feature_id, feature.given_name AS feature_given_name, feature.type AS feature_type, feature.start AS feature_start, feature.start_is_biological_start AS feature_start_is_biological_start, feature."end" AS feature_end, feature.end_is_biological_end AS feature_end_is_biological_end, feature.is_plus_strand AS feature_is_plus_strand, feature.score AS feature_score, feature.source AS feature_source, feature.phase AS feature_phase, feature.coordinate_id AS feature_coordinate_id, coordinate.id AS coordinate_id, coordinate.length AS coordinate_length, coordinate.genome_id AS coordinate_genome_id
FROM feature JOIN coordinate ON feature.coordinate_id = coordinate.id JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id JOIN transcript ON transcript_piece.transcript_id = transcript.id JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana', 'Bdistachyon', 'Creinhardtii', 'Gmax', 'Mguttatus', 'Mpolymorpha', 'Ptrichocarpa', 'Sitalica')
ORDER BY genome.species, coordinate.length desc;

SELECT count(feature.id)
FROM feature JOIN coordinate ON feature.coordinate_id = coordinate.id JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id JOIN transcript ON transcript_piece.transcript_id = transcript.id JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana', 'Bdistachyon', 'Creinhardtii', 'Gmax', 'Mguttatus', 'Mpolymorpha', 'Ptrichocarpa', 'Sitalica')
ORDER BY genome.species, coordinate.length desc;

SELECT count(feature.id)
FROM feature JOIN coordinate ON feature.coordinate_id = coordinate.id JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id JOIN transcript ON transcript_piece.transcript_id = transcript.id JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana', 'Bdistachyon', 'Creinhardtii', 'Gmax')
ORDER BY genome.species, coordinate.length desc;


explain query plan SELECT count(feature.id)
FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana', 'Creinhardtii')
ORDER BY genome.species, coordinate.length desc;

SELECT count(feature.id)
FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana', 'Creinhardtii')
ORDER BY genome.species, coordinate.length desc;


explain query plan SELECT count(feature.id)
FROM feature JOIN coordinate ON feature.coordinate_id = coordinate.id JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id JOIN transcript ON transcript_piece.transcript_id = transcript.id JOIN genome ON genome.id = coordinate.genome_id
WHERE transcript.longest = 1 AND genome.species IN ('Athaliana')
ORDER BY genome.species, coordinate.length desc;
