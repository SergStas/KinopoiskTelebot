create table if not exists film
(
	id integer
		primary key,
	name text not null,
	year integer not null
);
create table if not exists genre
(
	id integer
		primary key,
	name text not null
);
create table if not exists genre_film
(
	genre_id integer not null
		references genre,
	film_id integer not null
		references film,
	constraint genre_film_pk
		primary key (genre_id, film_id)
);
create table if not exists  person
(
	id integer
		primary key,
	full_name text not null,
	start_year integer not null,
	end_year integer not null
);
create table if not exists colleague
(
	person_id1 integer not null
		references person,
	person_id2 integer not null
		references person,
	count_films integer not null,
	constraint colleague_pk
		primary key (person_id1, person_id2)
);
create table if not exists person_film
(
	person_id integer not null
		references person,
	film_id integer not null
		references film,
	constraint person_film_pk
		primary key (person_id, film_id)
);
create table if not exists position
(
	id integer
		primary key,
	name text not null
);
create table if not exists person_position_film
(
	person_id integer not null
		references person,
	position_id integer not null
		references position,
	film_id integer not null
	    references film,
	constraint person_pk
		primary key (position_id, person_id, film_id)
);