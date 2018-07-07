import unittest

from rasa_dialogflow_interpreter.interpreter import build_response

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
