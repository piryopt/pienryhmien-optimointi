# Database explanation
Somewhat informal explanation of the database schema

## users
Stores nescessary user data: Name, email, teacher status and admin status. Entry is created when the user logs in for the first time with University of Helsinki account. Name, email, and teacher/not teacher data is received from the login, admin status is automatically set to false.

## surveys
Surveys stores the survey id, name, description and other data that relates to a specific survey, not survey choices. Surveys are created by teachers.

## survey_teachers
Stores information on which teachers have access to surveys in the application. Stored data is pairs of teacher's user IDs and survey IDs

## survey_choices
The actual choices in a survey to be ranked, preschool etc. Contains names of the choices, maximum spaces, and references a survey with survey_id

## choice_infos
Contains additional information fields for survey choices, references choice_id and contains info key and value, key equals the column name shown for variable info fields in the choices table when editing a survey.

## user_survey_rankings
Stores users' survey selections based on priority, choice ids are presented in order with commas in between and in string format. If user has rejected a dhoice these are in the same format as ranking and reasoning presented by user is saved. references user and survey IDs.

## final_group
Stores the result of sorting students to groups. References user id, survey id and choice id, student in survey was placed in choice.

## feedback
Table stores feedback given by users after this functionality has been added to the application. References id of user who left the feedback and contains boolean on if the feedback is solved or not.
