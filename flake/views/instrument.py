from ..services.instrument import InstrumentService

class InstrumentView:
  
  def __init__(self, url: str, name: str):
    self.service = InstrumentService(url, name)
  
  
  def get(self):
    return self.service.get()
  
  def get_logs(self, tail: int = 100):
    return self.service.get_logs(tail)
  
  def get_logs_stream(self, tail: int = 100):
    return self.service.get_logs_stream(tail)
  
  def remove(self):
    return self.service.remove()
  