# Will contain:
#   general user-facing global functions for stubs
#   the base stub class that all stubs should be derived from
#   the default stub class that can be derived from (will still have to implement the render function)

from twisted.web.server import Request as Tw_Request

from mockwebserver.extraction.data import Data

class Stub:
  def __init__(self, id : str):
    self.id = id

  def render(self, request : Tw_Request):
    raise NotImplementedError()

  def matchesRequest(self, request : Tw_Request) -> bool:
    raise NotImplementedError()

  def extractData(self, request : Tw_Request) -> Data:
    raise NotImplementedError()

class DefaultStub (Stub):
  def __init__(self, id : str, *matchers : Matcher):