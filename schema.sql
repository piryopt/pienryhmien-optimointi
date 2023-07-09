CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name TEXT,
 	student_number TEXT, -- or int or not at all
	email TEXT,
	isteacher BOOLEAN
);

CREATE TABLE surveys ( -- yksittäinen kysely
	id SERIAL PRIMARY KEY,
	surveyname TEXT,
	teacher_id INTEGER REFERENCES users,
	min_choices INTEGER,
	closed BOOLEAN 
);

CREATE TABLE survey_choices ( -- yksittäinen päiväkoti, pienryhmä
	id SERIAL PRIMARY KEY,
	survey_id INTEGER REFERENCES surveys,
	name TEXT,
	max_spaces INTEGER
);

CREATE TABLE choice_infos ( -- dynamic amount of additional infos to choices
	id SERIAL PRIMARY KEY,
	choice_id INTEGER REFERENCES survey_choices,
	info_key TEXT,
	info_value TEXT
);

CREATE TABLE user_survey_rankings (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	survey_id INTEGER REFERENCES surveys,
	ranking TEXT, -- e.g 1,2,5,3,4, the id's of survey_choices
	deleted BOOLEAN
);

CREATE TABLE final_group ( -- lopullinen sijoitus
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	survey_id INTEGER REFERENCES surveys,
	choice_id INTEGER REFERENCES survey_choices
);

CREATE UNIQUE INDEX idx_user_survey_rankings_user_id_survey_id on user_survey_rankings (user_id,survey_id);