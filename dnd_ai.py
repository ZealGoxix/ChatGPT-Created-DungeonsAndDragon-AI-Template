#ChatGPT Created

import requests # type: ignore
import random
import textwrap
import openai
import json
import os

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

# In-memory campaign state
campaign = {
    "quests": [],
    "npcs": [],
    "encounters": [],
    "characters": {},
    "story": []
}

# List of possible monsters to randomly select from if the API call fails
default_monsters = ["goblin", "orc", "skeleton", "zombie", "bandit"]

def print_wrapped(text, width=80):
    """Wraps text neatly to fit within the terminal width."""
    print(textwrap.fill(text, width=width))

def roll_dice(dice="d20"):
    """Rolls a specified dice, e.g., d20, d6, d8."""
    sides = int(dice[1:])
    result = random.randint(1, sides)
    print(f"Rolled a {dice}: {result}")
    return result

def import_character(filename="character.json"):
    """Loads character data from a JSON file (e.g., exported from D&D Beyond)."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            character_data = json.load(f)
            campaign["characters"][character_data["name"]] = character_data
            print(f"Character '{character_data['name']}' loaded into the campaign.")
    else:
        print("Character file not found.")

def get_monster(monster_name=None):
    """Fetches monster details from the Open5e API or randomly selects a default monster."""
    if not monster_name:
        monster_name = random.choice(default_monsters)
    
    url = f"https://api.open5e.com/monsters/{monster_name.lower()}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Monster '{monster_name}' not found."}
    
def get_quest():
    """Generates a random quest using the Chartopia API."""
    url = "https://chartopia.d12dev.com/api/v1/command/random/"
    response = requests.get(url)
    if response.status_code == 200:
        quest = response.json()["content"]
        campaign["quests"].append(quest)
        return quest
    else:
        return "Failed to retrieve quest."

def generate_npc_dialogue(prompt):
    """Generates NPC dialogue using ChatGPT."""
    characters = "\n".join(f"{k}: {v['class']} (Level {v['level']})" for k, v in campaign["characters"].items())
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are a D&D assistant. The current campaign contains the following: "
                f"Quests: {campaign['quests']}, NPCs: {campaign['npcs']}, Encounters: {campaign['encounters']}."
                f" Characters: {characters}. Use this information to respond appropriately."
            )},
            {"role": "user", "content": prompt}
        ]
    )
    npc_dialogue = response.choices[0].message['content']
    campaign["npcs"].append({"prompt": prompt, "response": npc_dialogue})
    return npc_dialogue

def generate_next_encounter():
    """Generates the next encounter/event with a randomly chosen monster using ChatGPT."""
    monster_name = random.choice(default_monsters)  # Select a random monster from the list
    monster = get_monster(monster_name)  # Retrieve monster details
    monster_info = (
        f"Monster: {monster['name']}\n"
        f"Type: {monster.get('type', 'unknown')}\n"
        f"HP: {monster.get('hit_points', 'unknown')}\n"
        f"AC: {monster.get('armor_class', 'unknown')}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "Generate an encounter for a D&D campaign that includes a monster. "
                "Use the following details:\n"
                f"Quests: {campaign['quests']}, NPCs: {campaign['npcs']}, Story: {campaign['story']}."
                f" You must include the monster: {monster_info}"
            )}
        ]
    )
    encounter = response.choices[0].message['content']
    campaign["encounters"].append({"encounter": encounter, "monster": monster_info})
    return encounter

def combat(character_name, monster_name, attack_type="basic attack"):
    """Simulates a combat encounter between a character and a monster."""
    character = campaign["characters"].get(character_name)
    monster = get_monster(monster_name)

    if not character or "error" in monster:
        print("Character or monster not found.")
        return

    character_attack_roll = roll_dice("d20") + character.get("strength", 0)
    monster_defense = monster.get("armor_class", 10)

    if character_attack_roll >= monster_defense:
        damage = roll_dice("d8") + character.get("strength", 0)
        print(f"{character_name} hits {monster['name']} with a {attack_type} for {damage} damage!")
    else:
        print(f"{character_name} misses {monster['name']} with a {attack_type}.")

def generate_story_segment():
    """Generates the next part of the adventure story."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "Continue the story with a new adventure segment. Consider the ongoing quests, NPCs, and encounters."
                f" Quests: {campaign['quests']}, Story: {campaign['story']}."
            )}
        ]
    )
    story_segment = response.choices[0].message['content']
    campaign["story"].append(story_segment)
    return story_segment

def save_campaign(filename="campaign.json"):
    """Saves the campaign state to a JSON file."""
    with open(filename, "w") as f:
        json.dump(campaign, f, indent=4)
    print("Campaign saved.")

def load_campaign(filename="campaign.json"):
    """Loads the campaign state from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            global campaign
            campaign = json.load(f)
        print("Campaign loaded.")
    else:
        print("No saved campaign found.")

def main():
    print_wrapped("Welcome to the D&D AI Command Prompt! Type 'help' for commands.")

    load_campaign()  # Load previous campaign if available

    while True:
        command = input("> ").strip().lower()

        if command == "help":
            print_wrapped(
                "Commands:\n"
                "- monster [name]: Get monster details\n"
                "- quest: Generate a quest\n"
                "- npc [prompt]: Generate NPC dialogue\n"
                "- encounter: Generate the next encounter\n"
                "- roll [dice]: Roll a dice, e.g., d20, d6\n"
                "- story: Generate the next story segment\n"
                "- combat [character] [monster] [attack]: Start a combat encounter\n"
                "- import [file]: Import a character from a JSON file\n"
                "- save: Save the current campaign\n"
                "- load: Load a saved campaign\n"
                "- exit: Quit"
            )

        elif command.startswith("combat"):
            parts = command.split()
            if len(parts) >= 3:
                character_name = parts[1]
                monster_name = parts[2]
                attack_type = " ".join(parts[3:]) if len(parts) > 3 else "basic attack"
                combat(character_name, monster_name, attack_type)
            else:
                print("Please specify a character, monster, and optional attack type.")

        elif command.startswith("monster"):
            monster_name = command.split()[1] if len(command.split()) > 1 else None
            monster = get_monster(monster_name)
            if "error" in monster:
                print(monster["error"])
            else:
                print_wrapped(
                    f"Monster: {monster['name']}\n"
                    f"Type: {monster.get('type', 'unknown')}\n"
                    f"HP: {monster.get('hit_points', 'unknown')}\n"
                    f"AC: {monster.get('armor_class', 'unknown')}"
                )

        elif command == "quest":
            quest = get_quest()
            print_wrapped(f"Quest: {quest}")

        elif command.startswith("npc"):
            prompt = command[4:].strip()
            if not prompt:
                print("Please provide a prompt for the NPC.")
            else:
                npc_response = generate_npc_dialogue(prompt)
                print_wrapped(f"NPC: {npc_response}")

        elif command == "encounter":
            encounter = generate_next_encounter()
            print_wrapped(f"Encounter: {encounter}")

        elif command.startswith("roll"):
            dice = command.split()[1] if len(command.split()) > 1 else "d20"
            roll_dice(dice)

        elif command == "story":
            story_segment = generate_story_segment()
            print_wrapped(f"Story: {story_segment}")

        elif command.startswith("import"):
            filename = command.split()[1] if len(command.split()) > 1 else "character.json"
            import_character(filename)

        elif command == "save":
            save_campaign()

        elif command == "load":
            load_campaign()

        elif command == "exit":
            save_campaign()
            print("Goodbye!")
            break

        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()