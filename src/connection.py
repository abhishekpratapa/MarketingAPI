from pymongo import MongoClient


# Type Exception
#
# Description: This exception handles a type error if the variable if the wrong type this
#              this exception is called

class type_exception(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Database Exception
#
# Description: This exception handles a database exception, it is raised whenever a database
#              doesn't exist this exception is called

class database_exception(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Query Error
#
# Description: this exception handles a query exception, it is raised whenever there is
#              and error when quering the database

class query_error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# class: Connection
#
# Description: This is a class that allows someone to connect to a mongo server and do all the
#              necessary functions.
#
# Methods:
#
#       insert
#       get_data
#

class Connection:


    # Method: __init_
    #
    # Description: Create a new database connection object with the database_names specified, using the url specified
    #
    # parameter url: The URL to the MongoDB database that requires the connection
    # parameter database_names: An array of database names to create a connection to the client
    #
    # return: [No return value]

    def __init__(self, url, database_names):
        #connect to the mongo client
        self.client = MongoClient(url);
        self.db = dict()

        #connect to all the DB's in the database_names
        for database in database_names:
            self.db[database] = self.client[database]


    # Method: insert
    #
    # Description: insert data into the Mongo database
    #
    # parameter database_name [String]: this parameter takes the name of the database to connect to
    # parameter collection_name [String]: this parameter takes the name of the collection to connect to
    # @parameter data [Dictionary]: this parameter takes a data variable in the form of a dict() datatype,
    #                               to insert into the database
    #
    # return: True if the data is successfully inserted into the database | False of the data is not
    #         successfully inserted into the database

    def insert(self, database_name, collection_name, data):

        # Check if the type of the data is dict()
        if not (type(dict()) == type(data)):
            raise type_exception("Please make sure the data is in 'dict()' format")

        # Check if the database name exists
        if not (database_name in list(self.db.keys())):
            raise database_exception("the selected database doesn't exist in the particular scope")

        # Try to insert the data into the database
        try:
            self.db[database_name][collection_name].insertOne(data)
            return True
        except:
            return False

    # method: get_data
    #
    # Description: get data from the specified Mongo DB, if a search query is defined then use that query
    #              to get the data from the database
    #
    # parameter database_name [String]: this parameter takes the name of the database to connect to
    # parameter collection_name [String]: this parameter takes the name of the collection to connect to
    # @parameter search_query [Dictionary]: this parameter takes a query in the form of a dict() datatype
    #
    # return: this method returns the database in the form of a dictionary list

    def get_data(self, database_name, collection_name, search_query):

        # Check if the type of the search_query is dict()
        if not (type(dict()) == type(search_query)):
            raise type_exception("Please make sure the search_query is in 'dict()' format")

        # Check if the database name exists
        if not (database_name in list(self.db.keys())):
            raise database_exception("the selected database doesn't exist in the particular scope")

        # Check if the parameters are empty
        if not search_query:
            # Query the whole collection
            try:
                return self.db[database_name][collection_name].find()
            except:
                raise query_error("There was a query error, could not find any documents")
        else:
            # Query a particular collection
            try:
                return  self.db[database_name][collection_name].find(search_query)
            except:
                raise query_error("There was a query error, could not find any documents")