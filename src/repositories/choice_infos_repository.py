from sqlalchemy import text
from src import db

class ChoiceInfosRepository:
    def create_new_choice_info(self, choice_id, info_key, info_value):
        '''
        Adds an additional to existing survey choice, updates choice_infos table
        '''
        sql = "INSERT INTO choice_infos (choice_id, info_key, info_value)"\
              " VALUES (:c_id, :i_key, :i_value)"
        result = db.session.execute(text(sql), {"c_id":choice_id, "i_key":info_key, "i_value":info_value})
        db.session.commit()

    def get_choice_additional_infos(self, choice_id):
        '''
        Gets a list of key-value pairs based on choice_id from choice_infos tables
        '''

        sql = "SELECT info_key, info_value FROM choice_infos WHERE choice_id=:choice_id"
        result = db.session.execute(text(sql), {"choice_id":choice_id})
        return result.fetchall()
    
choice_infos_repository = ChoiceInfosRepository()