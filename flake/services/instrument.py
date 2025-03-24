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
  
  def get_log_lines(self, tail: int = 100):
    # request GET /logs/instrument/{id}
    resp = requests.get(f"{self.url}/logs/instrument/{self.name}", params={"tail": tail}, stream=True)
    return resp.iter_lines(decode_unicode=True)
  
  def get_log_stream(self):
    # request GET /logs/instrument/{id}/files
    resp = requests.get(f"{self.url}/logs/instrument/{self.name}/files", stream=True)
    resp.raise_for_status()
    return resp.iter_content(chunk_size=8192)
  
  def remove(self):
    # request DELETE /config/instrument/{id}
    resp = requests.delete(f"{self.url}/config/instrument/{self.name}")
    return resp.json()