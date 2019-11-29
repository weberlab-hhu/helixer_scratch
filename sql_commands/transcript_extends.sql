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

SELECT coordinate.seqid, min(feature.end) + 1, max(feature.start) + 1, count(distinct(transcript.id)) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
CROSS JOIN association_transcript_piece_to_feature ON association_transcript_piece_to_feature.feature_id = feature.id
CROSS JOIN transcript_piece ON association_transcript_piece_to_feature.transcript_piece_id = transcript_piece.id
CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE genome.species IN ('Athaliana') AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
	AND feature.type = 'geenuff_transcript' AND feature.is_plus_strand = 0
GROUP BY super_locus.id
ORDER BY count(distinct(transcript.id)) DESC
LIMIT 10;

