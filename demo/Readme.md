# MODIM demo example #

This folder contains an example of a demo.

A demo must contain the following elements:
* `init`: file describing the default GUI configuration when the robot is not interacting with a person.
* `lang_instance`: file describing the possible languages available for the demo. Images of the flags must be included in the img folder.
* `index.html` (+ possible other HTML files): layout files
* `img`: folder containing images
* `actions`: folder containing specification of MODIM action
* `grammars`: folder containing the grammar files used in the demo. 
* `scripts`: folder containing interaction scripts

The .xml and .grxml files can be automatically generated from a .txt file using the grammar generator.
The file associates each recognized word with a keyword or label that must be sent to PNP.

How to run example:

```
cd $MODIM_HOME/src/GUI
python ws_server.py [-robot pepper|marrtino]
```

```
cd $MODIM_HOME/demo/eurobotics
python -m SimpleHTTPServer 8000
```

```
firefox <demoIP>:8000
```

```
cd $MODIM_HOME/demo/eurobotics/scripts
python demo1.py
```


