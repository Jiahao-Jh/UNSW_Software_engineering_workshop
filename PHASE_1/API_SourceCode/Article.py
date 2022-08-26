'''
File: Article.py
File Created: Friday, 11th March 2022 6:04:38 pm
Author: Hu Shuhao (hu.shuhao@outlook.com)
'''

import json


class Article(dict):

    def __init__(self,
                 url='',
                 date_of_publication='Not applicable',
                 headline='The article does not have a headline',
                 main_text='') -> None:
        dict.__init__(self, url=url, date_of_publication=date_of_publication, headline=headline, main_text=main_text,
            reports=[])

    def json(self):
        return json.dumps(self)
