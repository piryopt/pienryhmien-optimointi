ALTER TABLE surveys
    ADD COLUMN allow_absences BOOLEAN DEFAULT FALSE;


ALTER TABLE survey_owners
    DROP CONSTRAINT survey_owners_survey_id_fkey;

ALTER TABLE survey_owners
    ADD CONSTRAINT survey_owners_survey_id_fkey
        FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE;

ALTER TABLE survey_choices
    DROP CONSTRAINT survey_choices_survey_id_fkey;

ALTER TABLE survey_choices
    ADD COLUMN participation_limit INTEGER DEFAULT 0;

ALTER TABLE survey_choices
    ADD CONSTRAINT survey_choices_survey_id_fkey
        FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE;

CREATE TABLE survey_stages (
    survey_id VARCHAR(10) REFERENCES surveys,
    choice_id INTEGER REFERENCES survey_choices,
    stage TEXT NOT NULL,
    order_number INTEGER,
    PRIMARY KEY (survey_id, choice_id, stage)
);

ALTER TABLE choice_infos
    DROP CONSTRAINT choice_infos_choice_id_fkey;

ALTER TABLE choice_infos
    ADD CONSTRAINT choice_infos_choice_id_fkey
        FOREIGN KEY (choice_id) REFERENCES survey_choices(id) ON DELETE CASCADE;

ALTER TABLE user_survey_rankings
    DROP CONSTRAINT user_survey_rankings_survey_id_fkey;

ALTER TABLE user_survey_rankings
    ADD COLUMN stage TEXT DEFAULT NULL,
    ADD COLUMN not_available BOOLEAN DEFAULT NULL;

ALTER TABLE user_survey_rankings
    ADD CONSTRAINT user_survey_rankings_survey_id_fkey
        FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE;

DROP INDEX IF EXISTS idx_user_survey_rankings_user_id_survey_id;

CREATE UNIQUE INDEX idx_user_survey_rankings_user_id_survey_id_stage
ON user_survey_rankings (user_id, survey_id, stage);

ALTER TABLE final_group
    DROP CONSTRAINT final_group_survey_id_fkey,
    DROP CONSTRAINT final_group_choice_id_fkey;

ALTER TABLE final_group
    ADD CONSTRAINT final_group_survey_id_fkey
        FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,
    ADD CONSTRAINT final_group_choice_id_fkey
        FOREIGN KEY (choice_id) REFERENCES survey_choices(id) ON DELETE CASCADE;

ALTER TABLE surveys
    ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;

ALTER TABLE surveys ADD COLUMN min_choices_per_stage JSONB DEFAULT NULL;

ALTER TABLE surveys
ALTER COLUMN min_choices SET DEFAULT NULL;

ALTER TABLE survey_stages
    DROP CONSTRAINT survey_stages_survey_id_fkey,
    DROP CONSTRAINT survey_stages_choice_id_fkey;

ALTER TABLE survey_stages
    ADD CONSTRAINT survey_stages_survey_id_fkey
        FOREIGN KEY (survey_id)
        REFERENCES surveys(id)
        ON DELETE CASCADE,
    ADD CONSTRAINT survey_stages_choice_id_fkey
        FOREIGN KEY (choice_id)
        REFERENCES survey_choices(id)
        ON DELETE CASCADE;

-- These have to be added to prod db before merging the changes
-- CREATE TABLE statistics ( -- One row that is updated, others for (weekly?) history/backups
--	id SERIAL PRIMARY KEY,
--	total_created_surveys INTEGER,
--	active_surveys_count INTEGER,
--	registered_teachers_count INTEGER,
--	registered_students_count INTEGER,
--	total_survey_answers INTEGER,
--	is_current_row BOOLEAN,
--	updated_at TIMESTAMP DEFAULT NOW()
--);

-- INSERT INTO statistics (total_created_surveys, active_surveys_count, registered_teachers_count,
-- registered_students_count, total_survey_answers, is_current_row) VALUES (<VAL FROM PROD>, <VAL FROM PROD>,
-- <VAL FROM PROD>, <VAL FROM PROD>, <VAL FROM PROD>, TRUE);
