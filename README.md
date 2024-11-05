# Project Overview

This Python script provides an interactive D&D-inspired command-line prompt. Players can manage a campaign with quests, NPC dialogues, encounters, and a newly added combat system where players can create custom attacks to battle monsters. This script uses OpenAI's API to enhance interactions, creating dynamic dialogues and scenarios.

All credit goes to ChatGPT. This template is kept for learning purposes and possible future projects. Starting my serach for the perfect D&D AI for solo play, I could not find any. D&D AI could never meet the real-life expectations, experience, or role play of having a Dungeon Master. If I could make the reality one step closer even with the current errors, I want to try.

## Features

- **Random Quest Generation**: Retrieve quests from a Chartopia API or add your own.
- **NPC Dialogue Creation**: Generate custom dialogue using OpenAI's ChatGPT API.
- **Encounter Generation**: Randomly generate encounters with monsters, either using an API or pre-defined list.
- **Combat System**: Engage in combat with monsters using user-defined attacks, dice rolls, and health tracking.
- **Dice Rolling**: Roll various types of dice (e.g., d20, d6) for skill checks, attacks, or other scenarios.
- **Campaign Save/Load**: Save and load campaign data as JSON.


## How to Run the Project
## Prerequisites
- [Python 3.x](https://www.python.org/)
- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- Replace API KEY in the code.

Run in Command Line.
```cmd
git clone
cd <repo_directory>
pip install requests openai
python dnd_ai.py
```
# Inspiration

* **Avrae D&D Discord Bot** - Designed to help you and your friends play D&D online.
https://avrae.io/ 
* **AI Dungeon** - A text-based adventure-story game you direct (and star in) while the AI brings it to life.
https://aidungeon.com/ 

## Future Ideas
* **Character Intergration**
* **Turn-Based Combat**
* **AI Training For Better Campaign**
* **Chat-GPT-Generated Passive&Abilites Randomsier For RPG-Like Gameplay**
* **Possible GUI Or [Roll20](https://roll20.net/) Intergration**

# Commands
* ```monster [name]```: Fetch monster details by name.
* ```quest```: Generate a new quest.
* ```npc [prompt]```: Generate NPC dialogue based on the given prompt.
* ```encounter```: Generate a random encounter with a monster.
* ```roll [dice]```: Roll a specified dice, e.g., d20 or d6.
* ```story```: Generate the next segment of the story.
* ```combat [character] [monster] [attack]```: Initiate a combat round with a custom attack.
* ```import [file]```: Import a character from a JSON file.
* ```save```: Save the campaign state.
* ```load```: Load a saved campaign.
* ```exit```: Save and exit the prompt.
  
## Example Output:
Muti-round Combat
**Input:**
```cmd
> combat hero skeleton ice blast
[Combat Initiated]
Hero encounters Skeleton and launches an Ice Blast!
```
**Output:**
```
> Hero rolls d20 for attack...
Rolled a d20: 18
Hero's attack roll (18) vs Skeleton's Armor Class (13): Hit!

> Rolling damage for Ice Blast (1d10)...
Rolled 1d10: 6
Hero's Ice Blast hits Skeleton for 6 damage!
Skeleton's HP reduced from 12 to 6.

**Next Round:**
The Skeleton, weakened but still standing, raises its sword to strike back!

> Skeleton rolls d20 for attack...
Rolled a d20: 14
Skeleton's attack roll (14) vs Hero's Armor Class (12): Hit!

> Rolling damage for Skeleton's attack (1d6)...
Rolled 1d6: 4
Skeleton hits Hero for 4 damage!
Hero’s HP now at 14.
```
This `README.md` file provides a detailed overview of the script, its features, setup instructions, and example command usage, including the new combat system. 


