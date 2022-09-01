# Will contain:
#   base request extractor class
#   matcher-based extractor class
# the user will likely implement their own request data extraction code

import re
from typing import Optional, Sequence, Dict, Any, Union

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
  def __init__(self, matchSubset : bool = True, **parameters : Sequence[str]):
    self.matchSubset = matchSubset
    self.parameters = parameters

  def getId(self) -> str:
    return "QUERY {}".format(self.parameters)

  def extractData(self, request: Tw_Request) -> Optional[Extract]:
    if request == None:
      raise ValueError()
    elif len(self.parameters) > len(request.args):
      return None
    elif not self.matchSubset and len(self.parameters) < len(request.args):
      return None
    params = request.args.copy()
    extract = Extract([], {})
    for patternKey in self.parameters:
      keyResult = None
      valueResult = None
      matchingRequestKey = None
      for requestKey in params:
        keyResult = Pa_parse(patternKey, requestKey, case_sensitive=True)
        if not isinstance(keyResult, Pa_Result):
          continue
        patternValues = self.parameters[patternKey]
        requestValues = params[requestKey]
        if len(patternValues) > len(requestValues):
          continue
        elif not self.matchSubset and len(patternValues) < len(requestValues):
          continue
        for index in range(len(patternValues)):
          valueResult = Pa_parse(patternValues[index], requestValues[index], case_sensitive=True)
          if isinstance(valueResult, Pa_Result):
            matchingRequestKey = requestKey
            break
      if isinstance(keyResult, Pa_Result) and isinstance(valueResult, Pa_Result) and params.pop(matchingRequestKey, None) != None:
        extract.fixed.extend(list(keyResult.fixed))
        extract.fixed.extend(list(valueResult.fixed))
        extract.named.update(keyResult.named)
        extract.named.update(valueResult.named)
      else:
        return None
    return extract
      


