from ..services.config import ConfigService

class ConfigView:
  
  def __init__(self, url: str):
    self.service = ConfigService(url)
  
  def reload(self):
    return self.service.reload()
  
  def get_settings(self):
    return self.service.get_settings()
  
  def get_runtime(self):
    return self.service.get_runtime()
  
  def get_instruments(self):
    return self.service.get_instruments()
  
  def add_or_update_instrument(self, payload: dict):
    return self.service.add_or_update_instrument(payload)