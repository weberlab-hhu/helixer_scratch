SELECT feature.id AS feature_id,
                              feature.given_name AS feature_given_name,
                              feature.type AS feature_type,
                              feature.start AS feature_start,
                              feature.start_is_biological_start AS feature_start_is_biological_start,
                              feature."end" AS feature_end,
                              feature.end_is_biological_end AS feature_end_is_biological_end,
                              feature.is_plus_strand AS feature_is_plus_strand,
                              feature.score AS feature_score,
                              feature.source AS feature_source,
                              feature.phase AS feature_phase,
                              feature.coordinate_id AS feature_coordinate_id,
                              coordinate.id AS coordinate_id,
                              coordinate.length AS coordinate_length,
                              coordinate.genome_id AS coordinate_genome_id
                       FROM genome
                       CROSS JOIN coordinate ON coordinate.genome_id = genome.id
                       CROSS JOIN feature ON feature.coordinate_id = coordinate.id
                       CROSS JOIN association_transcript_piece_to_feature
                           ON association_transcript_piece_to_feature.feature_id = feature.id
                       CROSS JOIN transcript_piece
                           ON association_transcript_piece_to_feature.transcript_piece_id =
                           transcript_piece.id
                       CROSS JOIN transcript ON transcript_piece.transcript_id = transcript.id
                       CROSS JOIN super_locus ON transcript.super_locus_id = super_locus.id
                       WHERE transcript.longest = 1 AND genome.species IN ("ciona_savignyi")
                           AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
                       ORDER BY genome.species;

explain query plan SELECT feature.id ,
                              feature.given_name AS feature_given_name,
                              feature.type AS feature_type,
                              feature.start AS feature_start,
                              feature.start_is_biological_start AS feature_start_is_biological_start,
                              feature."end" AS feature_end,
                              feature.end_is_biological_end AS feature_end_is_biological_end,
                              feature.is_plus_strand AS feature_is_plus_strand,
                              feature.score AS feature_score,
                              feature.source AS feature_source,
                              feature.phase AS feature_phase,
                              feature.coordinate_id AS feature_coordinate_id,
                              coordinate.id AS coordinate_id,
                              coordinate.genome_id AS coordinate_genome_id
FROM genome
JOIN coordinate ON coordinate.genome_id = genome.id
JOIN feature ON feature.coordinate_id = coordinate.id
JOIN association_transcript_piece_to_feature
   ON association_transcript_piece_to_feature.feature_id = feature.id
JOIN transcript_piece
   ON association_transcript_piece_to_feature.transcript_piece_id =
   transcript_piece.id
JOIN transcript ON transcript_piece.transcript_id = transcript.id
JOIN super_locus ON transcript.super_locus_id = super_locus.id
WHERE transcript.longest = 1 AND genome.species IN ("ciona_savignyi")
   AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
ORDER BY genome.species;


explain query plan SELECT feature.id AS feature_id,
                              feature.given_name AS feature_given_name,
                              feature.type AS feature_type,
                              feature.start AS feature_start,
                              feature.start_is_biological_start AS feature_start_is_biological_start,
                              feature."end" AS feature_end,
                              feature.end_is_biological_end AS feature_end_is_biological_end,
                              feature.is_plus_strand AS feature_is_plus_strand,
                              feature.score AS feature_score,
                              feature.source AS feature_source,
                              feature.phase AS feature_phase,
                              feature.coordinate_id AS feature_coordinate_id,
                              coordinate.id AS coordinate_id,
                              coordinate.length AS coordinate_length,
                              coordinate.genome_id AS coordinate_genome_id
                       FROM genome
                       JOIN coordinate ON coordinate.genome_id = genome.id
                       JOIN feature ON feature.coordinate_id = coordinate.id
                       JOIN association_transcript_piece_to_feature
                           ON association_transcript_piece_to_feature.feature_id = feature.id
                       JOIN transcript_piece
                           ON association_transcript_piece_to_feature.transcript_piece_id =
                           transcript_piece.id
                       JOIN transcript ON transcript_piece.transcript_id = transcript.id
                       JOIN super_locus ON transcript.super_locus_id = super_locus.id
                       WHERE transcript.longest = 1 AND genome.species IN ("ciona_savignyi")
                           AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
                       ORDER BY genome.species;

SELECT feature.id AS feature_id,
                              feature.given_name AS feature_given_name,
                              feature.type AS feature_type,
                              feature.start AS feature_start,
                              feature.start_is_biological_start AS feature_start_is_biological_start,
                              feature."end" AS feature_end,
                              feature.end_is_biological_end AS feature_end_is_biological_end,
                              feature.is_plus_strand AS feature_is_plus_strand,
                              feature.score AS feature_score,
                              feature.source AS feature_source,
                              feature.phase AS feature_phase,
                              feature.coordinate_id AS feature_coordinate_id,
                              coordinate.id AS coordinate_id,
                              coordinate.length AS coordinate_length,
                              coordinate.genome_id AS coordinate_genome_id
                       FROM genome
                       JOIN coordinate ON coordinate.genome_id = genome.id
                       JOIN feature ON feature.coordinate_id = coordinate.id
                       JOIN association_transcript_piece_to_feature
                           ON association_transcript_piece_to_feature.feature_id = feature.id
                       JOIN transcript_piece
                           ON association_transcript_piece_to_feature.transcript_piece_id =
                           transcript_piece.id
                       JOIN transcript ON transcript_piece.transcript_id = transcript.id
                       JOIN super_locus ON transcript.super_locus_id = super_locus.id
                       WHERE transcript.longest = 1 AND genome.species IN ("ciona_savignyi")
                           AND super_locus.type = 'gene' AND transcript.type = 'mRNA'
                       ORDER BY genome.species;
