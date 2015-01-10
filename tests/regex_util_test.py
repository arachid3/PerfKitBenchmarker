# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for perfkitbenchmarker.lib.regex_util."""

import unittest

from perfkitbenchmarker import regex_util


class ExtractGroupTestCase(unittest.TestCase):

  def testMatches(self):
    regex = r'test ([\da-f]+) text'
    string = 'test 12a3de text'
    self.assertEqual('12a3de', regex_util.ExtractGroup(regex, string, group=1))

  def testNoMatch(self):
    regex = r'test ([\da-f]+) text'
    string = 'test text'
    self.assertRaises(regex_util.NoMatchError, regex_util.ExtractGroup, regex,
                      string, group=1)

  def testMatches_Unanchored(self):
    regex = r'([\da-f]+) text'
    string = 'test 12a3de text'
    self.assertEqual('12a3de', regex_util.ExtractGroup(regex, string, group=1))

  def testNamedGroup(self):
    regex = r'test (?P<hex>[\da-f]+) text'
    string = 'test 12a3de text'
    self.assertEqual('12a3de', regex_util.ExtractGroup(regex, string,
                                                       group='hex'))

  def testNumberedGroup_Invalid(self):
    regex = r'test ([\da-f]+) (.*)'
    string = 'test 12a3de text'
    self.assertRaisesRegexp(IndexError, 'No such group 3 in',
                            regex_util.ExtractGroup, regex, string, group=3)

  def testNumberedGroup_Valid(self):
    regex = r'test ([\da-f]+) (.*)'
    string = 'test 12a3de text'
    self.assertEqual('text', regex_util.ExtractGroup(regex, string, group=2))

  def testNumberedGroup_WholeMatch(self):
    regex = r'test [\da-f]+ (.*)'
    string = 'test 12a3de text'
    self.assertEqual(string, regex_util.ExtractGroup(regex, string, group=0))


class ExtractFloatTestCase(unittest.TestCase):

  def testParsesSuccessfully(self):
    regex = r'test (\d+|\.\d+|\d+\.\d+) string'
    string = 'test 12.435 string'
    self.assertAlmostEqual(12.435, regex_util.ExtractFloat(regex, string,
                                                           group=1))

  def testRaisesValueErrorOnInvalidInput(self):
    regex = r'test (invalid_float) string'
    string = 'test invalid_float string'
    self.assertRaises(ValueError, regex_util.ExtractFloat, regex, string,
                      group=1)

if __name__ == '__main__':
  unittest.main()