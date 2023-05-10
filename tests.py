import json


with open("db2.json", 'r') as f:
    db = json.load(f)

film_object = {
            "title": "LALAL",
            "year": "2020",
            "director": "uech"
        }

db.append(film_object)

new_db = json.dumps(db, indent=4)

with open("db2.json", 'w') as f:
    f.write(new_db)