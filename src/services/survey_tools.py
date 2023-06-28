'''Module for survey related functions'''
from sqlalchemy.sql import text
from src import db

class SurveyTools:
    '''Class for survey related functions'''

    def fetch_all_surveys():
        '''Returns a list of all surveys in the database'''
        sql = text("SELECT id, surveyname FROM surveys")
        result = db.session.execute(sql)
        all_surveys = result.fetchall()
        return all_surveys

    def fetch_survey_responses(survey):
        '''Returns a list of answers submitted to a certain survey'''
        sql = text ("SELECT user_id, ranking FROM user_survey_rankings " +
                    "WHERE survey_id=:survey AND deleted IS FALSE")
        result = db.session.execute(sql, {"survey":survey})
        responses = result.fetchall()
        return responses


    def fetch_surveys_and_answer_amounts():
        '''Returns a list of surveys and the amount of how many answers
        each of them have'''
        sql = text("SELECT surveys.id, surveys.surveyname, " +
                   "COUNT(user_survey_rankings.survey_id) " +
                   "AS answer_count FROM surveys JOIN user_survey_rankings " +
                   "ON surveys.id = user_survey_rankings.survey_id " +
                   "GROUP BY surveys.id, surveys.surveyname")
        result = db.session.execute(sql)
        all_surveys = result.fetchall()
        return all_surveys
