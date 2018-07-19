from datetime import datetime
from flask import url_for


Diaries = 0

class Diary:
    def __init__(self, name, email, password, entries, date, content, entry):
        self.name = name
        self.email = email
        self.password = password
        self.date = date
        self.content = content
        self.entries=[]
        self.entry = entry


    def add_entry(self, enter_content):
        #create empty entry if entry has been used before
        self.entry = {}
        self.date = datetime.now()
        self.content = enter_content
        self.entry = {
            "Date": self.date,
            "content": self.content
        }
        self.entries.append(self.entry)
        return self.entry
    
    def find_entry_by_date(self, date):
        group_entries = []
        for entry in self.entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                return entry
            #return not found if  full date is give by the followiing condition
            elif len(date) > 10:
                return 'No such entry'
        for entry in self.entries:
            if date == entry["Date"].strftime('%A') or date == entry["Date"].strftime('%B') or date == entry["Date"].strftime('%C'):
                group_entries.append(entry)
        specific_entries={"grouped": group_entries}
        if group_entries == []:
            return 'No such entries'
        return specific_entries

    def modify_entry(self, date):
        for entry in self.entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                return self.entry["content"]
        return 'No such entry'

    def delete_entry(self, date):
        for entry in self.entries:
            if date == entry["Date"].strftime('%A.%B.%Y'):
                self.entries.pop()
                return "Entry Deleted"
        return 'No such entry'

    def list_all_entries(self):
        if self.entries:
            return self.entries