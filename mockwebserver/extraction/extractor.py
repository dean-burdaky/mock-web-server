# Will contain:
#   base request extractor class
#   matcher-based extractor class
# the user will likely implement their own request data extraction code

from typing import Tuple, Optional, Sequence, Dict, Any

from twisted.web.server import Request as Tw_Request
from parse import parse as Pa_parse, Result as Pa_Result

class Extract:
  def __init__(self, fixed : Sequence[Any], named : Dict[str, Any]):
    self.fixed = fixed
    self.named = named

class Extractor:
  def extractData(self, request : Tw_Request) -> Optional[Extract]:
    raise NotImplementedError()

class PathExtractor:
  def __init__(self, pattern : str):
    self.pattern = pattern
  
  def extractData(self, request : Tw_Request) -> Optional[Extract]:
    pattern = self.pattern
    if not pattern.endswith('/'):
      pattern += '/'
    path = request.path
    if not pattern.endswith('/'):
      path += '/'
    result = Pa_search(pattern, path, case_sensitive=True)
    if not isinstance(result, Pa_Result):
      return None
    named = {}
    for key in result.named:
      if key.startswith("PATH_"):
        named[key[5:]] = result.named[key]
      else:
        if '/' in result.named[key]:
          return None
        named[key] = result.named[key]
        
    return Extract(result.fixed, named)