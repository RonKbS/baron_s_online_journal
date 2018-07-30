from datetime import datetime
import testing_database

'''Note that user model has not been included
which will enable more distinguishing between
several users'''

entries = []
users = []
entry_id = 1
users = []
count_user_id = 1


class User:
    def __init__(self, name, email, password, user_id):
        self.name = name
        self.email = email
        self.password = password
        self.user_id = count_user_id

    def add_user(self, user_id, count_user_id):
        User = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'Userid': count_user_id
        }
        count_user_id += 1
        users.append(User)
        return User


class Diary(User):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def add_entry(enter_content, count_user_id):
        '''create empty entry if entry has been used before'''
        entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "date": date.strftime('%A.%B.%Y'),
            "content": content,
<<<<<<< Updated upstream
            "ID": entry_id,
            "Userid": super.User.user_id
||||||| merged common ancestors
            "entry_id": Diary.entry_id,
            "user_id": Diary.count_user_id

=======
            "entry_id": Diary.entry_id,
            "user_id": count_user_id

>>>>>>> Stashed changes
        }
<<<<<<< Updated upstream
        for entry in entries:
            if entries == []:
                entries.append(new_entry)
                return entry
            elif new_entry["content"] == entry["content"]:
                return "New entry is similar to older entry"
            else:
                entry["ID"] = entry["ID"] + 1
        entries.append(new_entry)
||||||| merged common ancestors
        for entry in Diary.entries:
            if Diary.entries == []:
                Diary.entries.append(new_entry)
                return entry
            elif new_entry["content"] == entry["content"]:
                return "New entry is similar to older entry"
            else:
                entry["ID"] = entry["ID"] + 1
        Diary.entries.append(new_entry)
=======
        for user in Diary.users:
            if user['Userid'] == count_user_id:
                for entry in Diary.entries:
                    if Diary.entries == []:
                        Diary.entries.append(new_entry)
                        return entry
                    elif new_entry["content"] == entry["content"]:
                        return "New entry is similar to older entry"
                    else:
                        entry["ID"] = entry["ID"] + 1
        Diary.entries.append(new_entry)
>>>>>>> Stashed changes
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
