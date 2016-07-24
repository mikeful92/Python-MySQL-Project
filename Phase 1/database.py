import pymysql

try:
    # Connection to MySQL DB
    cnn = pymysql.connect(
        host="localhost",
        user="root",  # your username
        password='root',
        database="bb_cards")  # name of the data base
    print("It Works!!")

    # Cursor executes the string queries
    cursor = cnn.cursor()

    # String query to create the buy_list table
    createStatement = """CREATE TABLE buy_list(
        sport varchar(2) NOT NULL,
        item_desc varchar(50) NOT NULL,
        buy_price int(10) NOT NULL
    ) ENGINE=MyISAM;    
    """
    # Execute the SQL CREATE statement
    cursor.execute(createStatement)
    print("Table created")

    # String query to INSERT the sample data to the table
    insertStatement = """INSERT INTO `buy_list` (`sport`, `item_desc`, `buy_price`) VALUES
    ('BB', '1960 Topps Mantle #350 PSA 4', 199),
    ('FB', '1961 Topps Unitas #1 PSA 3', 299),
    ('BK', '1986-1987 Jordan #26 PSA 8', 400),
    ('HK', '1954 Parkhurst Howe #24 PSA 4', 500),
    ('BB', '1983 Topps Wax Case', 2300),
    ('BK', '1989-90 Fleer Wax Case', 300);
    """

    # Execute the SQL INSERT statement
    cursor.execute(insertStatement)
    print("Data inserted")

    # Commit all changes to the connection
    cnn.commit()
    print("Changes commited")


except pymysql.MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

finally:
    if cursor:
        cursor.close()
    if cnn:
        cnn.close()

