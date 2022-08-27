# Will contain:
#   base request extractor class
#   matcher-based extractor class
# the user will likely implement their own request data extraction code

from typing import Optional, Sequence, Dict, Any

from twisted.web.server import Request as Tw_Request
from parse import parse as Pa_parse, Result as Pa_Result

class Extract:
  def __init__(self, fixed : Sequence[Any], named : Dict[str, Any]):
    self.fixed = fixed
    self.named = named

class Extractor:
  def getId(self) -> str:
    raise NotImplementedError()

  def extractData(self, request : Tw_Request) -> Optional[Extract]:
    raise NotImplementedError()

class PathExtractor (Extractor):
  def __init__(self, pattern : str):
    self.pattern = pattern

  def getId(self) -> str:
    return "PATH '{}'".format(self.pattern)
  
  def extractData(self, request : Tw_Request) -> Optional[Extract]:
    if request == None:
      raise ValueError()
    pattern = self.pattern
    if len(pattern) > 0 and not pattern.endswith('/'):
      pattern += '/'
    path = request.path
    if len(path) > 0 and not path.endswith('/'):
      path += '/'
    result = Pa_parse(pattern, path, case_sensitive=True)
    return Extract(list(result.fixed), result.named) if isinstance(result, Pa_Result) else None