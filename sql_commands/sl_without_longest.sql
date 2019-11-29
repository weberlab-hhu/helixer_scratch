select sl.id, sl.given_name from super_locus as sl
 where sl.id not in (
	select distinct t.super_locus_id from transcript as t
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
	 where t.longest
)
	 
