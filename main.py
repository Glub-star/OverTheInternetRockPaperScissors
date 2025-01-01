import socket

# Shared game logic
def play_game(conn, role):
    choices = ['rock', 'paper', 'scissors']
    
    if role == "server":
        # Server part: Waiting for client's choice and processing the game
        client_choice = conn.recv(1024).decode('utf-8')
        if not client_choice:
            return

        #print(f"Client chose: {client_choice}")

        # Server's choice (for simplicity, just using rock)
        while True:
            server_choice = input("Enter your choice (rock, paper, scissors): ").lower()

            if server_choice in choices:
                break  # Exit the loop once a valid choice is entered
            else:
                print("Invalid input. Please enter rock, paper, or scissors.")

        # Determine the winner
        if client_choice == server_choice:
            result = "It's a tie!"
        elif (client_choice == 'rock' and server_choice == 'scissors') or \
             (client_choice == 'paper' and server_choice == 'rock') or \
             (client_choice == 'scissors' and server_choice == 'paper'):
            result = "You win!"  # Server wins
        else:
            result = "You lose!"  # Server loses
        
        # Send result back to the client
        conn.send(result.encode('utf-8'))
        
        # Explicitly print if the server (host) won or lost
        if result == "You win!":
            print("You Lost!")
        elif result == "You lose!":
            print("You Won!")
        else:
            print("It's a tie!")
        
    elif role == "client":
        # Client part: Sending the choice to the server
        while True:
            user_choice = input("Enter your choice (rock, paper, scissors): ").lower()

            if user_choice in choices:
                # Send the choice to the server
                conn.send(user_choice.encode('utf-8'))
                break  # Exit the loop once a valid choice is sent
            else:
                print("Invalid input. Please enter rock, paper, or scissors.")

        # Receiving result from the server
        result = conn.recv(1024).decode('utf-8')
        print(f"Result: {result}")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Listening on all interfaces and port 12345
    server_socket.listen(1)
    
    ip_address = socket.gethostbyname(socket.gethostname())  # Get local IP address
    print(f"Server is hosting on: {ip_address}")
    
    print("Server is listening for connections...")
    
    conn, addr = server_socket.accept()
    print(f"Connected to: {addr}")

    # Run the game as a server
    play_game(conn, "server")

    conn.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Ask for the server's IP address
    server_ip = input("Enter the server IP address: ")
    if server_ip == "localhost": server_ip = "127.0.0.1"
    server_port = 12345
    
    client_socket.connect((server_ip, server_port))

    # Run the game as a client
    play_game(client_socket, "client")

    client_socket.close()


def main():
    print("Welcome to Rock, Paper, Scissors!")
    role = input("Would you like to start a server or join an existing one? (start/join): ").strip().lower()
    
    if role == 'start':
        print("You are hosting the server.")
        start_server()
    elif role == 'join':
        print("You will connect to an existing server.")
        start_client()
    else:
        print("Invalid input. Please enter 'start' or 'join'.")
        main()


if __name__ == '__main__':
    main()
