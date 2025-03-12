from ..services.job import JobService

class JobView:
  
  def __init__(self, url: str, id: str):
    self.service = JobService(url, id)
  
  def get(self):
    return self.service.get()
  
  def get_status(self):
    return self.service.get_status()
  
  def start(self):
    return self.service.start()
  
  def stop(self):
    return self.service.stop()
  
  def restart(self):
    self.stop()
    return self.start()
  
  def pause(self):
    return self.service.pause()
  
  def resume(self):
    return self.service.resume()