# Will contain:
#   base matcher class
#   path matcher
#   query matcher
#   method matcher

from typing import Type

from twisted.web.server import Request as Tw_Request

from mockwebserver.extraction.extractor import Extract, Extractor
from mockwebserver.extraction.header import PathExtractor

class Matcher:
  def __init__(self, extractor : Extractor):
    self._extractor = extractor

  def matchesRequest(self, request : Tw_Request) -> bool:
    result = self._extractor.extractData(request)
    return isinstance(result, Extract)

class PathMatcher (Matcher):
  def __init__(self, pattern : str):
    super().__init__(PathExtractor(pattern))
    self.pattern = pattern