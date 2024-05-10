import os
from flask import Flask, jsonify, request
import mysql.connector

from coordinator import get_consumers, get_servers_of_consumer, insert_car_record, insert_consumer_record, insert_server_record, setup_servers_for_consumer


app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return 'Coordinator Running...'

@app.route('/register/server', methods=['Post'])
def register_server():
    requestDict = request.json  # Get JSON data from the request body
    if not requestDict or 'ip' not in requestDict or 'port' not in requestDict:
        return jsonify({'error': 'Invalid request. IP and port are required.'}), 400
    
    ip = requestDict['ip']
    port = requestDict['port']

    try:
        connection = get_connection()
        assigned_id = insert_server_record(connection, ip, port)

    except Exception as e:
        return jsonify({'error': 'Internal error.', 'error message': str(e)}), 500
    
    finally:
        connection.close()  # Return connection to the pool
    
    return jsonify({'message': 'Server registered successfully', 'Assigned ID: ': assigned_id}), 201


@app.route('/consumers', methods=['Get'])
def consumers():
    try:
        connection = get_connection()
        consumer_info_list = get_consumers(connection)

    except Exception as e:
        return jsonify({'error': 'Internal error.', 'error message': str(e)}), 500
    
    finally:
        connection.close()  # Return connection to the pool
    
    return jsonify({ 'message': 'Consumer registered successfully',
                     'consumers': consumer_info_list
                     }), 200


@app.route('/register/consumer', methods=['Post'])
def register_consumer():
    requestDict = request.json  # Get JSON data from the request body
    if not requestDict \
        or 'compensation' not in requestDict \
        or 'frequency' not in requestDict \
        or 'server_quantity' not in requestDict:
        return jsonify({'error': 'Invalid request. Missing parameter.'}), 400
    
    compensation = requestDict['compensation']
    frequency = requestDict['frequency']
    server_quantity = requestDict['server_quantity']

    try:
        connection = get_connection()
        assigned_id = insert_consumer_record(connection, compensation, frequency)
        chosen_servers = setup_servers_for_consumer(connection, assigned_id, server_quantity)

    except Exception as e:
        return jsonify({'error': 'Internal error.', 'error message': str(e)}), 500
    
    finally:
        connection.close()  # Return connection to the pool
    
    return jsonify({ 'message': 'Consumer registered successfully',
                     'Assigned ID': assigned_id,
                     'Chosen servers': chosen_servers
                     }), 201


@app.route('/register/car', methods=['Post'])
def register_car():
    requestDict = request.json  # Get JSON data from the request body
    if not requestDict \
        or 'consumer_id' not in requestDict \
        or 'payment_method' not in requestDict:
        return jsonify({'error': 'Invalid request. Missing parameter.'}), 400
    
    consumer_id= requestDict['consumer_id']
    payment_method = requestDict['payment_method']

    try:
        connection = get_connection()
        car_id = insert_car_record(connection, consumer_id, payment_method)
        paired_servers = get_servers_of_consumer(connection, consumer_id)

    except Exception as e:
        return jsonify({'error': 'Internal error.', 'error message': str(e)}), 500
    
    finally:
        connection.close()  # Return connection to the pool
    
    return jsonify({ 'message': 'Consumer registered successfully',
                     'Assigned_ID': car_id,
                     "paired_servers" : paired_servers
                     }), 201



if __name__ == '__main__':
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=5,
        # host='127.0.0.1',
        # database='coordinator',
        # user='mytestuser',
        # password=''
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

    def get_connection():
        return connection_pool.get_connection()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

    connection_pool._remove_connections()




