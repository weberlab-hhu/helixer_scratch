select super_locus_id, given_name, count(id) from (
	select distinct t.super_locus_id, sl.given_name, t.id from transcript as t
	  join super_locus as sl
	    on t.super_locus_id = sl.id
	  join transcript_piece as tp
		on tp.transcript_id == t.id
	  join association_transcript_piece_to_feature as asso
		on asso.transcript_piece_id == tp.id
	  join feature as f
		on asso.feature_id == f.id
	  join coordinate as c
		on f.coordinate_id == c.id
	  join genome as g
		on c.genome_id = g.id
	 where g.species = 'Athaliana'
	 order by c.id)
group by super_locus_id
