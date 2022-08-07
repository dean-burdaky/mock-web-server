from twisted.internet import reactor as Tw_reactor, endpoints as Tw_endpoints
from twisted.web.server import Site as Tw_Site

from mockwebserver.core.stub import StubManager
from mockwebserver.core.request import RequestDelegator

class MockWebServer:
  def __init__(self, port : int, backlog : int = 50):
    self.port = port
    self.backlog = backlog
    self._stubManager = StubManager()
    self._requestDelegator = RequestDelegator(self._stubManager)
    self._endpoint = Tw_endpoints.TCP4ServerEndpoint(Tw_reactor, port, backlog)

  def run(self):
    site = Tw_Site(self._requestDelegator)
    self._endpoint.listen(site)
    Tw_reactor.run()