import unittest
from unittest import mock

from http.client import INTERNAL_SERVER_ERROR
from twisted.web.server import NOT_DONE_YET as Tw_NOT_DONE_YET
from twisted.internet.defer import Deferred as Tw_Deferred

from mockwebserver.core.request import RequestDelegator
from mockwebserver.core.stub import StubManager
from mockwebserver.extraction.data import DTO
from mockwebserver.stub import Stub

class TestRender (unittest.TestCase):
  def testRenderWithNoRequest(self):
    request = None
    stubManager = mock.NonCallableMock()
    requestDelegator = RequestDelegator(stubManager)
    passed = False
    with mock.patch("mockwebserver.core.request.Tw_deferToThread") as Mock_Tw_deferToThread:
      self.assertRaises(ValueError, requestDelegator.render, request)
      Mock_Tw_deferToThread.assert_not_called()
      passed = True
    self.assertTrue(passed)

  def testRenderWithTwistedDeferingToThreadAndAddingCallbackOk(self):
    request = mock.NonCallableMock()
    stubManager = mock.NonCallableMock()
    requestDelegator = RequestDelegator(stubManager)
    literal = None
    with mock.patch("mockwebserver.core.request.Tw_deferToThread") as Mock_Tw_deferToThread:
      mockDefered = mock.NonCallableMock(Tw_Deferred)
      mockDefered.addCallback = mock.Mock(return_value=mockDefered)
      Mock_Tw_deferToThread.return_value = mockDefered

      literal = requestDelegator.render(request)

      Mock_Tw_deferToThread.assert_called_once_with(requestDelegator._requestProcessor.processRequest, request)
      mockDefered.addCallback.assert_called_once_with(requestDelegator._requestProcessor.stubRender)
    self.assertEqual(literal, Tw_NOT_DONE_YET)

  def testRenderWithTwistedDeferingToThreadFailed(self):
    request = mock.NonCallableMock()
    request.setResponseCode = mock.Mock()
    stubManager = mock.NonCallableMock()
    requestDelegator = RequestDelegator(stubManager)
    literal = None
    with mock.patch("mockwebserver.core.request.Tw_deferToThread") as Mock_Tw_deferToThread:
      Mock_Tw_deferToThread.return_value = None

      literal = requestDelegator.render(request)

      Mock_Tw_deferToThread.assert_called_once_with(requestDelegator._requestProcessor.processRequest, request)
    self.assertIsInstance(literal, bytes)
    self.assertRegex(literal.decode(), "Failed to defer request to (a )?thread")
    request.setResponseCode.assert_called_once_with(INTERNAL_SERVER_ERROR)

  def testRenderWithAddingCallbackFailed(self):
    request = mock.NonCallableMock()
    stubManager = mock.NonCallableMock()
    requestDelegator = RequestDelegator(stubManager)
    literal = None
    with mock.patch("mockwebserver.core.request.Tw_deferToThread") as Mock_Tw_deferToThread:
      mockDefered = mock.NonCallableMock(Tw_Deferred)
      mockDefered.addCallback = mock.Mock(return_value=None)
      Mock_Tw_deferToThread.return_value = mockDefered

      literal = requestDelegator.render(request)

      Mock_Tw_deferToThread.assert_called_once_with(requestDelegator._requestProcessor.processRequest, request)
      mockDefered.addCallback.assert_called_once_with(requestDelegator._requestProcessor.stubRender)
    self.assertIsInstance(literal, bytes)
    self.assertRegex(literal.decode(), "Failed to add call( )?back to deferred( object)?")
    request.setResponseCode.assert_called_once_with(INTERNAL_SERVER_ERROR)