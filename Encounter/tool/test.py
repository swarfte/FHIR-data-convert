import json
import blueprint as blueprint

demo = blueprint.EncounterTemplate()
jsonStr = json.dumps(demo.__dict__)

with open('demo.json', 'w') as f:
    f.write(jsonStr)

print(jsonStr)
