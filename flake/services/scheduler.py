import requests

class SchedulerService:
  
  def __init__(self, url: str):
    self.url = url
  
  def get_jobs(self, name: str = None):
    # request GET /scheduler/jobs
    resp = requests.get(f"{self.url}/scheduler/jobs", params={"name": name})
    return resp.json()
  
  def get_status(self):
    # request GET /scheduler/status
    try:
      resp = requests.get(f"{self.url}/scheduler/status")
      return resp.json()
    except Exception as e:
      return {"status": "error", "message": str(e)}
  
  def start(self):
    # request PUT /scheduler?action=start
    resp = requests.put(f"{self.url}/scheduler/status", params={"action": "start"})
    return resp.json()
  
  def stop(self):
    # request PUT /scheduler?action=stop
    resp = requests.put(f"{self.url}/scheduler/status", params={"action": "stop"})
    return resp.json()
  
  def pause(self):
    # request PUT /scheduler?action=pause
    resp = requests.put(f"{self.url}/scheduler/status", params={"action": "pause"})
    return resp.json()
  
  def resume(self):
    # request PUT /scheduler?action=resume
    resp = requests.put(f"{self.url}/scheduler/status", params={"action": "resume"})
    return resp.json()