from datetime import datetime


'''Note that user model has not been included
which will enable more distinguishing between
several users'''

entries = []
entry_id = 1


class Diary:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

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
