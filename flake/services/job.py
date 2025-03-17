import requests

class JobService:
  def __init__(self, url: str, id: str):
    self.url = url
    self.id = id
  
  def get(self):
    # request GET /scheduler/job/{id}
    resp = requests.get(f"{self.url}/scheduler/job/{self.id}")
    return resp.json()
  
  def get_status(self):
    # request GET /scheduler/job/{id}/status
    resp = requests.get(f"{self.url}/scheduler/job/{self.id}/status")
    return resp.json()
  
  def start(self):
    # request PUT /scheduler/job/{id}?action=start
    resp = requests.put(f"{self.url}/scheduler/job/{self.id}/status", params={"action": "start"})
    return resp.json()
  
  def stop(self):
    # request PUT /scheduler/job/{id}?action=stop
    resp = requests.put(f"{self.url}/scheduler/job/{self.id}/status", params={"action": "stop"})
    return resp.json()
  
  def pause(self):
    # request PUT /scheduler/job/{id}?action=pause
    resp = requests.put(f"{self.url}/scheduler/job/{self.id}/status", params={"action": "pause"})
    return resp.json()
  
  def resume(self):
    # request PUT /scheduler/job/{id}?action=resume
    resp = requests.put(f"{self.url}/scheduler/job/{self.id}/status", params={"action": "resume"})
    return resp.json()
  
  def run(self):
    # request POST /scheduler/job/{id}
    resp = requests.post(f"{self.url}/scheduler/job/{self.id}")
    return resp.json()