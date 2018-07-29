from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


'''Note that user model has not been included
which will enable more distinguishing between
several users'''

entries = []
users = []
entry_id = 1
users = []
count_user_id = 1


class Diary:

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def add_user(name, user_id, email, password, count_user_id):
        User = {
            'name': name,
            'email': email,
            'password': password,
            'Userid': count_user_id
        }
        count_user_id += 1
        users.append(User)
        return User

    @staticmethod
    def add_entry(enter_content):
        '''create empty entry if entry has been used before'''
        entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "date": date.strftime('%A.%B.%Y'),
            "content": content,
            "ID": entry_id
            "user"
        }
        for entry in entries:
            if entries == []:
                entries.append(new_entry)
                return entry
            elif new_entry["content"] == entry["content"]:
                return "New entry is similar to older entry"
            else:
                entry["ID"] = entry["ID"] + 1
        entries.append(new_entry)
        return new_entry

    @staticmethod
    def find_entry_by_id(entry_id):
        for entry in entries:
            if entry_id == entry["ID"]:
                return entry
        return 'No such entry'

    
    
    @staticmethod
    def modify_entry(entry_id, content):
        for entry in entries:
            if entry_id == entry["ID"]:
                entry["content"] = content
                return entry
        return 'No such entry'

    @staticmethod
    def delete_entry(entry_id):
        for entry in entries:
            if entry_id == entry['ID']:
                entries.remove(entry)
                return "Entry deleted"
        return 'No such entry'

    @staticmethod
    def list_all_entries():
        if entries != []:
            return entries
        return 'No entries'
