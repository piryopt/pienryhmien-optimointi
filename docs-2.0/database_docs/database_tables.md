# Database tables
Basic explanations of the database tables. Self-explanatory items are left unexplained. 

## users
Contains the users' name and email data, as well as information on whether they have teacher or admin status. This data is obtained from the University of Helsinki login, while admin status has to be given by another admin.

Columns:
* name
* email
* isteacher (true/false)
* admin (true/false)
* language

## surveys
Contains the data of each individual survey, which are determined at the time of its creation. Surveys are closed either manually or when time_end has been reached. Search visibility allows for the filtering of choices based on their name. 

Columns:
* surveyname
* min_choices
* closed (true/false)
* results_saved (true/false)
* survey_description
* time_end
* allowed_denied_choices
* allow_search_visibility (true/false)
* deleted (true/false)

## survey_owners
Ties users to the surveys that they have ownership of. References **surveys** and **users**.

## survey_choices
Contains the data of each individiual choice in a survey. If mandatory is set to true, the group has to be filled to its minimum size. References **surveys**.

Columns:
* max_spaces
* deleted (true/false)
* min_size
* mandatory (true/false)

## choice_infos
Contains a dynamic amount of additional information of choices. This value can be set to hidden. References **survey_choices**.

Columns:
* info_key
* info_value
* hidden (true/false)

## user_survey_rankings
Contains the rankings of each group by the survey responder, as well as groups they have rejected and their reasoning for it. References **users** and **surveys**.

Columns:
* ranking
* rejections
* reason
* deleted (true/false)

## final_group
The final allocation of survey responders to their groups, and how they ranked the given group. References **users**, **surveys** and **survey_choices**.

## feedback
Contains data of user feedback. If the given feedback issue has been solved, it can be marked off as such. References **users**.

Columns:
* title
* type
* content
* solved (true/false)
