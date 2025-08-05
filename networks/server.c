#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>

#define PORT 9090
#define MAX_BUFFER 1024

void start_server() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buffer[MAX_BUFFER];

    // Creating socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Defining server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Binding the socket to the address
    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Binding failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Listening for incoming connections
    if (listen(server_fd, 3) == -1) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("[Server] Waiting for sensor data...\n");

    // Accepting incoming connections
    addr_len = sizeof(client_addr);
    client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addr_len);
    if (client_fd == -1) {
        perror("Accept failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Receiving data from client
    int len = recv(client_fd, buffer, MAX_BUFFER, 0);
    if (len == -1) {
        perror("Receive failed");
        close(client_fd);
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Null-terminate the received message
    buffer[len] = '\0';

    // Display received sensor data
    printf("[Server] Sensor Data Received: %s\n", buffer);

    // Closing the connection
    close(client_fd);
    close(server_fd);
}

void start_client() {
    int client_fd;
    struct sockaddr_in server_addr;
    char message[MAX_BUFFER];

    // Getting the sensor data message from the user
    printf("Enter sensor data: ");
    fgets(message, MAX_BUFFER, stdin);
    message[strcspn(message, "\n")] = '\0';  // Remove newline character

    // Creating socket
    client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Defining server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  // localhost
    server_addr.sin_port = htons(PORT);

    // Connecting to the server
    if (connect(client_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connection failed");
        close(client_fd);
        exit(EXIT_FAILURE);
    }

    // Send data to server
    send(client_fd, message, strlen(message), 0);
    printf("[Client] Data sent to server.\n");

    // Closing the connection
    close(client_fd);
}

int main() {
    pid_t pid;

    // Create a child process using fork to separate client and server
    pid = fork();
    
    if (pid == -1) {
        // Fork failed
        perror("Fork failed");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        // Child process - Client
        start_client();
    } else {
        // Parent process - Server
        start_server();
    }

    return 0;
}
