import requests

class InstrumentService:
  def __init__(self, url: str, name: str):
    self.url = url
    self.name = name
  
  def get(self):
    # request GET /config/instrument/{id}
    resp = requests.get(f"{self.url}/config/instrument/{self.name}")
    return resp.json()
  
  def get_logs(self, tail: int = 100):
    # request GET /logs/instrument/{id}
    resp = requests.get(f"{self.url}/logs/instrument/{self.name}", params={"tail": tail})
    return resp.text
  
  def get_logs_stream(self, tail: int = 100):
    # request GET /logs/instrument/{id}
    resp = requests.get(f"{self.url}/logs/instrument/{self.name}", params={"tail": tail}, stream=True)
    return resp.iter_lines(decode_unicode=True)
  
  def remove(self):
    # request DELETE /config/instrument/{id}
    resp = requests.delete(f"{self.url}/config/instrument/{self.name}")
    return resp.json()