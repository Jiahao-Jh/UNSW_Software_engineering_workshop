'''
File: location.py
File Created: Monday, 14th March 2022 11:31:40 am
Author: Hu Shuhao (hu.shuhao@outlook.com)
'''
from calendar import c
import json


class Location(dict):
  def __init__(self, country='', city=''):
    dict.__init__(self, country=country, city=city)
  
  def json(self):
    return json.dumps(self)