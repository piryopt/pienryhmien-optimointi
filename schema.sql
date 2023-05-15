CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstname TEXT,
 	lastname TEXT,
	isteacher BOOLEAN
);

CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
	coursename TEXT UNIQUE,
	teacher_id INTEGER REFERENCES users
);

CREATE TABLE groups (
	id SERIAL PRIMARY KEY,
	groupname TEXT,
	course_id INTEGER REFERENCES courses
);

CREATE TABLE choices (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	name TEXT,
	max_spaces INTEGER,
	current_spaces INTEGER,
	info1 TEXT,
	info2 TEXT
);

CREATE TABLE rankings (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	group_id INTEGER REFERENCES groups,
	choice_id INTEGER REFERENCES choices,
	ranking INTEGER
);

CREATE TABLE participants (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	user_id INTEGER REFERENCES users	
);

CREATE TABLE user_group (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	user_id INTEGER REFERENCES users,
	group_id INTEGER REFERENCES groups
);

USERS lisätän entry, kun käyttäjä kirjautuu ensimmäistä kertaa sisään.

COURSES opettaja voi lisätä kurssin

GROUPS kysely, liittyy tiettyyn kurssiin

CHOICES kyselyyn liittyvä pienryhmä/päiväkoti yms. sisältää tiedon käyttäjien määrästä ja kaksi lisätietokenttää (esim osoite ja ikäryhmä)

RANKINGS iso taulu, käyttäjän id - kyselyn id - valinnan id - valittu tärkeys

PARTICIPANTS pääse näkemään kurssille osallistujat

USER_GROUP lopullinen sijoitus
