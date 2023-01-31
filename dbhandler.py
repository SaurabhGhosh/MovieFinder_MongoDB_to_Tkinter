# Import MySQL related libraries 
import mysql
from mysql.connector import Error
# Import Mongo db client library
from pymongo import MongoClient


class DBHandler:
    """This class contains the attributes and methods to handle database interactions from the scraping program as
    well as the UI tool. """
    def __init__(self):
        """This is the constructor method. It initiates the connection instances with the database."""
        # SQL DB initiation
        try:
            # Create the connection instance as a class level variable by calling "connect" method
            # and supplying the connection details and credentials.
            self.sql_connection = mysql.connector.connect(host='localhost',
                                                          port='3306',
                                                          database='pythonapps',
                                                          user='pythonuser',
                                                          password='Welcome1')
            if self.sql_connection.is_connected():
                db_Info = self.sql_connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)

        # Handle exception if connectivity fails
        except Error as e:
            print("Error while connecting to MySQL", e)

        # NoSQL DB initiation
        self.mongo_client = MongoClient(host="localhost", port=27017)
        self.mongo_db = self.mongo_client["local"]
        # Create a class variable for the collection. This will get overwritten with each gnre specific collection 
        self.movie_collection = None

    def get_directors(self):
        """This method retrieves the list of Directors from the MySQL DB"""
        # Set the query as a string 
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Directors'"
        # Get the cursor instance
        cursor = self.sql_connection.cursor()
        directors = []
        try:
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                directors.append(row[0])
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            cursor.close()
        return directors

    def get_writers(self):
        """This method retrieves the list of Writers from the MySQL DB"""
        # Set the query as a string 
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Writers'"
        cursor = self.sql_connection.cursor()
        writers = []
        try:
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                writers.append(row[0])
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            cursor.close()
        return writers

    def get_actors(self):
        """This method retrieves the list of Actors from the MySQL DB"""
        # Set the query as a string 
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Stars'"
        cursor = self.sql_connection.cursor()
        actors = []
        try:
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                actors.append(row[0])
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            cursor.close()
        return actors

    def get_movies_results(self, genre, director=None, writer=None, actor=None):
        """This method retrieves the records from the genre-specific collection from Mongo db.
           This method accepts values for the director,writer or actor's name to filter within
           list of movies"""
        # Get the collection instance for the genre
        self.movie_collection = self.mongo_db[genre + "boxoffice"]
        # Initiate the list to return
        movies = []
        # Mongo db takes search criteria as dictionary. Initiate the criteria dictionary and the list within it.
        # The format of the query will be formed like below -
        # search_query = "{ $and: [{$or: [ { Director: 'Andrew Dominik'}, { Directors: 'Andrew Dominik'} ] },\
        #    {$or: [ { Stars: 'Lily Fisher'}, { Star: 'Lily Fisher'} ] }]}"
        search_input_query = {}
        search_input_list = []
        # Append director's name from parameter if passed
        if director is not None and director != '':
            search_input_director = {'$or': [{'Directors': director}, {'Director': director}]}
            search_input_list.append(search_input_director)
        # Append writer's name from parameter if passed
        if writer is not None and writer != '':
            search_input_writer = {'$or': [{'Writers': writer}, {'Writer': writer}]}
            search_input_list.append(search_input_writer)
        # Append actor's name from parameter if passed
        if actor is not None and actor != '':
            search_input_actor = {'$or': [{'Stars': actor}, {'Star': actor}]}
            search_input_list.append(search_input_actor)
        # Add the criteria with '$and' if more than one criterion is provided
        if len(search_input_list) > 1:
            search_input_query = {'$and': search_input_list}
        # Keep only one criterion if one is sent with parameter
        elif len(search_input_list) == 1:
            search_input_query = search_input_list[0]
        # Don't add criteria if no parameter passed for director, writer and actor 
        else:
            pass

        # Iterate through the results and append the rank and title to the return list
        for doc in self.movie_collection.find(search_input_query):
            movie_detail = [doc.get("Rank"), doc.get("Title")]
            movies.append(movie_detail)
        return movies

    def get_movie_detail(self, movie_name):
        """This method retrieves the whole document for the selected movie from Mongo db collection matching by
        title. """
        return self.movie_collection.find_one({"Title": movie_name})

    def close_connections(self):
        """This method closes both MySQL and Mongo db collections"""
        self.sql_connection.close()
        self.mongo_client.close()