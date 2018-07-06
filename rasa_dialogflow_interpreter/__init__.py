from string import ascii_lowercase
from random import choice

from rasa_core.interpreter import NaturalLanguageInterpreter
import dialogflow
from google.oauth2.service_account import Credentials


def serialize_response(msg, intent=None, entities=None):
    """
    serialize_response builds a rasa_core compatible dict using
    the given message, intent and list of entities
    """
    return {
        'text': msg,
        'intent': intent,
        'entities': entities if entities is not None else [],
    }


class DialogFlowInterpreter(NaturalLanguageInterpreter):
    """
    DialogFlowInterpreter is an Interpreter for use in rasa_core that
    performs Natural Language processing using dialogflow v2
    """
    def __init__(self, project_id=None, service_account_json=None, language_code='en'):
        self.project_id = project_id
        self.language_code = language_code
        self.service_account_json = service_account_json

    def parse(self, text):
        """
        parse takes a string and responds with the NLU results sent
        by dialogflow
        """
        credentials = None
        if self.service_account_json:
            credentials = Credentials.from_service_account_file(
                self.service_account_json)

        session_client = dialogflow.SessionsClient(
            credentials=credentials)

        # as we want to delegate conversation flow to rasa core
        # we force dialogflow to be stateless by passing a random string
        # as session_id value
        session_id = ''.join(choice(ascii_lowercase) for i in range(16))
        session = session_client.session_path(self.project_id, session_id)
        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        if not response:
            return serialize_response(text)

        return serialize_response(
            response.query_result.query_text, intent={
                'name': response.query_result.intent.display_name,
                'confidence': response.query_result.intent_detection_confidence,
            })
