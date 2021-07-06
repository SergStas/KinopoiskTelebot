create table if not exists genre
(
	id integer primary key,
	name text not null
);
create table if not exists  person
(
	id integer primary key,
	full_name text not null,
	photo_url text not null
);
create table if not exists params
(
    id integer primary key,
    person_id integer not null
        references person,
    start_year integer not null,
    end_year integer not null,
    threshold integer not null,
    is_actor integer not null
);
create table if not exists colleague
(
	person_id1 integer not null
		references person,
	person_id2 integer not null
		references person,
	params_id integer not null
        references params,
	count_films integer not null,
	constraint colleague_pk
		primary key (person_id1, person_id2, params_id)
);
create table if not exists params_genre
(
    genre_id integer not null
        references genre,
    params_id integer not null
        references params,
    constraint params_genre_pk
        primary key (genre_id, params_id)
);
create table  if not exists user_type
(
    id integer primary key,
    name text not null
);
create table  if not exists user
(
    id integer primary key,
    strat_date_use text not null,
    date_last_visit text not null,
    user_type_id number not null
        references user_type
);
create table if not exists req
(
    id integer not null,
    user_id integer not null
        references user,
    params_id integer not null
        references params,
    constraint req_pk
        primary key (id, user_id)
);
create table if not exists fav
(
    req_id integer not null
        references req,
    req_user_id integer not null
        references req,
    constraint fav_pk
        primary key (req_id, req_user_id)
);

