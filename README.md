# rasa-dialogflow-interpreter
[![Build Status](https://travis-ci.org/m90/rasa-dialogflow-interpreter.svg?branch=master)](https://travis-ci.org/m90/rasa-dialogflow-interpreter)
> rasa_core interpreter connecting to dialogflow.com API v2

A `rasa_core` [Interpreter](https://core.rasa.com/interpreters.html) that sources intent data from dialogflow.com API v2. This means you can run `rasa_core` and do Natural Language Understanding using Dialogflow.

## Installation

Install using pip:

```
pip install rasa-dialogflow-interpreter
```

## Usage

```py
from rasa_dialogflow_interpreter.interpreter import DialogflowInterpreter
from rasa_core.agent import Agent

agent = Agent.load(
    'path/to/dialogue/models',
    interpreter=DialogflowInterpreter(
        'dialogflow-project-name',
        # if you omit the `service_account_json` parameter the value
        # exported to GOOGLE_APPLICATION_CREDENTIALS will be used instead
        service_account_json='dialogflow-project-name.json',
    ))

msg = agent.handle_message('Hello Dialogflow!')
```

Note that due to the way that Dialogflow currently works, the returned `entities` will not have `start` and `end` values.

### License
MIT © [Frederik Ring](http://www.frederikring.com)

