from src.repositories.choice_infos_repository import (
    choice_infos_repository as default_choice_infos_repository
)

class ChoiceInfosService:
    def __init__(self, choice_infos_repository = default_choice_infos_repository):
          self._choice_infos_repository = choice_infos_repository
          
    def get_choice_additional_infos(self, choice_id):
            return self._choice_infos_repository.get_choice_additional_infos(choice_id)
    
choice_infos_service = ChoiceInfosService()