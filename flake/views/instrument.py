from ..services.instrument import InstrumentService

class InstrumentView:
  
  def __init__(self, url: str, id: str):
    self.service = InstrumentService(url, id)
  
  
  def get(self):
    return self.service.get()
  
  def remove(self):
    return self.service.remove()
  