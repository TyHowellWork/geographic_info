#!/usr/bin/env python

PKG='geodesy'
import roslib; roslib.load_manifest(PKG)

import sys
import unittest

from geodesy.props import *     # module being tested

from geographic_msgs.msg import KeyValue
from geographic_msgs.msg import MapFeature
from geographic_msgs.msg import RouteSegment
from geographic_msgs.msg import WayPoint

class TestPythonProps(unittest.TestCase):
    """Unit tests for Python KeyValue property handling.
    """

    def test_empty_feature_match(self):
        f = MapFeature()
        self.assertIsNone(match(f, set(['no', 'such', 'property'])))

    def test_empty_property_set(self):
        f = MapFeature()
        put(f, 'valid', 'any')
        self.assertIsNone(match(f, set()))

    def test_feature_match(self):
        f = MapFeature()
        put(f, 'different')
        put(f, 'valid', 'any')
        prop = match(f, set(['a', 'valid', 'property']))
        self.assertIsNotNone(prop)
        self.assertEqual(prop, ('valid', 'any'))
        k, v = prop
        self.assertEqual(k, 'valid')
        self.assertEqual(v, 'any')

    def test_empty_waypoint_match(self):
        p = WayPoint()
        self.assertIsNone(match(p, set(['nothing', 'defined'])))

    def test_waypoint_match(self):
        p = WayPoint()
        put(p, 'another', 'anything')
        put(p, 'name', 'myself')
        prop = match(p, set(['name']))
        self.assertIsNotNone(prop)
        k, v = prop
        self.assertEqual(k, 'name')
        self.assertEqual(v, 'myself')

    def test_segment_value_change(self):
        s = RouteSegment()
        put(s, 'another', 'anything')
        put(s, 'name', 'myself')
        self.assertEqual(get(s, 'name'), 'myself')
        put(s, 'name', 'alias')
        self.assertEqual(get(s, 'name'), 'alias')

    def test_segment_null_value(self):
        s = RouteSegment()
        put(s, 'another', 'anything')
        put(s, 'name')
        self.assertEqual(get(s, 'name'), '')
        put(s, 'name', 'myself')
        self.assertEqual(get(s, 'name'), 'myself')

    def test_invalid_key_set(self):
        f = MapFeature()
        put(f, 'notset', 'any')
        self.assertEqual(get(f, 'notset'), 'any')
        self.assertRaises(ValueError, match, f, 'notset')

if __name__ == '__main__':
    import rosunit
    rosunit.unitrun(PKG, 'test_uuid_py', TestPythonProps) 
