from string import ascii_lowercase
from random import choice
import logging

import dialogflow
from rasa_core.interpreter import RegexInterpreter
from google.oauth2.service_account import Credentials
from google.api_core.exceptions import GoogleAPICallError, RetryError

logger = logging.getLogger(__name__)


def build_entity(key, value):
    """
    build_entity return a dict that can be passed back to rasa as an entity
    using the given string key and value
    """
    return {"entity": key, "value": value, "start": 0, "end": 0}


def build_response(msg, intent=None, entities=None):
    """
    build_response builds a rasa_core compatible dict using
    the given message, intent and list of entities
    """
    out_entities = []
    if entities is not None:
        out_entities = [
            build_entity(key, value) for (key, value) in entities.items() if value
        ]

    return {"text": msg, "intent": intent if intent else {}, "entities": out_entities}


class UpstreamError(Exception):
    pass


class DialogflowInterpreter(RegexInterpreter):
    """
    DialogflowInterpreter is an Interpreter for use in rasa_core that
    performs Natural Language processing using dialogflow API v2
    """

    def __init__(
        self,
        project_id=None,
        service_account_json=None,
        language_code="en",
        raise_on_error=False,
    ):
        self.project_id = project_id
        self.language_code = language_code
        self.raise_on_error = raise_on_error

        credentials = None
        if service_account_json:
            credentials = Credentials.from_service_account_file(service_account_json)

        self.session_client = dialogflow.SessionsClient(credentials=credentials)

    def parse(self, text):
        """
        parse takes a string and responds with the NLU results sent
        by dialogflow API v2
        """

        # as we want to delegate conversation flow to rasa core
        # we force dialogflow to be stateless by passing a random string
        # as session_id value
        session_id = "".join(choice(ascii_lowercase) for i in range(16))

        session = self.session_client.session_path(self.project_id, session_id)
        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.language_code
        )

        query_input = dialogflow.types.QueryInput(text=text_input)

        try:
            response = self.session_client.detect_intent(
                session=session, query_input=query_input
            )
        except (RetryError, GoogleAPICallError) as e:
            if self.raise_on_error:
                raise UpstreamError(str(e))
            else:
                logger.error(
                    "Failed to parse text '{}' using dialogflow API v2. "
                    "Error: {}".format(text, e)
                )
                return build_response(text)

        return build_response(
            response.query_result.query_text,
            intent={
                "name": response.query_result.intent.display_name,
                "confidence": response.query_result.intent_detection_confidence,
            },
            entities=response.query_result.parameters,
        )
