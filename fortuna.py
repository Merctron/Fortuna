import argparse
import datetime
import json
import random
import os

GLOBAL_CONFIG_FILE   = "global.fortuna.json"
GLOBAL_RENEWAL_CACHE = "renewals.fortuna.json"

LIST_TYPE_SELECTIONS = {
    "RANDOMIZE"           : lambda flist: flist[random.randint(0, len(flist) - 1)],
    "RANDOMIZE_AND_CACHE" : lambda flist: flist[random.randint(0, len(flist) - 1)],
    "SELECT_ALL"          : lambda flist: flist
}

LIST_TYPE_FORMATS = {
    "RANDOMIZE"           : lambda selection: "\nToday's {}: {}\n".format(selection["list"], selection["selection"]),
    "RANDOMIZE_AND_CACHE" : lambda selection: "\nToday's {}: {}\n".format(selection["list"], selection["selection"]),
    "SELECT_ALL"          : lambda selection: "\n{}:\n\n{}\n".format(selection["list"],
                                                                  "\n".join(map(lambda item: "* {}".format(item), selection["selection"])))
}

def generate_note_for_cache(selections):
    note = dict()
    note["date"] = datetime.datetime.now()
    for selection in selections:
        note[selection["list"]] = selection["selection"]
    return note

def generate_note(selections):
    note      = generate_note_for_cache(selections)
    note_text = "This is your Fortune for today, {}\n".format(note["date"])
    for selection in selections:
        note_text += LIST_TYPE_FORMATS[selection["type"]](selection)
    return note, note_text

# Import JSON for global configuration.
config_file_path = os.path.join(os.environ["LOCALAPPDATA"], "fortuna", GLOBAL_CONFIG_FILE)
if not os.path.exists(config_file_path):
    os.makedirs(os.path.dirname(config_file_path))
    print("Global configuration not found. Please create it at {}".format(config_file_path))
    exit(0)

config_file = open(config_file_path, "r")
config      = json.load(config_file)

# Import cached history and prune to avoid reuse.

# Create a new list based on available options.
selections = []
for list_key in config:
    flist     = config[list_key]
    selection = LIST_TYPE_SELECTIONS[flist["type"]](flist["options"])
    selections.append({ "list" : list_key, "selection": selection, "type": flist["type"] })

# Publish list to cache. Update cache for renewals if any.
note, note_text = generate_note(selections)
note_json       = json.dumps(note,
                             default=lambda obj: obj.isoformat()) # Supply lambda to serialize datetime.

note_name  = "{}{:02d}{:02d}.fortuna.json".format(note["date"].year, note["date"].month, note["date"].day)
cache_path = os.path.join(os.environ["LOCALAPPDATA"], "fortuna", "cache")
note_path = os.path.join(cache_path, note_name)
if not os.path.exists(note_path):
    os.makedirs(os.path.dirname(note_path))
if os.path.exists(note_path):
    print("A note for {} has already been generated!".format(note["date"].isoformat()))
    exit(0)
note_file = open(note_path, "a")
json.dump(note_json, note_file)

print(note_text)