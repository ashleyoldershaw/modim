Grammar generator

The script allows to automatically generate well formed grammar files starting from a text file made of a sequence of strings.

Text file

A text file encloses all the words, sequence of words or phrases to be recognized by the robot.
It is the only file to be written or to be modified in order to create, to add or to delete elements from a grammar.

The name of the text file is exactly the name of the topic of interest plus the language tag for the xml:lang attribute;
Example:
topic_en-US".txt

Content of the text file follows this rule: A -> B as (words, sequence of words or phrases) -> (symbol returned in the grammar frame);

Example:
yes -> yes
no -> no
cancel, sorry I made a mistake -> cancel


Script files

To generate grammars, run "python generator.py" from terminal and files:
topic.xml
topic_languageTag.grxml
frame_topic_languageTag.grxml

for each topic-text file are created.


