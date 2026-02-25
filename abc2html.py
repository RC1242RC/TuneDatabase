# CONVERT ABC FILES INTO HTML TABLE

# Imports
import os
import pandas as pd
from tqdm import tqdm
import itertools
import Levenshtein

# Options
tune_dir = os.path.join(".", "Tunes")
html_file_path = os.path.join("..", "PersonalWebsite", "static", "data", "tunelist_table.html")
similarity_cutoff_names = 0.4
similarity_cutoff_tunes = 0.6

# Open each abc file in turn and read the lines
tune_list = []
tune_files = os.listdir(tune_dir)
for i in tqdm(range(len(tune_files))):
    tune_file = tune_files[i]
    tune_dict = {"ABC": []}
    with open(os.path.join(tune_dir, tune_file)) as open_tune_file:
        lines = open_tune_file.readlines()

        # For each line, match the start to a valid abc property
        line_starts = {"X:": {"Found": False, "Name": "X"}, 
                       "T:": {"Found": False, "Name": "Title"}, 
                       "C:": {"Found": False, "Name": "Composer"}, 
                       "M:": {"Found": False, "Name": "Time"}, 
                       "R:": {"Found": False, "Name": "Type"}, 
                       "L:": {"Found": False, "Name": "Time Unit"}, 
                       "S:": {"Found": False, "Name": "Source"}, 
                       "K:": {"Found": False, "Name": "Key"}}
        line_tracker = [False]*8
        for line in lines:
            categorised_line = False
            for line_start in line_starts:
                if categorised_line == False:
                    if line[:2] == line_start:
                        if line_starts[line_start]["Found"] == True:
                            raise RuntimeError("Duplicate of \"{}\" property found in \"{}\"".format(line_start, tune_file))
                        else:
                            line_starts[line_start]["Found"] = True
                            tune_dict[line_starts[line_start]["Name"]] = line[2:].strip()
                            categorised_line = True
            
            # If line is not matched to property, check if it is blank, which is illegal
            # If not blank, then this must be the body of the tune
            if categorised_line == False:
                if line.strip() == "":
                    raise RuntimeError("\"{}\" contains a blank line".format(tune_file))
                else:
                    tune_dict["ABC"] += [line]
                    categorised_line = True

    # Add parsed tune to list
    tune_dict["ABC"] = "".join(tune_dict["ABC"])
    tune_list += [tune_dict]

# Check similarities
sim_names = []
sim_tunes = []
for pair in itertools.combinations(tune_list, 2):
    if Levenshtein.ratio(pair[0]["Title"], pair[1]["Title"]) >= similarity_cutoff_names:
        sim_names += [(pair[0]["Title"], pair[1]["Title"])]
    if Levenshtein.ratio(pair[0]["ABC"], pair[1]["ABC"]) >= similarity_cutoff_tunes:
        sim_tunes += [(pair[0]["Title"], pair[1]["Title"])]
print("Checking similarities")
print("-"*20)
print("Tune pairs with similar names: {}".format(len(sim_names)))
if len(sim_names) != 0:
    for pair in sim_names:
        print("    ", pair)
print("-"*20)
print("Tune pairs with similar notes: {}".format(len(sim_tunes)))
if len(sim_tunes) != 0:
    for pair in sim_tunes:
        print("    ", pair)
print("-"*20)


# Construct DataFrame and write to html file
tune_pd = pd.DataFrame(tune_list, columns=["Title", "Type", "Time", "Time Unit", "Key", "Composer", "Source", "ABC"])
# Old order: ["Type", "Time", "Time Unit", "Key", "Title", "Composer", "Source", "ABC"]
tune_pd.to_html(buf=html_file_path, index=False, table_id="tunelist_table", classes=["display compact"], border=False)
print("Written to {}".format(html_file_path))