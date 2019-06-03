# Med Reminder

An implementation of patient interaction with a pharmacy clerk using VUI(voice user interface) through Alexa.

## Getting Started

Clone to your local machine, update skill id in .ask/config and skill.json files.

### Prerequisites

Need to have aws cli and ask cli installed and configured.

```
pip install aws cli

Set up ask cli:
https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html
```

### Installing

Create venv with virtualenv in base dir, then install packages in lambda/requirements.txt

First install all requirements in your venv
```
pip install -r requirements.txt
```
**THEN** do the same in `lambda/` director **with** the -t 

```
pip install -t . -r requirements.txt
```
This helps with uploading dependencies into lambda func.


### Currently Uses

* Dialog.DelegateDirective to chain intents from launchrequest based on whether or not user exists in db.
* Dynamodb persistence adapter to save/retrieve information on the current user.
* Amazon.YesIntent and Amazon.NoIntent for handling dynamic question prompts(cannot be put into the build side)

### Future Additions

* Adding helper API for **reminders**.
* Adding **dynamic entities** to further customize.
* Creating a helper SSML API for **sounds**.


### SSML Utility

SSMLHelper class acts as the interface for exposing numeric SSML related tags as well as text SSML related tags. Each of the sub classes support chaining so you can iteratively build speech. 

Note: This is currently only set-up to work with Alexa SDK's speak() function

```
from medreminder_utils import SSMLHelper
ssml = SSMLHelper
text = ssml.get_text_helper()

```

## Deployment

Deploy with ask cli command, or manually upload files to lambda/alexa. I have included a zip and upload utility for lambda.

```
python zip_upload.py
```
Creates function.zip file and uploads it to your lambda arn.

## Contributing

Please contact me via opening an issue ticket if you'd like to contribute.

## Authors
Hiren Patel - github.com/hpca01


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
