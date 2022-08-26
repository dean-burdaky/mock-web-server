from http.client import INTERNAL_SERVER_ERROR
from typing import Tuple, Dict, Any

from twisted.internet.threads import deferToThread as Tw_deferToThread
from twisted.internet.defer import Deferred as Tw_Deferred
from twisted.web.resource import Resource as Tw_Resource
from twisted.web.server import Request as Tw_Request, NOT_DONE_YET as Tw_NOT_DONE_YET

from mockwebserver.core.stub import StubManager
from mockwebserver.stub import Stub
from mockwebserver.extraction.data import DTO

class RequestProcessor:
  def __init__(self, stubManager : StubManager):
    self._stubManager = stubManager

  def processRequest(self, request : Tw_Request) -> DTO:
    if request == None:
      raise ValueError()
    stub = self._stubManager.findStubForRequest(request)
    data = None
    if isinstance(stub, Stub):
      data = stub.extractData(request)
    return DTO(request, stub, data)

  def stubRender(self, dto : DTO):
    return dto.stub.render(dto.request, dto.data)

class RequestDelegator (Tw_Resource):
  isLeaf = True

  def __init__(self, stubManager : StubManager):
    self._requestProcessor = RequestProcessor(stubManager)

  def render(self, request : Tw_Request):
    if request == None:
      raise ValueError()
    deferred = Tw_deferToThread(self._requestProcessor.processRequest, request)
    if isinstance(deferred, Tw_Deferred):
      deferred.addCallback(self._requestProcessor.stubRender)
      # May need to add errback
      return Tw_NOT_DONE_YET
    else:
      request.setResponseCode(INTERNAL_SERVER_ERROR)
      return b"Failed to defer request to a thread"