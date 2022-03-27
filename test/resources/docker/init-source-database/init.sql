create schema if not exists test;

CREATE TABLE test.musician
(
    name       text    NOT NULL,
    surname   text    NOT NULL,
    age        integer NOT NULL,
    instrument text    NOT NULL
);

INSERT INTO test.musician (name, surname, age, instrument)
values ('kurt', 'cobain', 27, 'guitar');

INSERT INTO test.musician (name, surname, age, instrument)
values ('jim', 'morrison', 27, 'vocal');

INSERT INTO test.musician (name, surname, age, instrument)
values ('noel', 'gallagher', 54, 'guitar');

INSERT INTO test.musician (name, surname, age, instrument)
values ('kirk', 'hammett', 59, 'guitar');

INSERT INTO test.musician (name, surname, age, instrument)
values ('gene', 'simmons', 72, 'bass');

