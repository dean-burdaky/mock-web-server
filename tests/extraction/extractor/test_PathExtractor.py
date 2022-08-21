import unittest
from unittest import mock

from mockwebserver.extraction.extractor import Extract, PathExtractor

class TestExtractData (unittest.TestCase):
  def testExtractDataWithNonEmptyPatternNullRequest(self):
    testPattern = "/this/is/a/test/path"
    testRequest = None

    extractor = PathExtractor(testPattern)
    self.assertRaises(ValueError, extractor.extractData, testRequest)

  def testExtractDataWithEmptyPatternEmptyPath(self):
    testPattern = ""
    testRequest = mock.NonCallableMock()
    testRequest.path = ""

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithEmptyPatternNonEmptyPath(self):
    testPattern = ""
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsNone(extract)

  def testExtractDataWithExactPatternSamePath(self):
    testPattern = "/this/is/a/test/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = testPattern

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithExactPatternDifferentPath(self):
    testPattern = "/this/is/a/test/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/different/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsNone(extract)

  def testExtractDataWithExactPatternWithEndSlashSamePathWithoutEndSlash(self):
    path = "/this/is/a/test/path"
    testPattern = path + '/'
    testRequest = mock.NonCallableMock()
    testRequest.path = path

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithExactPatternWithoutEndSlashSamePathWithEndSlash(self):
    path = "/this/is/a/test/path"
    testPattern = path
    testRequest = mock.NonCallableMock()
    testRequest.path = path + '/'

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithPositionalPathVarPatternMatchingPath(self):
    testPattern = "/this/is/a/{}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["test"])
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithPositionalPathVarPatternNonMatchingPath(self):
    testPattern = "/this/is/a/{}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/the/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsNone(extract)

  def testExtractDataWithTwoPositionalPathVarPatternMatchingPath(self):
    testPattern = "/this/is/{}/{}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["a", "test"])
    aPos = extract.fixed.index("a")
    testPos = extract.fixed.index("test")
    self.assertLess(aPos, testPos)
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithNamedPathVarPatternMatchingPath(self):
    testPattern = "/this/is/a/{var1}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertDictEqual(extract.named, {"var1": "test"})

  def testExtractDataWithNamedPathVarPatternNonMatchingPath(self):
    testPattern = "/this/is/a/{var1}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/the/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsNone(extract)

  def testExtractDataWithTwoNamedPathVarPatternMatchingPath(self):
    testPattern = "/this/is/{var1}/{var2}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertEqual(len(extract.fixed), 0)
    self.assertDictEqual(extract.named, {"var1": "a", "var2": "test"})

  def testExtractDataWithPathVarForTwoNodesPatternMatchingPath(self):
    testPattern = "/this/is/{}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["a/test"])
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithStartingPathVarPatternMatchingPath(self):
    testPattern = "{}/a/test/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["/this/is"])
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithEndingPathVarPatternMatchingPath(self):
    testPattern = "/this/is/a/{}"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["test/path"])
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithFreeformPatternMatchingPathTwice(self):
    testPattern = "{}/test/path/{}"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/path/with/an/additional/test/path/if/i/add/another/test/path/how/many/do/i/have"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, [
      "/this/is/a",
      "with/an/additional/test/path/if/i/add/another/test/path/how/many/do/i/have"
    ])
    self.assertEqual(len(extract.named), 0)

  def testExtractDataWithFreeformPatternMatchingPathTwice(self):
    testPattern = "{}/test/{intermediate}/path/{}"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/test/very/big/path/with/an/additional/test/small/path" \
                       "/if/i/add/another/test/incredible/path/how/many/do/i/have"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, [
      "/this/is/a",
      "with/an/additional/test/small/path/if/i/add/another/test/incredible/path/how/many/do/i/have"
    ])
    self.assertDictEqual(extract.named, {"intermediate": "very/big"})

  def testExtractDataWithPartialNodePathVarPatternMatchingPath(self):
    testPattern = "/this/is/a/test{}/path"
    testRequest = mock.NonCallableMock()
    testRequest.path = "/this/is/a/testing/path"

    extractor = PathExtractor(testPattern)
    extract = extractor.extractData(testRequest)

    self.assertIsInstance(extract, Extract)
    self.assertListEqual(extract.fixed, ["ing"])
    self.assertEqual(len(extract.named), 0)

if __name__ == "__main__":
  unittest.main()