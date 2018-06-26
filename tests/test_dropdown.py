#!/usr/bin/env python

import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select
import requests
import os.path

from app import dropdown_constants

class DropdownTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_file_exists(self):
        assert os.path.exists(dropdown_constants.URL)
        #r = requests.get('https://www.google.com')
        #self.assertEqual(r.status_code, 200)

    def test_dropdown_exists(self):
        driver = self.driver
        driver.get(dropdown_constants.URL)

        elements = driver.find_elements_by_id('states')
        assert (len(elements) > 0)

    def test_dropdown_contains_state_names(self):
        driver = self.driver
        driver.get(dropdown_constants.URL)

        states_dropdown = Select(driver.find_element_by_id('states'))
        states = states_dropdown.options

        for state in states:
            assert state.text.upper() in (state_name.upper() for state_name in dropdown_constants.STATE_LIST)
