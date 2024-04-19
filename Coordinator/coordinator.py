
class CoordiantorError(Exception):
    """A custom exception class."""
    
    def __init__(self, message):
        """Initialize the custom exception with a message."""
        self.message = message
    
    def __str__(self):
        """Return a string representation of the exception."""
        return f"CoordnatorError: {self.message}"
    
def get_consumers(connection):
    cursor = connection.cursor()
    cursor.execute("\
        SELECT c.*, cus.server_count \
        FROM Consumers as c \
            JOIN \
            (SELECT consumer_id, COUNT(*) as server_count \
            FROM ConsumerUsingServer \
            GROUP BY consumer_id) as cus \
        ON c.id = cus.consumer_id;")
    result = cursor.fetchall()
    cursor.close()
    return result
    

def insert_server_record(connection, ip, port):

    cursor = connection.cursor(prepared=True)
    insert_statement = "INSERT INTO Servers (ip, port) VALUES (%s, %s)"

    try:
        cursor.execute(insert_statement, (ip, port))
        connection.commit()
    except Exception as e:
        raise CoordiantorError("MySQL Error: " + str(e))
    else:

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id = cursor.fetchone()[0]
        return last_insert_id
    finally:
        cursor.close()
    

def insert_consumer_record(connection, compensation, frequency):

    cursor = connection.cursor(prepared=True)
    insert_statement = "INSERT INTO Consumers (compensation, frequency) VALUES (%s, %s)"

    try:
        cursor.execute(insert_statement, (compensation, frequency))
        connection.commit()
    except Exception as e:
        raise CoordiantorError("MySQL Error: " + str(e))
    else:

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_insert_id = cursor.fetchone()[0]
        return last_insert_id
    finally:
        cursor.close()

def setup_servers_for_consumer(connection, consumer_id, server_quantity):
    cursor = connection.cursor(prepared=True)
    get_server_id_statement = f"SELECT id FROM Servers ORDER BY RAND() LIMIT {server_quantity};"
    insert_consumer_server_pair_statement = "INSERT INTO ConsumerUsingServer (consumer_id, server_id) VALUES (%s, %s)"

    try:
        cursor.execute(get_server_id_statement)
        chosen_server_ids = list(map(lambda x: x[0], cursor.fetchall()))
        for server_id in chosen_server_ids:
            cursor.execute(insert_consumer_server_pair_statement, (consumer_id, server_id))
        
        connection.commit()
    except Exception as e:
        raise CoordiantorError("MySQL Error: " + str(e))
    else:
        return chosen_server_ids
    finally:
        cursor.close()


def insert_car_record(connection, consumer_id, payment_method):
    cursor = connection.cursor(prepared=True)
    insert_car_supply_consumer_statement = "INSERT INTO CarSupplyConsumer (consumer_id, payment_method) VALUES (%s, %s)"

    try:
        cursor.execute(insert_car_supply_consumer_statement, (consumer_id, payment_method))
        connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        car_id = cursor.fetchone()[0]

    except Exception as e:
        raise CoordiantorError("MySQL Error: " + str(e))
    else:
        return car_id
    finally:
        cursor.close()

def get_servers_of_consumer(connection, consumer_id):
    cursor = connection.cursor(prepared=True)
    get_servers_statement = \
        "SELECT s.ip, s.port \
        FROM Consumers as c JOIN ConsumerUsingServer as cus JOIN Servers as s \
        ON c.id = cus.consumer_id and cus.server_id = s.id\
        WHERE c.id = %s;"

    try:
        cursor.execute(get_servers_statement, (consumer_id, ))
        servers = cursor.fetchall()

    except Exception as e:
        raise CoordiantorError("MySQL Error: " + str(e))
    else:
        return servers
    finally:
        cursor.close()