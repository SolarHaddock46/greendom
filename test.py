import json
with open('testfile.json', w) as file:
    json.dump({'ph_high_threshold': "16.0"}, file)
