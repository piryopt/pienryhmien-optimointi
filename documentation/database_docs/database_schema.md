# Database tables explanation
Somewhat informal explanation of database schema


## users
Stores user data, entry created when user logs in for the first time with University of Helsinki AD account

## surveys
Contains name of the survey, by whom it was created, how many choices you have to rank in the least (maybe not needed but it's still there for now) and whether it's closed or not. Answers to closed surveys cannot be submitted. Will be referenced by other tables. Created by teachers

## survey_choices
The actual places to be ranked, data about the preschool or small group etc. References a survey with survey_id

Has only two required fields, name and how many spots does it have. Rest of the info is stored in the next table.

## choice_infos
This table contains all the non-required additional information about a choice. Format:

choice_id - key - value

Key and value are texts and can be anything, e.g. key can be postinumero (postal code) and value 00100 or the key can be ikäryhmä (age of children) and value 3-4v or whatever. One choice can have as many additional infos as is needed.


## user_survey_rankings
Stores users' survey selections based on priority.

user_id - survey_id - choice_id - ranking

user A in survey B selected choice C with priority D

e.g.

2 - 1 - 5 - 1

2 - 1 - 4 - 2

user id=2 in survey id=2 selected choice id=5 with priority 1

user id=2 in survey id=2 selected choice id=4 with priority 2


## final_group
Stores the result of the algorithm

user_id - survey_id - choice_id

User B in survey C was placed in choice D 
