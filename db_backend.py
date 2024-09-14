import json
import os


class DB:
    PATH = f'{os.getcwd()}/db.json'

    def __init__(self):
        self.setup()

    def setup(self):
        """ Check exists and create json file """
        if not os.path.exists(self.PATH):
            with open(self.PATH, 'w') as file:
                json.dump({}, file, indent=4)

    def chats(self):
        """ Return exists chat ids """
        with open(self.PATH, 'r') as file:
            data = json.load(file)
            return data.keys()

    def get(self, chat_id=None):
        """
        Return chat's data by chat_id.
        If not chat_id - return all data.
        """
        chat_id = str(chat_id)
        with open(self.PATH, 'r') as file:
            if chat_id:
                return json.load(file).get(chat_id, {})
            else:
                return json.load(file)

    def update(self, chat_id, new_data: dict):
        """ Update chat's data by chat_id """
        chat_id = str(chat_id)

        all_data = self.get()
        chat_data = all_data.get(chat_id, {})
        chat_data.update(**new_data)
        all_data.update({chat_id: chat_data})

        with open(self.PATH, 'w') as file:
            json.dump(all_data, file, indent=4)

    def clear(self, chat_id):
        """ Clear chat's data by chat_id """
        chat_id = str(chat_id)
        with open(self.PATH, 'w') as file:
            data = json.load(file)
            data.pop(chat_id, None)
            json.dump(data, file, indent=4)
