import requests

class ConfigService:
  
  def __init__(self, url: str):
    self.url = url
  
  def reload(self):
    # request PUT /config/
    resp = requests.put(f"{self.url}/config/")
    return resp.json()
  
  def get_settings(self):
    # request GET /config/settings
    resp = requests.get(f"{self.url}/config/settings")
    return resp.json()
  
  def get_runtime(self):
    # request GET /config/runtime
    resp = requests.get(f"{self.url}/config/runtime")
    return resp.json()
  
  def get_instruments(self):
    # request GET /config/instruments
    resp = requests.get(f"{self.url}/config/instruments")
    return resp.json()
  
  def add_or_update_instrument(self, payload: dict):
    # request POST /config/instruments
    resp = requests.post(f"{self.url}/config/instruments", json=payload)
    return resp.json()
  