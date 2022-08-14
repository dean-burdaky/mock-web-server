# Will contain:
#   base matcher class
#   path matcher
#   query matcher
#   method matcher

from typing import Type

from twisted.web.server import Request as Tw_Request

from mockwebserver.extraction.extractor import Extract, Extractor, PathExtractor

class Matcher:
  def __init__(self, extractor : Extractor):
    self._extractor = extractor

  def matchesRequest(self, request : Tw_Request) -> bool:
    result = self._extractor.extractData(request)
    return isinstance(result, Extract)

class PathMatcher (Matcher):
  def __init__(self, pattern : str, fixedStart : bool = True, fixedEnd : bool = True, caseSensitive : bool = True):
    super().__init__(PathExtractor(pattern, fixedStart, fixedEnd, caseSensitive))
    self.pattern = pattern
    self.fixedStart = fixedStart
    self.fixedEnd = fixedEnd
    self.caseSensitive = caseSensitive