import json
import os

DATA_FILE = 'data/users.json'

def save_user_data(user_id, data):
    # Load existing data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

    # Save or update user data
    users[user_id] = data
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

def get_user_data(user_id):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            users = json.load(f)
        return users.get(user_id)
    return None
