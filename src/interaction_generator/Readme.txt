This new version of Interaction Generator is created to work on informations retrieved by JSON data (repositories available at https://github.com/opendatajson/factbook.json and https://github.com/opendatajson/football.json.

For simplicity, the JSON files are downloaded and processed off-line.

Informations in json data, are used to generate files for quiz-like interactions.
These informations are elaborated by actionWriter.py that generates final files, used by the robot in its interactions. 

* quiz_country.py = Retrieves informations as continent area, name of country, area…then compare the size of a country tuple and return the informations needed to generate the interaction file.
The comparison is done for every tuple of countries found in the corrisponding json folder (/factbook.json).

* quiz_football.py = Retrieves informations of a match: matchday, team1, team2, score1, score2…compare the score point to evaluate which is the winner team. Returning these informations, actionWriter.py can generate quizzes for every match of every matchday of every European Championship of every year that is stored in the relative folder (/football.json).
Notice, for our case, only italian, spanish and english leagues are considered.

* entertainment_act.py = Used to generate file to ask the user if she/he wants to do a quiz on football or on geography.

* activity_act.py = Used to generate file to ask the user if she/he wants to interact with the robot.

All these interactions are available in multilanguage mode (es:italian, spanish and english).

To generate interaction files of the desired interaction, open interactionGenerator.py and choose among the available ones.

If you want to add a new interaction, just write your phython code which returns an action dictionary like:

action = {'NAME': 'action_name',
          'TEXTS': action_text(),
          'BUTTONS': action_button(),
          'GRAMMARS': action_grammar()
          }

and import it in interactionFiles.py


