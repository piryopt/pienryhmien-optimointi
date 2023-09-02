CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name TEXT,
	email TEXT UNIQUE,
	isteacher BOOLEAN,
	admin BOOLEAN
);

CREATE TABLE surveys ( -- yksittäinen kysely
	id VARCHAR(10) UNIQUE PRIMARY KEY,
	surveyname TEXT,
	min_choices INTEGER,
	closed BOOLEAN,
	results_saved BOOLEAN,
	survey_description TEXT,
	time_begin timestamp,
	time_end timestamp,
	allowed_denied_choices INTEGER,
	allow_search_visibility BOOLEAN,
	deleted BOOLEAN
);

CREATE TABLE survey_teachers (
	id SERIAL PRIMARY KEY,
	survey_id VARCHAR(10) REFERENCES surveys,
	teacher_id INTEGER REFERENCES users
);

CREATE TABLE survey_choices ( -- yksittäinen päiväkoti, pienryhmä
	id SERIAL PRIMARY KEY,
	survey_id VARCHAR(10) REFERENCES surveys,
	name TEXT,
	max_spaces INTEGER,
	deleted BOOLEAN
);

CREATE TABLE choice_infos ( -- dynamic amount of additional infos to choices
	id SERIAL PRIMARY KEY,
	choice_id INTEGER REFERENCES survey_choices,
	info_key TEXT,
	info_value TEXT,
	hidden BOOLEAN
);

CREATE TABLE user_survey_rankings (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	survey_id VARCHAR(10) REFERENCES surveys,
	ranking TEXT, -- e.g 1,2,5,3,4, the id's of survey_choices
	rejections TEXT, -- same format as ranking
	reason TEXT,
	deleted BOOLEAN
);

CREATE TABLE final_group ( -- lopullinen sijoitus
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	survey_id VARCHAR(10) REFERENCES surveys,
	choice_id INTEGER REFERENCES survey_choices
);

CREATE TABLE feedback (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	title TEXT,
	type TEXT,
	content TEXT,
	solved BOOLEAN
);

CREATE UNIQUE INDEX idx_user_survey_rankings_user_id_survey_id on user_survey_rankings (user_id,survey_id);