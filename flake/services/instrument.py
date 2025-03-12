import requests

class InstrumentService:
  def __init__(self, url: str, id: str):
    self.url = url
    self.id = id
  
  def get(self):
    # request GET /config/instrument/{id}
    resp = requests.get(f"{self.url}/config/instrument/{self.id}")
    return resp.json()
  
  def remove(self):
    # request DELETE /config/instrument/{id}
    resp = requests.delete(f"{self.url}/config/instrument/{self.id}")
    return resp.json()