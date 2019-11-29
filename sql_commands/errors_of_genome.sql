SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE feature.type IN ('missing_utr_5p', 'empty_super_locus', 'missing_start_codon',
					   'missing_stop_codon', 'wrong_starting_phase', 'mismatched_ending_phase',
					   'overlapping_exons', 'too_short_intron', 'super_loci_overlap_error')
	AND genome.species IN ('Creinhardtii');


SELECT count(feature.id) FROM genome
CROSS JOIN coordinate ON coordinate.genome_id = genome.id AND genome.species IN ('Creinhardtii')
CROSS JOIN feature ON feature.coordinate_id = coordinate.id
WHERE feature.type IN ('missing_utr_5p', 'empty_super_locus', 'missing_start_codon',
					   'missing_stop_codon', 'wrong_starting_phase', 'mismatched_ending_phase',
					   'overlapping_exons', 'too_short_intron', 'super_loci_overlap_error');


SELECT count(feature.id) FROM feature
JOIN coordinate ON feature.coordinate_id = coordinate.id
JOIN genome ON genome.id = coordinate.genome_id
WHERE genome.species IN ('Creinhardtii');
