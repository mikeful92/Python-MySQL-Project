# Card Project -Phase 1

After following the introduction we are ready to start looking at some of the code. We will start with the <code>database.py</code> file. This is part of the final step of setup.

## Set-up

### SQL Tables/Data

We have automated the process of creating the SQL Tables and inserting sample data for them. This will allow us to DROP tables and revert to a clean slate as needed.

Once in the /Phase 1 directory we can run the python scrip with:

<code>python3 database.py</code>

The command interface will provide information on the success of the execution.

### Breakdown the code

'''python
import pymysql''''''

We begin by just importing the module needed for the connection to MySQL. It includes everything we will be referencing through out the code.

'''python
try:
    cnn = pymysql.connect(
        host="localhost",
        user="root",  # your username
        password='root',
        database="bb_cards")  # name of the data base
    print("It Works!!")'''

Here we are creating an object that will be used as the connection to the database by using the connect() function. The connection function takes a few parameters. The database is local, so the host is "localhost". We will be using the root user, but that could change in the future. The password is based on what you set up at instalation of the MySQL-Server. Last we want it to go directly into using the "bb_cards" database.

'''python
cursor = cnn.cursor()'''

While we have created a connection, we need a cursor to actual perform the actions that we desire to the database. As the name implies the cursor acts like the cursor when inputing commands through the command line interface. The cursor will execute queries that are provided as strings.

'''python
createStatement = """CREATE TABLE buy_list(
        sport varchar(2) NOT NULL,
        item_desc varchar(50) NOT NULL,
        buy_price int(10) NOT NULL
    ) ENGINE=MyISAM;"""
'''

Here we are creating a variable that will hold the query for creation of the first table as a string. This allows us to make changes directly to the variable and re-use the query if necesarry.


'''python
cursor.execute(createStatement)
    print("Table created")'''

The cursor has an execute() function that will run our desired query from a string. We do not receive confirmation of the completion so we print directly to the command line.

'''python
insertStatement = """INSERT INTO `buy_list` (`sport`, `item_desc`, `buy_price`) VALUES
    ('BB', '1960 Topps Mantle #350 PSA 4', 199),
    ('FB', '1961 Topps Unitas #1 PSA 3', 299),
    ('BK', '1986-1987 Jordan #26 PSA 8', 400),
    ('HK', '1954 Parkhurst Howe #24 PSA 4', 500),
    ('BB', '1983 Topps Wax Case', 2300),
    ('BK', '1989-90 Fleer Wax Case', 300);
    """'''

This is similar to the creation variable, but now we are inserting data into the table. By having this variable we can easily add or delete more items that we would like to have on our starting table.

'''python
cursor.execute(insertStatement)
    print("Data inserted")
    cnn.commit()
    print("Changes commited") '''

Here we have another execute function. After we have completed our changes to the database we commit those changes. This is done using the commit() function from the connection object(Not the cursor object).

'''python
except pymysql.MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

finally:
    if cursor:
        cursor.close()
    if cnn:
        cnn.close()'''

We include some exception handling to catch any errors and finally close the cursor and the connection.