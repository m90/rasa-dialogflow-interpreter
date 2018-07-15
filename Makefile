test:
	@pytest

package: setup.py
	@python setup.py sdist bdist_wheel

publish: package
	@twine upload dist/*

format:
	@black ./rasa_dialogflow_interpreter/.

.PHONY: format test
