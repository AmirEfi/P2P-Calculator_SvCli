import socket
import os

# Define the maximum file size to be chunked and the chunk size
MAX_FILE_SIZE = 1024 * 1024  # 1 MB
CHUNK_SIZE = 1024  # 1 KB

# Define the message format for file requests and responses
FILE_REQUEST_MESSAGE_FORMAT = 'FILE_REQUEST\n{}\n'
FILE_RESPONSE_MESSAGE_FORMAT = 'FILE_RESPONSE\n{}\n{}\n{}\n'

# Define the file name for storing the server information
SERVERS_FILE = 'servers.txt'


def send_file(sock, client_addr, file_path):
    # Print the receiver's port to the console
    receiver_port = client_addr[1]
    print('Sending file to receiver on port {}'.format(receiver_port))

    # Send the file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    message = FILE_RESPONSE_MESSAGE_FORMAT.format(file_name, file_size, '').encode('utf-8')
    sock.sendall(message)

    # Send the file data in chunks
    with open(file_path, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            message = FILE_RESPONSE_MESSAGE_FORMAT.format(file_name, file_size, chunk_number).encode('utf-8') + chunk
            sock.sendall(message)
            chunk_number += 1

def main():
    # Ask the user whether they want to be a server or a receiver
    mode = input("Enter 's' for server mode, 'r' for receiver mode: ")

    if mode == 's':
        # If in server mode, ask the user to specify a folder to share files
        folder = input('Enter the path to the folder to share: ')

        # Create a socket object for the server
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the IP address and port number
        server_port = int(input('Enter the port number to bind to: '))
        server_sock.bind(('127.0.0.1', server_port))

        # Listen for incoming connections
        server_sock.listen()

        # Open the servers file for appending
        with open(SERVERS_FILE, 'a') as f:
            # Write the server information to the file
            f.write('127.0.0.1:{}\n'.format(server_port))
        while True:
            # Accept a new connection
            client_sock, client_addr = server_sock.accept()
            # Receive a message from the client
            message = client_sock.recv(MAX_FILE_SIZE).decode('utf-8').rstrip()
            # If the message is a file request, send the requested file
            if message.startswith('FILE_REQUEST'):
                file_name = message.split('\n')[1]
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    send_file(client_sock, client_addr, file_path)

            # Close the connection
            client_sock.close()

    elif mode == 'r':
        # If in receiver mode, read the server information from the file
        with open(SERVERS_FILE, 'r') as f:
            server_info = [line.strip().split(':') for line in f.readlines()]
        # Send the file request to each server and receive the file response
        file_name = input('Enter the name of the file to request: ')
        have_file = False
        for ip, port in server_info:
            # Create a socket object for the client
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'sending request to port {port}')
            # Connect to the server
            client_sock.connect(('127.0.0.1', int(port)))
            print(f'your port is {client_sock.getsockname()[1]}')
            # Send the file request
            message = FILE_REQUEST_MESSAGE_FORMAT.format(file_name).encode('utf-8')
            client_sock.sendto(message, (ip, int(port)))

            # Receive the file response
            file_data = b''
            while True:
                response = client_sock.recv(CHUNK_SIZE)
                if not response:
                    break
                file_data += response
            if len(file_data) == 0:
                continue
            response_lines = file_data.decode('utf-8').split('\n')
            file_size = int(response_lines[2])
            file_chunks = response_lines[4:]

            # Reconstruct the file from the received chunks
            file_content = ""
            for i in range(-1, file_size, CHUNK_SIZE):
                chunk_data = file_chunks[i + 5]
                file_content += chunk_data
            # Write the file to the receiver directory
            receiver_port = client_sock.getsockname()[1]
            receiver_dir = str(receiver_port)
            receiver_dir = "F:/SBU/term6/Network/finalp/files/received/" + receiver_dir
            file_path = os.path.join(receiver_dir, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(file_content)

            print('File received from server on port {}'.format(port))
            # Close the connection
            client_sock.close()
            break

    else:
        print('Invalid mode')


if __name__ == '__main__':
    main()