from datetime import datetime
from flask import url_for



class Diary:
    def __init__(self, entries, date, content, entry):
        self.date = date
        self.content = content
        self.entries=[]
        self.entry = {}

    def add_entry(self):
        #create empty entry if entry has been used before
        self.entry = {}
        self.date = datetime.now()
        self.entry = {
            "Date": self.date.strftime('%A %B, %Y')
            "content:": self.content
        }
        entries.append(entry)
        return entry
    
    def find_entry_by_date(self, date):
        specific_entries = []
        for entry in self.entries:
            if date == self.date:
                return entry
        for entry in self.entries:
            if date == self.date.strftime('%A') or date == self.date.strftime('%B') or date == self.date.strftime('%Y'):
                specific_entries.append(entry)
        return specific_entries

    def modify_entry(self, date):
        for entry in self.entries:
            if date == self.date:
                return self.entry["content"]

    def delete_entry(self, date):
        for entry in self.entries:
            if date == self.date:
                self.entries.pop()
                return "Entry Deleted"

    @staticmethod
    def list_all_entries():
        if entries:
            return self.entries