# Will contain:
#   base request extractor class
#   matcher-based extractor class
# the user will likely implement their own request data extraction code

import re
from typing import Optional, Sequence, Dict, Any, Tuple

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

class QueryExtractor (Extractor):
  _didNotPop = object()
  
  def __init__(self, matchSubset : bool = True, *parameters : Tuple[str, Any]):
    self.matchSubset = matchSubset
    self.parameters = parameters

  def getId(self) -> str:
    return "QUERY {}".format(self.parameters)

  def extractData(self, request: Tw_Request) -> Optional[Extract]:
    if request == None:
      raise ValueError()
    params = []
    for key in request.args:
      for item in request.args[key]:
        params.append((key, item))
    if len(self.parameters) > len(params):
      return None
    elif not self.matchSubset and len(self.parameters) < len(params):
      return None
    extract = Extract([], {})
    for patternKey, patternValue in self.parameters:
      keyResult = None
      valueResult = None
      matchingRequestKey = None
      for requestKey, requestValue in params:
        keyResult = Pa_parse(patternKey, requestKey, case_sensitive=True)
        if not isinstance(keyResult, Pa_Result):
          continue
        valueResult = Pa_parse(patternValue, requestValue, case_sensitive=True)
        if not isinstance(valueResult, Pa_Result):
          continue
        matchingRequestKey = requestKey
        break
      if not isinstance(matchingRequestKey, str) or params.pop(requestKey, self._didNotPop) == self._didNotPop:
        return None
      extract.fixed.extend(list(keyResult.fixed))
      extract.fixed.extend(list(valueResult.fixed))
      extract.named.update(keyResult.named)
      extract.named.update(valueResult.named)
    return extract
      


