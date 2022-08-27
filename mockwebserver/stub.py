# Will contain:
#   general user-facing global functions for stubs
#   the base stub class that all stubs should be derived from
#   the default stub class that can be derived from (will still have to implement the render function)

from typing import Callable, Dict, Any, Union

from twisted.web.server import Request as Tw_Request

from mockwebserver.extraction.extractor import Extractor
from mockwebserver.matching.matcher import Matcher

class Stub:
  def __init__(self, stubId : str):
    if stubId == None:
      raise ValueError()
    self.id = stubId

  def render(self, request : Tw_Request, data : Dict[str, Any]):
    raise NotImplementedError()

  def matchesRequest(self, request : Tw_Request) -> bool:
    raise NotImplementedError()

  def extractData(self, request : Tw_Request) -> Dict[str, Any]:
    raise NotImplementedError()

class DefaultStub (Stub):
  def __init__(self, \
               stubId : str, \
               renderCallable : Callable[[Tw_Request, Dict[str, Any]], Any], \
               *objects : Union[Matcher, Extractor]):
    super().__init__(stubId)
    if renderCallable == None:
      raise ValueError()
    self.renderCallable = renderCallable
    self.matchers = []
    self.extractors = []
    for obj in objects:
      if isinstance(obj, Matcher):
        self.matchers.append(obj)
      elif isinstance(obj, Extractor):
        self.extractors.append(obj)
      else:
        raise ValueError()

  def matchesRequest(self, request: Tw_Request) -> bool:
    if request == None:
      raise ValueError()
    for matcher in self.matchers:
      if not matcher.matchesRequest(request):
        return False
    return True

  def extractData(self, request: Tw_Request) -> Dict[str, Any]:
    data = {}
    for extractor in self.extractors:
      if not extractor.getId() in data:
        data[extractor.getId()] = extractor.extractData(request)
    return data

  def render(self, request : Tw_Request, data : Dict[str, Any]):
    return self.renderCallable(request, data)