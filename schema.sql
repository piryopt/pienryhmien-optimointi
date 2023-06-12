CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstname TEXT,
 	lastname TEXT,
 	student_number TEXT, -- or int or not at all
	email TEXT,
	isteacher BOOLEAN
);

CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
	coursename TEXT UNIQUE,
	teacher_id INTEGER REFERENCES users -- maybe not needed
);

CREATE TABLE surveys ( -- yksittäinen kysely
	id SERIAL PRIMARY KEY,
	groupname TEXT,
	course_id INTEGER REFERENCES courses,
	min_choices INTEGER
);

CREATE TABLE choices ( -- yksittäinen päiväkoti, pienryhmä
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	survey_id INTEGER REFERENCES surveys,
	name TEXT,
	max_spaces INTEGER,
	current_spaces INTEGER,
	info1 TEXT,
	info2 TEXT
);

CREATE TABLE rankings (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	survey_id INTEGER REFERENCES surveys,
	choice_id INTEGER REFERENCES choices,
	ranking INTEGER
);

CREATE TABLE participants (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	user_id INTEGER REFERENCES users,
	privileged BOOLEAN
);

CREATE TABLE final_group ( -- lopullinen sijoitus
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	user_id INTEGER REFERENCES users,
	survey_id INTEGER REFERENCES surveys,
	choice_id INTEGER REFERENCES choices
);

