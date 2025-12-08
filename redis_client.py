import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def save(key, data):
    r.set(key, json.dumps(data, ensure_ascii=False))

def load(key):
    value = r.get(key)
    return json.loads(value) if value else None
