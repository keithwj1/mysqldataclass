"""baseclass.py

This script contains classes that allow for easy object creation from databases.

Can be used with databases other than mysql, just change the driver in the DataList class

This script requires that `mysql.connector` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
classes:

    * DataObject - Base class for a table object
    * DataList - Base list class for filling data from a table/database
"""


import mysql.connector
import bisect
import os
from dotenv import load_dotenv


class NumberArrayWrapper:
    """
    Class NumberArrayWrapper
    Wraps a base class to allow for bisect
    """

    def __init__(self, array) -> None:
        self.__array = array

    def __getitem__(self, i) -> str:
        return self.__array[i].number

    def __len__(self) -> int:
        return len(self.__array)


class DataObject:
    """
    Class DataObject
    A base class that other data objects inherit for easy creation of objects from
    a database
    """

    number: str

    def __init__(self, number: str, *args, **kwargs) -> None:
        self.number = number

    def __lt__(self, o: object) -> bool:
        if self.number < o.number:
            return True
        return False

    def __gt__(self, o: object) -> bool:
        return not self.__lt__(o)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} number is {self.number}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__ }(Number={self.number})"

    def __eq__(self, o: object) -> bool:
        if self.number == o.number:
            return True
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)


class DataList:
    """
    Class DataList
    A base class that holds the functions to fill data from a database and store it in self.objects
    """

    object_type: DataObject
    database: str
    hostname: str
    port: int
    username: str
    password: str
    table: str
    table_dict: dict
    objects: list[DataObject]
    query: str
    filled: bool

    def __init__(self, *args, **kwargs) -> None:
        self.object_type = DataObject
        self.database = ""
        self.table = None
        self.hostname = ""
        self.port = 3306
        self.username = ""
        self.password = ""
        self.table_dict = None
        self.query = None
        self.filled = False
        self.objects = []
        self.get_env_variables()
    def get_env_variables(self) -> None:
        """
        Sets Variables from the .env file

        This is so I can keep an .env file with variables without exposing the passwords to github

        :return: Returns nothing
        """
        if self.database != "":
            return
        path : str
        path = '.env'
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(os.path.dirname(path)),'.env')
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(os.path.dirname(path)),'.env')
                if not os.path.exists(path):
                    print("Not using .env \n")
                    return
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                splitline = line.split('=')
                if len(splitline) > 1:
                    setattr(self,splitline[0],splitline[1])

    def print_connection(self) -> None:
        print(f"host={self.hostname},port={self.port},user={self.username},database={self.database},password={self.password} \n")

    def connect(self) -> mysql.connector.MySQLConnection:
        """
        Connects to the database and returns a connection object

        :return: Returns connection object
        """
        connection: mysql.connector.MySQLConnection
        connection = mysql.connector.connect(
            host=self.hostname,
            port=self.port,
            user=self.username,
            database=self.database,
            password=self.password,
        )
        return connection

    def set_table(self, table: str) -> None:
        """
        Sets the value of the table variable

        :param table: The name of the table
        :return: returns nothing
        """
        self.table = table

    def generate_query(self, table: str, table_dict: dict) -> str:
        """
        Generates a query string from the options given

        :param table: The name of the table
        :param table_dict: The dictionary of column to variable name pairs
        :return: returns string with the query
        """
        if table_dict is None:
            raise Exception("Missing Dictionary")
        if table is None:
            raise Exception("Missing Table")
        query: str
        query = "SELECT "
        for key in table_dict.keys():
            query = query + "'" + key + "',"
        query = query[:-1]
        query = query + " FROM " + table
        return query

    def set_query(self, table: str = None, table_dict: dict = None) -> str:
        """
        Generates a query string from the options given and sets it in the self.query variable.

        :param table: The name of the table
        :param table_dict: The dictionary of column to variable name pairs
        :return: returns string with the query
        """
        if table is None:
            table = self.table
        if table_dict is None:
            table_dict = self.table_dict
        self.query = self.generate_query(table, table_dict)
        return self.query

    def add_object(self, object) -> DataObject:
        """
        Adds an object to the objects array

        :param object: The object to add
        :return: returns the object
        """
        bisect.insort(self.objects, object)
        return object

    def create_object(self, number: str) -> DataObject:
        """
        Creates an object with the self.object_type, adds it to self.objects and returns it

        :param number: Unique identifier of the object
        :return: returns the object
        """
        cur: DataObject
        cur = self.object_type(number)
        self.add_object(cur)
        return cur

    def fill_data_from_table(
        self, table: str = None, table_dict: dict = None, query: str = None
    ) -> None:
        """
        Fill the objects array with information from the database

        :param table: The name of the table
        :param table_dict: The dictionary of column to variable name pairs
        :param query: A custom query that will override table and table_dit
        :return: returns nothing
        """
        print(f"Filling Data From Table {self.table}")
        if query is None:
            if self.query is None:
                query = self.set_query(table, table_dict)
            else:
                query = self.query
        with self.connect() as cnxn:
            with cnxn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                num_rows: int
                columns = [column[0] for column in cursor.description]
                for row in rows:
                    cur: DataObject
                    cur = self.create_object(row[0])
                    i: int
                    i = 0
                    # No zip so numba/cython knows what's good
                    for elem in row:
                        if isinstance(elem, str):
                            elem = elem.strip()
                        col: str
                        col = columns[i]
                        i += 1
                        setattr(cur, self.table_dict[col], elem)
                cursor.close()
            cnxn.close()

    def fill(self) -> None:
        """
        Checks if the data has already been filled and fills it if not.
        :return: returns nothing
        """
        if not self.filled:
            self.filled = True
            return self.fill_data_from_table(self.table, self.table_dict, self.query)

    def get_with_number(self, array: list[DataObject], number: str) -> DataObject:
        """
        Searches the given array for the provided number and returns the object

        :param array: Array to search
        :param number: Number to search for
        :return: returns the object
        """
        if array is None:
            return None
        elif len(array) < 1:
            return None
        wrapped_array: NumberArrayWrapper
        wrapped_array = NumberArrayWrapper(array)
        index: int
        index = bisect.bisect_right(wrapped_array, number, 0, len(array)) - 1
        if index < len(array) and wrapped_array[index] == number:
            return array[index]
        return None

    def get_all_with_number(
        self, array: list[DataObject], number: str
    ) -> list[DataObject]:
        """
        Searches the given array for the provided number and returns an array of objects that match

        :param array: Array to search
        :param number: Number to search for
        :return: returns an array of objects
        """
        if array is None:
            return None
        elif len(array) <= 0:
            return None
        wrapped_array: NumberArrayWrapper
        wrapped_array = NumberArrayWrapper(array)
        array_length: int
        array_length = len(array)
        low: int
        low = bisect.bisect_left(wrapped_array, number, 0, array_length)
        if low >= array_length or wrapped_array[low] != number:
            return None
        high: int
        high = bisect.bisect_right(wrapped_array, number, 0, array_length) - 1
        if high >= array_length or wrapped_array[high] != number:
            return None
        return array[low : high + 1]

    def search_number(self, number) -> DataObject:
        """
        Searches the class array for the given number

        :param array: Array to search
        :param number: Number to search for
        :return: returns the object
        """
        return self.get_with_number(self.objects, number)

    def search_all_number(self, number) -> list[DataObject]:
        """
        Searches the class array for the provided number and returns an array of objects that match

        :param array: Array to search
        :param number: Number to search for
        :return: returns an array of objects
        """
        return self.get_all_with_number(self.objects, number)

    def add_unique_object(self, new_object) -> DataObject:
        """
        Adds an object to the self.objects array if the number doesn't already exist

        :param array: Array to add the object to
        :param object: Object to add
        :return: returns the object
        """
        cur: DataObject
        cur = self.search_number(new_object.number)
        if cur is None:
            self.add_object(new_object)
        return new_object
