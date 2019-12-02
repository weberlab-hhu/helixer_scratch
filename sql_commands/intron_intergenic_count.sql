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
