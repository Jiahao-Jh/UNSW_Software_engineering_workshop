'''
File: Report.py
File Created: Friday, 11th March 2022 7:48:55 pm
Author: Hu Shuhao (hu.shuhao@outlook.com)
'''

import json


class Report(dict):

    def __init__(self,
                 disease,
                 syndromes='Not implemented yet',
                 locations=[],
                 event_date=None,
                 cases=-1,
                 death=-1,
                 hospitalization=-1):
        dict.__init__(self, disease=disease,
            syndromes=syndromes,
            locations=locations,
            event_date=event_date,
            cases=cases,
            death=death,
            hospitalization=hospitalization)

    def json(self):
        return json.dumps(self)
