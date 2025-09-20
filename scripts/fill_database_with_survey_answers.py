import random
from src.services.user_service import user_service
from src import db
from src.tools.db_tools import clear_database, generate_unique_id
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, String, TIMESTAMP, ForeignKey, text

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(Text)
	email = Column(Text, unique=True)
	isTeacher = Column(Boolean)
	admin = Column(Boolean)
	language = Column(Text)

class Survey(Base):
	__tablename__ = 'surveys'

	id = Column(String(10), primary_key=True, unique=True)
	name = Column(Text)
	min_choices = Column(Integer)
	closed = Column(Boolean)
	results_saved = Column(Boolean)
	survey_description = Column(Text)
	time_end = Column(TIMESTAMP)
	allowed_denied_choices = Column(Integer)
	allow_search_visibility = Column(Boolean)
	deleted = Column(Boolean)

class SurveyChoice(Base):
	__tablename__ = 'survey_choices'

	id = Column(Integer, primary_key=True)
	survey_id = Column(String(10), ForeignKey('surveys.id'))
	name = Column(Text)
	max_spaces = Column(Integer)
	deleted = Column(Boolean)
	min_size = Column(Integer)
	mandatory = Column(Boolean)

class UserSurveyRankings(Base):
	__tablename__ = 'user_survey_rankings'	
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	survey_id = Column(String(10), ForeignKey('surveys.id'))
	ranking = Column(Text)
	rejections = Column(Text)
	reason = Column(Text)
	deleted = Column(Boolean)

def add_survey_answers_to_db(survey_id, group_amount, student_amount):
	db.session.bulk_insert_mappings(
		UserSurveyRankings, 
		[{
			"user_id": i,
			"survey_id": survey_id,
			"ranking": ",".join([str(r) for r in random.sample(range(1, group_amount + 1), group_amount)]),
			"rejections": "",
			"reason": "",
			"deleted": False
,
		} for i in range(1, student_amount + 1)]
	)

def fill_database(group_amount, student_amount):
	clear_database()
	survey_id = generate_unique_id(10)
	add_survey_to_db(group_amount, survey_id)
	add_users_to_db(student_amount)
	add_teacher_for_survey(survey_id)
	add_groups_to_db(group_amount, survey_id)
	add_survey_answers_to_db(survey_id, group_amount, student_amount)
	db.session.commit()

def add_teacher_for_survey(survey_id):
	res = db.session.execute(
		text("""
			 INSERT INTO users 
			 	(id, name, email, isteacher, admin, language)
			 VALUES (999999999, 'opettaja', 'opettaja@mail.com', true, false, 'fi')
			 RETURNING id
			 """)
	)
	teacher_id = res.fetchone()[0]
	db.session.execute(
		text("INSERT INTO survey_owners (survey_id, user_id)" \
			"VALUES (:survey_id, :user_id)"),
		{"survey_id": survey_id, "user_id": teacher_id}
	)

def add_survey_to_db(group_amount, survey_id):
	survey_values = {
		"id": survey_id,
		"surveyname": "test survey",
		"min_choices": group_amount,
		"closed": False,
		"results_saved": False,
		"survey_description": "test description",
		"time_end": "2026-09-20 14:30:00",
		"allowed_denied_choices": 0,
		"allow_search_visibility": False,
		"deleted": False
	}
	db.session.execute(
		text("""
		INSERT INTO surveys (id, surveyname, min_choices,
		  closed, results_saved, survey_description,
		  time_end, allowed_denied_choices, 
		  allow_search_visibility, deleted)
		VALUES (:id, :surveyname, :min_choices, :closed,
		  :results_saved, :survey_description, :time_end,
		  :allowed_denied_choices, :allow_search_visibility,
		  :deleted)
		"""),
		survey_values
		)

def add_users_to_db(student_amount):
	db.session.bulk_insert_mappings(
		User, 
		[{
			"id": i,
			"name": f"user_{i}",
			"email": f"user_{i}@mail.com",
			"isteacher": False,
			"admin": False,
			"language": "fi"
		} for i in range(1, student_amount + 1)]
	)

def add_groups_to_db(group_amount, survey_id):
	db.session.bulk_insert_mappings(
		SurveyChoice, 
		[{
			"id": i,
			"survey_id": survey_id,
			"name": f"group_{i}",
			"max_spaces": 100,
			"deleted": False,
			"min_size": 1,
			"mandatory": False
		} for i in range(1, group_amount + 1)]
	)	

