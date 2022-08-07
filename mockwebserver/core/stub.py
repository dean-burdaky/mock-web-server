# Will contain:
#   the stub manager, which will list all stubs used
#   base stub loader class
#   manual/interactive loader class
#   auto loader class

from typing import Optional, List, Iterable, Tuple

from twisted.web.server import Request as Tw_Request

from mockwebserver.stub import Stub

BoolWithError = Tuple[bool, str]

class StubManager:
  def __init__(self):
    self._stubs = []
    self._stub_ids = []

  def getStub(self, index : int) -> Optional[Stub]:
    if index < 0 or len(self._stubs) < index:
      return False, "Argument index={} is outside of range [0, {})".format(index, len(self._stubs))
    return self._stubs[index]

  def findStubIndex(self, stubId : str) -> int:
    return self._stub_ids.index(stubId)

  def findStub(self, stubId : str) -> Optional[Stub]:
    index = self.findStubIndex(stubId)
    return self.getStub(index)

  def hasStub(self, stubId : str) -> bool:
    return self.findStubIndex(stubId) >= 0

  def addStub(self, stub : Stub) -> BoolWithError:
    if self.hasStub(stub.id):
      return False, "Stub with ID {} has already been added".format(stub.id)
    self._stubs.append(stub)
    self._stub_ids.append(stub.id)
    return True, ""

  def addStubs(self, stubs : Iterable[Stub]) -> List[BoolWithError]:
    resultList = []
    for stub in stubs
      result = self.addStub(stub)
      resultList.append(result)
    return resultList

  def insertStub(self, index : int, stub : Stub) -> BoolWithError:
    if index < 0 or len(self._stubs) < index:
      return False, "Argument index={} is outside of range [0, {})".format(index, len(self._stubs))
    if self.hasStub(stub.id):
      return False, "Stub with ID {} has already been added".format(stub.id)
    if index < len(self._stubs):
      self._stubs.insert(index, stub)
      self._stub_ids.insert(index, stub.id)
      return True, ""
    else:
      return self.addStub(stub)

  def removeStubAt(self, index : int) -> Optional[Stub]:
    if index < 0 or len(self._stubs) < index:
      return None
    stub = self._stubs.pop(index)
    del self._stub_ids[index]
    return stub

  def removeStub(self, stubId : str) -> Optional[Stub]:
    index = self.findStubIndex(stubId)
    if index < 0:
      return None
   return self.removeStubAt(index)

  def removeAllStubs(self) -> List[Stub]:
    stubs = self._stubs
    self._stubs = []
    self._stub_ids.clear()
    return stubs

  def replaceStubAt(self, index : int, stub : Stub) -> Tuple[Optional[Stub], BoolWithError]:
    if index < 0 or len(self._stubs) < index:
      return None, (False, "Argument index={} is outside of range [0, {})".format(index, len(self._stubs)))
    oldStubId = self_stubs[index].id
    if oldStubId != stub.id and self.hasStub(stub.id):
      return None, (False, "New Stub ID {} is already in use".format(stub.id))
    oldStub = self.removeStub(oldStubId)
    inserted, error = self.insertStub(index, stub)
    return oldStub, (inserted, error)

  def replaceStub(self, oldStub : Stub, newStub : Stub) -> Tuple[Optional[Stub], BoolWithError]:
    index = self.findStubIndex(oldStub.id)
    if index < 0:
      return None, (False, "Could not find old stub with ID {}".format(oldStub.id))
    return self.replaceStubAt(index)

  def findStubForRequest(self, request : Tw_Request) -> Optional[Stub]:
    for stub in self._stubs:
      if stub.matchesRequest(request):
        return stub
    return None
