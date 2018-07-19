from datetime import datetime


'''Note that user model has not been included
which will enable more distinguishing between
several users'''

entries = []


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
        entry = {
            "Date": date,
            "content": content
        }
        entries.append(entry)
        return entry

    @staticmethod
    def find_entry_by_date(date):
        group_entries = []
        for entry in entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                return entry
            elif len(date) > 10:
                return 'No such entry'
        for entry in entries:
            if date == entry["Date"].strftime('%A') or date == entry["Date"].strftime('%B') or date == entry["Date"].strftime('%C'):
                group_entries.append(entry)
        specific_entries = {"grouped": group_entries}
        if group_entries == []:
            return 'No such entries'
        return specific_entries

    @staticmethod
    def modify_entry(date):
        for entry in entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                return entry["content"]
        return 'No such entry'

    @staticmethod
    def delete_entry(date):
        for entry in entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                entries.remove(entry)
                return "Entry Deleted"
        return 'No such entry'

    @staticmethod
    def list_all_entries():
        if entries != []:
            return entries
        return 'No entries'
