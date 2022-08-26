from typing import Tuple, Dict, Any

from twisted.web.server import Request as Tw_Request

from mockwebserver.stub import Stub

class DTO:
  def __init__(self, request : Tw_Request, stub : Stub, data : Dict[str, Any]):
    self.request = request
    self.stub = stub
    self.data = data