import requests

class ConfigService:
  
  def __init__(self, url: str):
    self.url = url
  
  def get_instruments(self):
    # request GET /config/instruments
    resp = requests.get(f"{self.url}/config/instruments")
    return resp.json()
  
  def add_or_update_instrument(self, payload: dict):
    # request POST /config/instruments
    resp = requests.post(f"{self.url}/config/instruments", json=payload)
    return resp.json()
  