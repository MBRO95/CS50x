select title from movies where id in (select movie_id from stars where person_id = (select id from people where name = "Bradley Cooper") INTERSECT select movie_id from stars where person_id = (select id from people where name = "Jennifer Lawrence"));
