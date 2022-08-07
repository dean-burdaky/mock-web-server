from typing import Tuple, Dict, Any

from twisted.web.server import Request as Tw_Request

from mockwebserver.stub import Stub

Data = Dict[str, Any]
DTO = Tuple[server.Request, stub.Stub, Data]

class DTO:
  def __init__(self, request : Tw_Request, stub : Stub, data : Data):
    self.request = request
    self.stub = stub
    self.data = data