import unittest
from unittest import mock

from mockwebserver.core.request import RequestProcessor
from mockwebserver.core.stub import StubManager
from mockwebserver.extraction.data import DTO
from mockwebserver.stub import Stub


class TestProcessRequest (unittest.TestCase):
  def setUp(self):
    self.mockData = mock.NonCallableMagicMock(dict)
    self.mockStub = Stub("id1")
    self.mockStub.extractData = mock.Mock(return_value=self.mockData)
    self.mockStubManager = StubManager()
    self.mockStubManager.findStubForRequest = mock.Mock(return_value=self.mockStub)

  def testProcessRequestWithNoRequest(self):
    request = None
    stubManager = mock.NonCallableMock()
    requestProcessor = RequestProcessor(self.mockStubManager)

    self.assertRaises(ValueError, requestProcessor.processRequest, request)
    self.mockStubManager.findStubForRequest.assert_not_called()
    self.mockStub.extractData.assert_not_called()

  def testProcessRequestWithRequestThatMatchesAStubWhichExtractsData(self):
    request = mock.NonCallableMock()
    requestProcessor = RequestProcessor(self.mockStubManager)
    
    dto = requestProcessor.processRequest(request)

    self.assertIsInstance(dto, DTO)
    self.assertEqual(dto.request, request)
    self.assertEqual(dto.stub, self.mockStub)
    self.assertEqual(dto.data, self.mockData)
    self.mockStubManager.findStubForRequest.assert_called_once_with(request)
    self.mockStub.extractData.assert_called_once_with(request)

  def testProcessRequestWithRequestThatMatchesAStubWhichFailsToExtractData(self):
    request = mock.NonCallableMock()
    self.mockStub.extractData.return_value = None
    requestProcessor = RequestProcessor(self.mockStubManager)
    
    dto = requestProcessor.processRequest(request)

    self.assertIsInstance(dto, DTO)
    self.assertEqual(dto.request, request)
    self.assertEqual(dto.stub, self.mockStub)
    self.assertIsNone(dto.data)
    self.mockStubManager.findStubForRequest.assert_called_once_with(request)
    self.mockStub.extractData.assert_called_once_with(request)

  def testProcessRequestWithRequestThatDoesNotMatchAStub(self):
    request = mock.NonCallableMock()
    self.mockStubManager.findStubForRequest.return_value = None
    requestProcessor = RequestProcessor(self.mockStubManager)
    
    dto = requestProcessor.processRequest(request)

    self.assertIsInstance(dto, DTO)
    self.assertEqual(dto.request, request)
    self.assertIsNone(dto.stub)
    self.assertIsNone(dto.data)
    self.mockStubManager.findStubForRequest.assert_called_once_with(request)
    self.mockStub.extractData.assert_not_called()