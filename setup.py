import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasa_dialogflow_interpreter",
    version="0.4.0",
    author="Frederik Ring",
    author_email="frederik.ring@gmail.com",
    description="rasa_core interpreter connecting to dialogflow.com API v2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m90/rasa-dialogflow-interpreter",
    packages=["rasa_dialogflow_interpreter"],
    install_requires=["dialogflow~=0.4", "rasa-core~=0.12"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
