import unittest

import dialogflow

from rasa_dialogflow_interpreter.interpreter import build_response, build_entity, DialogflowInterpreter


class TestBuildEntity(unittest.TestCase):
    def test_default(self):
        expected = {
            'entity': 'things',
            'value': 'many',
            'start': 0,
            'end': 0,
        }
        result = build_entity('things', 'many')
        self.assertDictEqual(expected, result)


class TestBuildResponse(unittest.TestCase):
    def test_default(self):
        expected = {
            'text': 'hello people',
            'intent': {
                'name': 'greet',
                'confidence': 0.8,
            },
            'entities': [
                {'entity': 'cash', 'value': 10.0, 'start': 0, 'end': 0},
                {'entity': 'money', 'value': 20.0, 'start': 0, 'end': 0},
            ],
        }
        result = build_response(
            'hello people', intent={
                'name': 'greet',
                'confidence': 0.8,
            }, entities={
                'cash': 10.0,
                'money': 20.0,
            })

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


class MockSessionsClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        pass

    def session_path(self, project_id, session_id):
        return '{}-{}'.format(project_id, session_id)

    def detect_intent(self, session=None, query_input=None):
        class MockResult():
            def __init__(self, query_text, intent, confidence):
                self.query_result = MockQueryResult(query_text, intent, confidence)

        class MockIntent():
            def __init__(self, intent):
                self.display_name = intent

        class MockQueryResult():
            def __init__(self, query_text, intent, confidence):
                self.query_text = query_text
                self.intent = MockIntent(intent)
                self.intent_detection_confidence = confidence
                self.parameters = {}

        return MockResult('Hello bot', 'welcome', 0.85)


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

    def test_parse(self):
        interpreter = DialogflowInterpreter(
            project_id='my-dflow-projjy')
        result = interpreter.parse('Oi!')
        self.assertEqual(result['text'], 'Hello bot')

