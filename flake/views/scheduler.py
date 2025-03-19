from ..services.scheduler import SchedulerService

class SchedulerView:
  
  def __init__(self, url: str):
    self.service = SchedulerService(url)
  
  def get_jobs(self, name: str = None):
    return self.service.get_jobs(name)
  
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