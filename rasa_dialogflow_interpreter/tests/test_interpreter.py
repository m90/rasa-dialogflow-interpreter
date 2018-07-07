import unittest

import dialogflow

from rasa_dialogflow_interpreter.interpreter import build_response, DialogflowInterpreter


class TestBuildResponse(unittest.TestCase):
    def test_default(self):
        expected = {
            'text': 'hello people',
            'intent': {
                'name': 'greet',
                'confidence': 0.8,
            },
            'entities': [],
        }
        result = build_response(
            'hello people', intent={
                'name': 'greet',
                'confidence': 0.8,
            }, entities=[])

        self.assertDictEqual(expected, result)

    def test_no_entities(self):
        expected = {
            'text': 'no entities needed',
            'intent': {
                'name': 'be-lazy',
                'confidence': 1.0,
            },
            'entities': [],
        }
        result = build_response(
            'no entities needed', intent={
                'name': 'be-lazy',
                'confidence': 1.0,
            })
        self.assertDictEqual(expected, result)


class MockSessionsClient:
    def __init__(self, *args, **kwargs):
        pass

    def session_path(self, project_id, session_id):
        return '{}-{}'.format(project_id, session_id)

    def detect_intent(self, session=None, query_input=None):
        return {
            'query_result': {
                'query_text': 'Hello human',
                'intent': {
                    'display_name': 'welcome',
                },
                'intent_detection_confidence': 0.85,
            },
        }


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._sessions_client = dialogflow.SessionsClient
        dialogflow.SessionsClient = MockSessionsClient

    def tearDown(self):
        dialogflow.SessionsClient = self._sessions_client

    def test_default_properties(self):
        interpreter = DialogflowInterpreter(
            project_id='my-dflow-projjy', language_code='es')

        self.assertEqual(interpreter.project_id, 'my-dflow-projjy')
        self.assertEqual(interpreter.language_code, 'es')

    def test_language_code_property(self):
        interpreter = DialogflowInterpreter(
            project_id='my-dflow-projjy')

        self.assertEqual(interpreter.project_id, 'my-dflow-projjy')
        self.assertEqual(interpreter.language_code, 'en')
