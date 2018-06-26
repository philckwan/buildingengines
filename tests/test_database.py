#!/usr/bin/env python

import unittest
import sqlite3
import pandas

from app import database_constants


class DatabaseTestCase(unittest.TestCase):
    def test_connection_succeeded(self):
        connection = sqlite3.connect(database_constants.DATABASE_LOCATION)
        self.assertEqual(type(connection).__name__, 'Connection')
        connection.close()

    def test_tables_exist(self):
        connection = sqlite3.connect(database_constants.DATABASE_LOCATION)
        cursor = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")

        list_of_tables = []
        for element in cursor.fetchall():
            list_of_tables.append(element[0])

        for table in database_constants.DATABASE_TABLES:
            assert table in list_of_tables

    def test_genre_columns_exists(self):
        connection = sqlite3.connect(database_constants.DATABASE_LOCATION)
        cursor = connection.execute('select * from genres')

        column_names = [column_name[0] for column_name in cursor.description]

        for column in database_constants.GENRES_COLUMNS:
            assert column in column_names

    def test_row_exists(self):
        connection = sqlite3.connect(database_constants.DATABASE_LOCATION)
        insert_cursor = connection.cursor()

        rows_before = connection.execute("SELECT COUNT(*) FROM genres").fetchone()[0]
        insert_cursor.execute("INSERT INTO GENRES(Name) VALUES ('Power Metal')")
        connection.commit()

        #genre_cursor = connection.execute("SELECT 1 from GENRES ORDER BY GenreId DESC")
        #print(type(genre_cursor.fetchone()))
        #print type(pandas.read_sql_query("SELECT Name from GENRES ORDER BY GenreId DESC LIMIT 1", connection))

        genre_added = pandas.read_sql_query("SELECT Name from GENRES ORDER BY GenreId DESC LIMIT 1", connection).iloc[0][0]
        self.assertEqual(genre_added, "Power Metal")

        rows_after = connection.execute("SELECT COUNT(*) FROM genres").fetchone()[0]

        self.assertEqual(rows_before, rows_after-1)

        cleanup = insert_cursor.execute("DELETE FROM genres WHERE GenreId > 25")
        connection.commit()
        connection.close()
