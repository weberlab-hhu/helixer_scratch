select cds_id, (cds_len - intron_len) from (	
	select t.id as cds_id, sum(abs(f.start - f.end)) as cds_len from transcript as t
	  join transcript_piece as tp
		on tp.transcript_id == t.id
	  join association_transcript_piece_to_feature as asso
		on asso.transcript_piece_id == tp.id
	  join feature as f
		on asso.feature_id == f.id
	 where t.super_locus_id = 6
	   and f.type = 'geenuff_cds'
	 group by t.id
	 order by sum(abs(f.start - f.end)) desc
    ) join (	 
	select t.id as intron_id, sum(abs(f.start - f.end)) as intron_len from transcript as t
	  join transcript_piece as tp
		on tp.transcript_id == t.id
	  join association_transcript_piece_to_feature as asso
		on asso.transcript_piece_id == tp.id
	  join feature as f
		on asso.feature_id == f.id
	 where t.super_locus_id = 6
	   and f.type = 'geenuff_intron'
	 group by t.id
	 order by sum(abs(f.start - f.end)) desc
   ) on cds_id = intron_id 
