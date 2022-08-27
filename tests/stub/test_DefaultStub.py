import unittest
from unittest import mock

from mockwebserver.stub import DefaultStub
from mockwebserver.extraction.extractor import PathExtractor
from mockwebserver.matching.matcher import Matcher, PathMatcher

class TestInit (unittest.TestCase):
  def testInit(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher = PathMatcher("/my/default/stub/matcher")
    extractor = PathExtractor("/my/default/stub/extractor")

    stub = DefaultStub(stubId, renderCallable, matcher, extractor)

    self.assertEqual(stub.id, stubId)
    self.assertEqual(stub.renderCallable, renderCallable)
    self.assertListEqual(stub.matchers, [matcher])
    self.assertListEqual(stub.extractors, [extractor])

  def testInitWithNoId(self):
    stubId = None
    renderCallable = mock.Mock()
    matcher = PathMatcher("/my/default/stub/matcher")
    extractor = PathExtractor("/my/default/stub/extractor")

    self.assertRaises(ValueError, DefaultStub, stubId, renderCallable, matcher, extractor)

  def testInitWithNoCallable(self):
    stubId = "defaultStub"
    renderCallable = None
    matcher = PathMatcher("/my/default/stub/matcher")
    extractor = PathExtractor("/my/default/stub/extractor")

    self.assertRaises(ValueError, DefaultStub, stubId, renderCallable, matcher, extractor)

  def testInitWithNoneMatcher(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher = None
    extractor = PathExtractor("/my/default/stub/extractor")

    self.assertRaises(ValueError, DefaultStub, stubId, renderCallable, matcher, extractor)

  def testInitWithNoneExtractor(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher = PathMatcher("/my/default/stub/matcher")
    extractor = None

    self.assertRaises(ValueError, DefaultStub, stubId, renderCallable, matcher, extractor)

  def testInitWithOnlyMatcher(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher = PathMatcher("/my/default/stub/matcher")

    stub = DefaultStub(stubId, renderCallable, matcher)

    self.assertEqual(stub.id, stubId)
    self.assertEqual(stub.renderCallable, renderCallable)
    self.assertListEqual(stub.matchers, [matcher])
    self.assertListEqual(stub.extractors, [])

  def testInitWithOnlyExtractor(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    extractor = PathExtractor("/my/default/stub/extractor")

    stub = DefaultStub(stubId, renderCallable, extractor)

    self.assertEqual(stub.id, stubId)
    self.assertEqual(stub.renderCallable, renderCallable)
    self.assertListEqual(stub.matchers, [])
    self.assertListEqual(stub.extractors, [extractor])

  def testInitWithMultipleMatchers(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher1 = PathMatcher("/my/first/default/stub/matcher")
    matcher2 = PathMatcher("/my/second/default/stub/matcher")
    extractor = PathExtractor("/my/default/stub/extractor")

    stub = DefaultStub(stubId, renderCallable, matcher1, extractor, matcher2)

    self.assertEqual(stub.id, stubId)
    self.assertEqual(stub.renderCallable, renderCallable)
    self.assertListEqual(stub.matchers, [matcher1, matcher2])
    self.assertListEqual(stub.extractors, [extractor])

  def testInitWithMultipleExtractors(self):
    stubId = "defaultStub"
    renderCallable = mock.Mock()
    matcher = PathMatcher("/my/default/stub/matcher")
    extractor1 = PathExtractor("/my/first/default/stub/extractor")
    extractor2 = PathExtractor("/my/second/default/stub/extractor")

    stub = DefaultStub(stubId, renderCallable, matcher, extractor2, extractor1)

    self.assertEqual(stub.id, stubId)
    self.assertEqual(stub.renderCallable, renderCallable)
    self.assertListEqual(stub.matchers, [matcher])
    self.assertListEqual(stub.extractors, [extractor2, extractor1])

class TestMatchesRequest (unittest.TestCase):
  def setUp(self):
    self.stubId = "defaultStub"
    self.renderCallable = mock.Mock()
    self.matcher1 = mock.NonCallableMock(Matcher)
    self.matcher1.matchesRequest = mock.Mock(return_value=False)
    self.matcher2 = mock.NonCallableMock(Matcher)
    self.matcher2.matchesRequest = mock.Mock(return_value=False)
    self.matcher3 = mock.NonCallableMock(Matcher)
    self.matcher3.matchesRequest = mock.Mock(return_value=False)
    self.matcher4 = mock.NonCallableMock(Matcher)
    self.matcher4.matchesRequest = mock.Mock(return_value=False)
    

  def testMatchesRequestWithNoRequest(self):
    request = None
    stub = DefaultStub(self.stubId, self.renderCallable, self.matcher1, self.matcher2, self.matcher3, self.matcher4)

    self.assertRaises(ValueError, stub.matchesRequest, request)

  def testMatchesRequestWithAllMatchersMatching(self):
    request = mock.NonCallableMock()
    self.matcher1.matchesRequest.return_value = True
    self.matcher2.matchesRequest.return_value = True
    self.matcher3.matchesRequest.return_value = True
    self.matcher4.matchesRequest.return_value = True
    stub = DefaultStub(self.stubId, self.renderCallable, self.matcher1, self.matcher2, self.matcher3, self.matcher4)

    matches = stub.matchesRequest(request)

    self.assertTrue(matches)
    self.matcher1.matchesRequest.assert_called_once_with(request)
    self.matcher2.matchesRequest.assert_called_once_with(request)
    self.matcher3.matchesRequest.assert_called_once_with(request)
    self.matcher4.matchesRequest.assert_called_once_with(request)

  def testMatchesRequestWithAllButOneMatcherMatching(self):
    request = mock.NonCallableMock()
    self.matcher1.matchesRequest.return_value = True
    self.matcher2.matchesRequest.return_value = True
    self.matcher3.matchesRequest.return_value = True
    stub = DefaultStub(self.stubId, self.renderCallable, self.matcher1, self.matcher2, self.matcher3, self.matcher4)

    matches = stub.matchesRequest(request)

    self.assertFalse(matches)
    self.matcher4.matchesRequest.assert_called_once_with(request)

  def testMatchesRequestWithOneMatcherMatching(self):
    request = mock.NonCallableMock()
    self.matcher1.matchesRequest.return_value = True
    stub = DefaultStub(self.stubId, self.renderCallable, self.matcher1, self.matcher2, self.matcher3, self.matcher4)

    matches = stub.matchesRequest(request)

    self.assertFalse(matches)
    self.matcher1.matchesRequest.assert_called_once_with(request)
    self.matcher2.matchesRequest.assert_called_once_with(request)

  def testInitWithNoMatchersMatching(self):
    request = mock.NonCallableMock()
    stub = DefaultStub(self.stubId, self.renderCallable, self.matcher1, self.matcher2, self.matcher3, self.matcher4)

    matches = stub.matchesRequest(request)

    self.assertFalse(matches)
    self.matcher1.matchesRequest.assert_called_once_with(request)