# Will contain:
#   base request extractor class
#   matcher-based extractor class
# the user will likely implement their own request data extraction code

from typing import Tuple, Optional, Sequence, Dict, Any

from twisted.web.server import Request as Tw_Request
from parse import search as Pa_search, Result as Pa_Result

class Extract:
  def __init__(self, fixed : Sequence[Any], named : Dict[str, Any]):
    self.fixed = fixed
    self.named = named

class Extractor:
  def extractData(self, request : Tw_Request) -> Optional[Extract]:
    raise NotImplementedError()

class PathExtractor:
  def __init__(self, pattern : str, fixedStart : bool = True, fixedEnd : bool = True, caseSensitive : bool = True):
    self.pattern = pattern
    self.fixedStart = fixedStart
    self.fixedEnd = fixedEnd
    self.caseSensitive = caseSensitive
  
  def extractData(self, request : Tw_Request, calcRegion : bool = False) -> Optional[Extract]:
    anyCounter = 0
    pattern = self.pattern
    path = request.path
    if path[-1] != '/':
      path += '/'
    if self.fixedEnd and pattern[-1] != '/':
      pattern += '/'
    index = 0
    while index >= 0:
      index = pattern.find("{_any}", index)
      if index >= 0:
        closeIndex = pattern.find('}', index)
        pattern = pattern[:closeIndex] + str(anyCounter) + pattern[closeIndex:]
        anyCounter += 1
        index = closeIndex
    if self.fixedStart:
      pattern = "::START::/" + pattern
      path = "::START::/" + path
    if self.fixedEnd:
      pattern += "/::END::"
      path += "/::END::"
    result = Pa_search(pattern, path, case_sensitive=self.caseSensitive)
    return Extract(result.fixed, result.named) if isinstance(result, Pa_Result) else None