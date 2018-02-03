Init file options:

WELCOMEMSG: Message to 
LEFTIMG: image to be displayed on the left side of the GUI. It remains fixed during the interaction.
RIGHTIMG: image to be displayed on the left side of the GUI. It is changed during the interaction.
PROFILE: default profile with format <age, gender, language, occupation>
MULTILANG: set to YES if multiple languages must be considered.


Implemented actions:
- display_init: resets the GUI according to the Init file configuration.
- display_[text|image]_action  : displays [text|image] according to the content of the file with the same name (i.e., text_goodbye, image_welcome, etc...)
- display_txtimg_action  : displays both text and image according to the content of the file with the same name (i.e., text_welcome, image_welcome)
- say_action: sends the string contained in the file text_action to the TTS component
- ask_action: displays a text (usually a question) and a set of buttons contained in a file text_action
- askimg_action: displays a text and buttons contained in a file text_action and an image contained in image_action
- set_profile_<*,*,*,*>: changes the current profile to <*,*,*,*>

===========================================================================================

HTML/JavaScript/Websocket version

1. Run ws server

python ws_server.py

2. Run the web page

firefox QAGUI.html

3. Run the interaction

python demo1.py





