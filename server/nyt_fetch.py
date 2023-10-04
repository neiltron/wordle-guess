import os
import requests
import json

CACHE_DIR = './data/cache'

def fetch_wordle_solution(date):
  cache_file_path = os.path.join(CACHE_DIR, f"{date.strftime('%Y-%m-%d')}.json")

  if os.path.exists(cache_file_path):
    with open(cache_file_path, 'r') as f:
      data = json.load(f)
  else:
    url = f"https://www.nytimes.com/svc/wordle/v2/{date.strftime('%Y-%m-%d')}.json"
    response = requests.get(url)
    if response.status_code != 200:
      raise ValueError(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    data = response.json()
    with open(cache_file_path, 'w') as f:
      f.write(response.text)

  return data["solution"]