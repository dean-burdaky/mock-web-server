import unittest
from unittest import mock

from mockwebserver.stub import Stub
from mockwebserver.core.stub import StubManager

class TestAddStub (unittest.TestCase):
  def testAddStubWithNone(self):
    stub = None
    stubManager = StubManager()

    self.assertRaises(ValueError, stubManager.addStub, stub)

  def testAddStubWithNewStub(self):
    stub = Stub("id1")
    stubManager = StubManager()

    success, error = stubManager.addStub(stub)

    self.assertTrue(success)
    self.assertEqual(len(error), 0)

  def testAddStubWithOldStub(self):
    stub1 = Stub("id1")
    stub2 = Stub("id1")
    stubManager = StubManager()
    stubManager._stubs.append(stub1)
    stubManager._stub_ids.append(stub1.id)

    success, error = stubManager.addStub(stub2)

    self.assertFalse(success)
    self.assertEqual(error, "Stub with ID id1 has already been added")

  def testaddStubWithDifferentStub(self):
    stub1 = Stub("id1")
    stub2 = Stub("id2")
    stubManager = StubManager()
    stubManager._stubs.append(stub1)
    stubManager._stub_ids.append(stub1.id)

    success, error = stubManager.addStub(stub2)

    self.assertTrue(success)
    self.assertEqual(len(error), 0)

class TestAddStubs (unittest.TestCase):
  def testAddStubsWithNone(self):
    stubs = None
    stubManager = StubManager()

    self.assertRaises(ValueError, stubManager.addStubs, stubs)

  def testAddStubsWithOnlyNewStubs(self):
    stubs = [Stub("id1"), Stub("id2"), Stub("id3")]
    stubManager = StubManager()

    self.assertListEqual(stubManager.addStubs(stubs), [(True, ''), (True, ''), (True, '')])

    self.assertEqual(len(stubManager._stubs), 3)
    self.assertEqual(len(stubManager._stub_ids), 3)

  def testAddStubsWithSomeNullStubs(self):
    stubs = [Stub("id1"), Stub("id2"), None]
    stubManager = StubManager()

    self.assertListEqual(stubManager.addStubs(stubs), [(True, ''), (True, ''), (False, "Item is not a stub")])

    self.assertEqual(len(stubManager._stubs), 2)
    self.assertEqual(len(stubManager._stub_ids), 2)

  def testAddStubWithSomeNewStubsAndSomeOldStubs(self):
    oldStubs = [Stub("id1")]
    newStubs = [Stub("id2"), Stub("id3")]
    newStubs.extend(oldStubs)
    stubManager = StubManager()
    stubManager._stubs.extend(oldStubs)
    stubManager._stub_ids.extend([ oldStub.id for oldStub in oldStubs ])

    self.assertListEqual(
      stubManager.addStubs(newStubs),
      [(True, ''), (True, ''), (False, "Stub with ID id1 has already been added")]
    )

    self.assertEqual(stubManager._stubs.count(oldStubs[0]), 1)
    self.assertEqual(stubManager._stub_ids.count(oldStubs[0].id), 1)

  def testaddStubsWithDifferentStubs(self):
    oldStubs = [Stub("id1"), Stub("id2")]
    newStubs = [Stub("id3"), Stub("id4")]
    stubManager = StubManager()
    stubManager._stubs.extend(oldStubs)
    stubManager._stub_ids.extend([ oldStub.id for oldStub in oldStubs ])

    self.assertListEqual(stubManager.addStubs(newStubs), [(True, ''), (True, '')])

    self.assertEqual(len(stubManager._stubs), 4)
    self.assertEqual(len(stubManager._stub_ids), 4)

class TestFindStubForRequest (unittest.TestCase):
  def testFindStubForRequestWithNone(self):
    request = None
    stub = Stub("id1")
    stub.matchesRequest = mock.Mock(return_value=True)
    stubManager = StubManager()
    stubManager.addStub(stub)

    self.assertRaises(ValueError, stubManager.findStubForRequest, request)
    stub.matchesRequest.assert_not_called()

  def testFindStubForRequestWithEmptyStubManager(self):
    request = mock.NonCallableMock()
    stubManager = StubManager()

    stub = stubManager.findStubForRequest(request)

    self.assertIsNone(stub)

  def testFindStubForRequestThatMatchesOnlyOnce(self):
    request = mock.NonCallableMock()
    stub1 = Stub("id1")
    stub2 = Stub("id2")
    stub3 = Stub("id3")
    stub1.matchesRequest = mock.Mock(return_value=False)
    stub2.matchesRequest = mock.Mock(return_value=True)
    stub3.matchesRequest = mock.Mock(return_value=False)
    stubManager = StubManager()
    stubManager.addStubs([stub1, stub2, stub3])

    stub = stubManager.findStubForRequest(request)

    self.assertEqual(stub, stub2)
    stub2.matchesRequest.assert_called_once_with(request)

  def testFindStubForRequestThatMatchesTwice(self):
    request = mock.NonCallableMock()
    stub1 = Stub("id1")
    stub2 = Stub("id2")
    stub3 = Stub("id3")
    stub1.matchesRequest = mock.Mock(return_value=True)
    stub2.matchesRequest = mock.Mock(return_value=False)
    stub3.matchesRequest = mock.Mock(return_value=True)
    stubManager = StubManager()
    stubManager.addStubs([stub1, stub2, stub3])

    stub = stubManager.findStubForRequest(request)

    self.assertEqual(stub, stub1)
    stub1.matchesRequest.assert_called_once_with(request)

  def testFindStubForRequestThatNeverMatches(self):
    request = mock.NonCallableMock()
    stub1 = Stub("id1")
    stub2 = Stub("id2")
    stub3 = Stub("id3")
    stub1.matchesRequest = mock.Mock(return_value=False)
    stub2.matchesRequest = mock.Mock(return_value=False)
    stub3.matchesRequest = mock.Mock(return_value=False)
    stubManager = StubManager()
    stubManager.addStubs([stub1, stub2, stub3])

    stub = stubManager.findStubForRequest(request)

    self.assertIsNone(stub)
    stub1.matchesRequest.assert_called_once_with(request)
    stub2.matchesRequest.assert_called_once_with(request)
    stub3.matchesRequest.assert_called_once_with(request)

if __name__ == "__main__":
  unittest.main()