#!/usr/bin/env python

import json
import unittest

import requests
import urllib2

from app import jsonapi_constants


class JSONApiTestCase(unittest.TestCase):
    def test_site_is_online(self):
        response = requests.get(jsonapi_constants.BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_keys_exist_in_record(self):
        json_data = json.loads(urllib2.urlopen(jsonapi_constants.FIRST_RECORD).read())

        for key in jsonapi_constants.RECORD_KEYS:
            assert key in json_data.keys()

    def test_count_of_records(self):
        list_json_data = json.loads(urllib2.urlopen(jsonapi_constants.ALL_RECORDS).read())
        self.assertEquals(len(list_json_data), jsonapi_constants.ALL_RECORDS_LENGTH)

    def test_ids_are_unique(self):
        list_json_data = json.loads(urllib2.urlopen(jsonapi_constants.ALL_RECORDS).read())

        list_of_ids = []
        for json_data in list_json_data:
            list_of_ids.append(json_data['id'])

        self.assertEquals(len(list_of_ids), len(list_json_data))
