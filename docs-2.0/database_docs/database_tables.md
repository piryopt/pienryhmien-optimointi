# Database tables

Basic explanations of the database tables. Self-explanatory items are left unexplained.

## users

Contains the users' name and email data, as well as information on whether they have teacher or admin status. This data is obtained from the University of Helsinki login, while admin status has to be given by another admin. Language column is now an old unused column.

Columns:

- name
- email
- isteacher (true/false)
- admin (true/false)
- language

## surveys

Contains the data of each individual survey, which are determined at the time of its creation. Surveys are closed either manually or when time_end has been reached. Search visibility field was used to allow searching for a group when answering a survey. Now this feature is always allowed making this column unused. Column deleted_at is used to permanently delete surveys that have been set as deleted.

Columns:

- surveyname
- min_choices
- min_choices_per_stage
- closed (true/false)
- results_saved (true/false)
- survey_description
- time_end
- allowed_denied_choices
- allow_search_visibility (true/false)
- deleted (true/false)
- deleted_at

## survey_owners

Ties users to the surveys that they have ownership of. References **surveys** and **users**.

## survey_choices

Contains the data of each individiual choice in a survey. If mandatory is set to true, the group has to be filled to its minimum size. The column participation_limit allows for a maximum limit a user can be placed to a certain group within a multistage survey. References **surveys**.

Columns:

- max_spaces
- deleted (true/false)
- min_size
- mandatory (true/false)
- participation_limit

## survey_stages

This table is used within a multistage survey to connect a survey, a survey_choice (group) and stage. The column order_number is used to ensure the stages are in correct order when fetched from the database and displayed in the frontend.

Columns:

- survey_id
- choice_id
- stage
- order_numer
- (survey_id, choice_id, stage) primary key

## choice_infos

Contains a dynamic amount of additional information of choices. This value can be set to hidden. References **survey_choices**.

Columns:

- id
- choice_id
- info_key
- info_value
- hidden (true/false)

## user_survey_rankings

Contains the rankings of each group by the survey responder, as well as groups they have rejected and their reasoning for it. Stage tells which stage of the survey the ranking is related to. The column not_available allows users to set themselves as absent in a stage of a survey. References **users** and **surveys**.

Columns:

- user_id
- survey_id
- ranking
- rejections
- reason
- deleted (true/false)
- stage
- not_available

## final_group

The final allocation of survey responders to their groups, and how they ranked the given group. References **users**, **surveys** and **survey_choices**.

## feedback

Contains data of user feedback. If the given feedback issue has been solved, it can be marked off as such. References **users**.

Columns:

- title
- type
- content
- solved (true/false)

## Statistics

This table allows for saving of the application statistics such as total number of created surveys. The application should always have one row marked as current row (is_current_row = TRUE). This row is then updated with every action that should update the statistics. This current row is displayed in the application admin statistics. The other rows are weekly-saved backups/history data with is_current_row = FALSE. This approach allows statistics with permanently deleted surveys.

Columns:

- total_created_surveys
- active_surveys_count
- registered_teachers_count
- registered_students_count
- total_survey_answers
- is_current_row
- updated_at
