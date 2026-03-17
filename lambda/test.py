from lib.util.make_response import make_response
import json

print(json.dumps(make_response(200, {"type": 5}), indent=2))
print(make_response(200, {"type": 5}))