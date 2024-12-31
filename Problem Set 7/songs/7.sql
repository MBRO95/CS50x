select avg(energy) from (select * from songs where artist_id = (select id from artists where name = "Drake"));
