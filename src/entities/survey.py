from dataclasses import dataclass
from typing import List, Any

@dataclass
class Survey:
    id: int
    surveyname: str
    teacher_id: int
    min_choices: int
    results_saved: bool
    survey_description: str
    choices: List[Any]

@dataclass
class SurveyChoice:
    id: int
    survey_id: int
    name: str
    max_spaces: int
    info_columns: List[Any]

@dataclass
class SurveyChoiceInfo:
    id: int
    choice_id: int
    info_key: str
    info_value: str


MOCK_SURVEY = Survey(
    id = 1337,
    surveyname = "Mock Survey Entry",
    teacher_id = 734,
    min_choices = 8,
    results_saved = False,
    survey_description = "This is a sample survey to test Survey-objects",
    choices = [
        SurveyChoice(id=1, survey_id=734, name="Ensimmäinen valinta", max_spaces=8, info_columns=[
            SurveyChoiceInfo(id=1, choice_id=1, info_key="Kuvaus", info_value="Tosi kiva valinta, ensimmäinen sellainen"),
            SurveyChoiceInfo(id=2, choice_id=1, info_key="Osoite", info_value="Ekatie 1, 00100 Helsinki")
        ]),
        SurveyChoice(id=2, survey_id=734, name="Toinen valinta", max_spaces=7, info_columns=[
            SurveyChoiceInfo(id=1, choice_id=2, info_key="Kuvaus", info_value="Ihan kiva valinta tämäkin, muttei ensimmäinen"),
            SurveyChoiceInfo(id=2, choice_id=2, info_key="Osoite", info_value="Tokatie 2, 00100 Helsinki")
        ]),
        SurveyChoice(id=3, survey_id=734, name="Kolmas valinta", max_spaces=6, info_columns=[
            SurveyChoiceInfo(id=1, choice_id=3, info_key="Kuvaus", info_value="Kolmas valinta toden sanoo?"),
            SurveyChoiceInfo(id=2, choice_id=3, info_key="Osoite", info_value="Kolkkitie 3, 00100 Helsinki")
        ])
    ]
)

print(MOCK_SURVEY)