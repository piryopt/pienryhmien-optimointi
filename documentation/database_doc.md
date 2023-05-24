# Database explanation
Somewhat informal explanation of database schema


## Users
Stores user data, entry created when user logs in for the first time with University of Helsinki account

## Courses
Courses that contain the surveys, created by teachers

## Surveys
A survey linked to a course, will be referenced by other tables. Created by teachers

## Choices
The actual places to be ranked, preschool etc. References a survey with survey_id

KNOWN ISSUE: VARIABLE SIZE OF EXTRA DATA. While a "normal" small group has a name and person responsible (2 text fields), preschool probably has more (+ address, age of children etc),
we need to find a way to fit all the needed data somehow

## Rankings
Stores users' survey selections based on priority. Big table, maybe a key based on course_id?
user_id - survey_id - choice_id - ranking
user A in survey B selected choice C with priority D

## Participants
List of participants on a course

## Final_group
Stores the result of the algorithm
course_id - user_id - survey_id - choice_id
In course A user B in survey C was placed in choice D 
