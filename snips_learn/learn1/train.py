import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

# snips-nlu generate-dataset en dataset.yaml > dataset.json

engine = SnipsNLUEngine(config=CONFIG_EN)
with io.open('dataset.json') as f:
    dataset = json.load(f)
engine.fit(dataset)
engine.persist("model")
