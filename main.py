import requests
import csv
import json
import ciso8601

url = "http://api.coincap.io/v2/assets/{}/history?interval={}&start={}&end={}"