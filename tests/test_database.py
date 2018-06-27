#!/usr/bin/env python

import unittest
import sqlite3
import pandas

from app import database_constants


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(database_constants.DATABASE_LOCATION)

    def tearDown(self):
        self.connection.close()

    def test_connection_succeeded(self):
        self.assertEqual(type(self.connection).__name__, 'Connection')

    def test_tables_exist(self):
        cursor = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")

        list_of_tables = []
        for element in cursor.fetchall():
            list_of_tables.append(element[0])

        for table in database_constants.DATABASE_TABLES:
            assert table in list_of_tables

    def test_genre_columns_exists(self):
        cursor = self.connection.execute('select * from genres')

        column_names = [column_name[0] for column_name in cursor.description]

        for column in database_constants.GENRES_COLUMNS:
            assert column in column_names

    def test_row_exists(self):
        insert_cursor = self.connection.cursor()

        rows_before = self.connection.execute("SELECT COUNT(*) FROM genres").fetchone()[0]
        insert_cursor.execute("INSERT INTO GENRES(Name) VALUES ('Power Metal')")
        self.connection.commit()

        genre_added = pandas.read_sql_query("SELECT Name from GENRES ORDER BY GenreId DESC LIMIT 1", self.connection).iloc[0][0]
        self.assertEqual(genre_added, "Power Metal")

        rows_after = self.connection.execute("SELECT COUNT(*) FROM genres").fetchone()[0]

        self.assertEqual(rows_before, rows_after-1)

        cleanup = insert_cursor.execute("DELETE FROM genres WHERE GenreId > 25")
        self.connection.commit()
        self.connection.close()
