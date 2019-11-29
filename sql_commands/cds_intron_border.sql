drop table cds_intron_tmp;
create table cds_intron_tmp (id integer not null, t_id integer not null, start integer not null, end integer not null, primary key(id));

insert into cds_intron_tmp (id, t_id, start, end) select f2.id, t2.id as t_id, f2.start, f2.end
    from feature as f2
    join coordinate as c2
    on f2.coordinate_id = c2.id and f2.type = 'geenuff_intron'
    join genome as g2
    on c2.genome_id = g2.id and g2.species in ('Athaliana','Bdistachyon','Creinhardtii','Gmax','Mguttatus','Mpolymorpha','Ptrichocarpa','Sitalica')
    join association_transcript_piece_to_feature as asso2
    on asso2.feature_id == f2.id
    join transcript_piece as tp2
    on asso2.transcript_piece_id = tp2.id
    join transcript as t2
    on tp2.transcript_id = t2.id and t2.longest = 1;

--select f1.id as f1_id, f2.id as f2_id, f1.end, f2.start, f1.start, f2.end, g.species, c.id as c_id, t.id as t_id, t.given_name
select g.species, count(g.id)
from feature as f1
join coordinate as c
on f1.coordinate_id = c.id and f1.type = 'geenuff_cds'
join genome as g
on c.genome_id = g.id and g.species in ('Athaliana','Bdistachyon','Creinhardtii','Gmax','Mguttatus','Mpolymorpha','Ptrichocarpa','Sitalica')
join association_transcript_piece_to_feature as asso
on asso.feature_id == f1.id
join transcript_piece as tp
on asso.transcript_piece_id = tp.id
join transcript as t
on tp.transcript_id = t.id and t.longest = 1
join cds_intron_tmp as f2
on t.id = f2.t_id and (f1.end = f2.start or f1.start = f2.end)
group by g.id
order by g.species;

drop table cds_intron_tmp;
