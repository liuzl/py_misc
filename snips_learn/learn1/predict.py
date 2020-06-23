import json
from snips_nlu import SnipsNLUEngine

engine = SnipsNLUEngine.from_path("model")

parsing = engine.parse('Please give me some lights in the entrance !')
print(json.dumps(parsing, indent=2))
