# Will contain:
#   base matcher class
#   path matcher
#   query matcher
#   method matcher

from enum import Enum
from typing import Sequence, Union

from twisted.web.server import Request as Tw_Request

from mockwebserver.extraction.extractor import Extract, Extractor, PathExtractor, QueryExtractor

class Matcher:
  def __init__(self, extractor : Extractor):
    self._extractor = extractor

  def getId(self) -> str:
    return self._extractor.getId()

  def matchesRequest(self, request : Tw_Request) -> bool:
    result = self._extractor.extractData(request)
    return isinstance(result, Extract)

class PathMatcher (Matcher):
  def __init__(self, pattern : str):
    super().__init__(PathExtractor(pattern))
    self.pattern = pattern

class Method (Enum):
  GET = "GET",
  HEAD = "HEAD",
  POST = "POST",
  PUT = "PUT",
  DELETE = "DELETE",
  CONNECT = "CONNECT",
  OPTIONS = "OPTIONS",
  TRACE = "TRACE",
  PATCH = "PATCH"

class MethodMatcher (Matcher):
  def __init__(self, method : Union[Method, str]):
    super().__init__(None)
    if isinstance(method, str):
      method = Method(method)
    elif method == None:
      raise ValueError()
    self.method = method

  def getId(self) -> str:
    return "METHOD {}".format(self.method.value)

  def matchesRequest(self, request: Tw_Request) -> bool:
    return request.method == bytes(self.method.value)

class QueryMatcher (Matcher):
  def __init__(self, **parameters : Sequence[str]):
    super().__init__(QueryExtractor(**parameters))
    self.parameters = parameters