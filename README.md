# OSRS Computer Vision Bot

OSRS Computer Vision Bot is a set of python scripts and utilities that uses computer vision to detect colours,
images and text to automate the monitoring and control of the Old School Runescape client (specifically RuneLite).
This set of scripts also leverage a custom RuneLite plugin to expose the game state to the python scripts. The plugin is
completely within the guidelines provided by Jagex and should not be considered cheating.
This project is a hobby project to learn more about computer vision using a game that I loved playing as a kid
as the sandbox.

If you are interested building your own bot using similar technologies I would recommend checking out the following
project as it has a larger community, more mature, and provided some great ideas for parts of this project.

[OSRS Bot COLOR (OSBC)](https://github.com/kelltom/OSRS-Bot-COLOR)

Also, checkout the following project as it was the inspiration for this project and borrowed a lot of his work to jump
start my own.

[slyautomation bot](https://github.com/slyautomation/osrs_basic_botting_functions)

# Developer Setup (Windows Only)

1. Install Python 3.11 or newer
2. Clone/download this repository
3. Create a new virtual environment and activate it
4. Install the dependencies ```pip install -r requirements.txt```
5. Install tesseract-ocr
6. Compile RuneLite from source with the custom plugin
7. Run RuneLite with custom plugin and login to your account
8. Update pybot-config.yaml
9. Run one of the scripts

As of the writting of this README, tesseract-ocr is legacy from some ideas taken from slyautomation. I plan to remove
this dependency in the future.

## Getting Started

If you are new to python or OSRS color botting I would recommend checking out slyautomations project as it is a great
place to start and has much more detail on installing and setting up everything you need than this one.

## Custom RuneLite Plugin

The custom RuneLite plugin is used to expose the game state to the python scripts by setting up a locally available
server that exposes the information via requests. The reason that I have opted to use
a custom plugin instead of an existing plugin is two fold, first I wanted the flexibility to expose the game state and
other information that I needed and in a way that made sense to me and second I wasn't able to find a plugin that
accomplished what I needed. I took a look at existing plugins
and [morgHttpClient](https://github.com/MorgApps/morghttpclient/blob/master/src/main/java/com/morghttpclient/HttpServerPlugin.java)
plugin was the closest to what I wanted.
I took some inspiration from his plugin and used it as a starting point for my own.

I hope to get my plugin into the RuneLite plugin hub in the future but for now you will need to compile it from source.

From my reading this plugin should not break the Jagex Third Party Client Guidelines.

The plugin can be found here in `plugin/`

## Script Information

A lot of the scripts also leverage existing plugins to add colour, images, and text to the game client. These plugins
include but are not limited to: Ground Items, Object Markers, NPC Indicators, Inventory Tags, and Individual Skilling
Plugins

You will need to mark rocks, trees, npcs, etc. with the appropriate plugin to use the scripts.
