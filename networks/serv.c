#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/wait.h>

#define PORT 9090
#define BUFFER_SIZE 256
#define NUM_HEADLINES 3

void server_process() {
    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char headlines[NUM_HEADLINES][BUFFER_SIZE];
    int i;

    // Create server socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Error in server socket creation");
        exit(1);
    }
    printf("Server socket created successfully.\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Bind socket to the address
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error in server binding");
        exit(1);
    }
    printf("Server binding successful.\n");

    // Listen for incoming connections
    if (listen(server_socket, 5) == 0) {
        printf("Server listening on port %d...\n", PORT);
    } else {
        perror("Error in server listening");
        exit(1);
    }

    // Accept client connection
    client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
    if (client_socket < 0) {
        perror("Error in server accept");
        exit(1);
    }
    printf("Server accepted a client connection.\n");

    // Read all headlines first
    for (i = 0; i < NUM_HEADLINES; i++) {
        printf("Enter headline %d: ", i + 1);
        fgets(headlines[i], BUFFER_SIZE, stdin);
        headlines[i][strcspn(headlines[i], "\n")] = 0;
    }

    // Send all headlines with a newline delimiter
    for (i = 0; i < NUM_HEADLINES; i++) {
        send(client_socket, headlines[i], strlen(headlines[i]), 0);
        send(client_socket, "\n", 1, 0); // Send the newline delimiter
        printf("Server sent: %s\n", headlines[i]);
    }

    // Close sockets
    close(client_socket);
    close(server_socket);
    printf("Server shutting down.\n");
}

void client_process() {
    int client_socket;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    char headline_buffer[BUFFER_SIZE];
    int bytes_received;
    int i;

    // Create client socket
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket < 0) {
        perror("Error in client socket creation");
        exit(1);
    }
    printf("Client socket created successfully.\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Connect to the server
    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error in client connection");
        exit(1);
    }
    printf("Client connected to the server.\n");

    // Receive and display 3 headlines
    for (i = 0; i < NUM_HEADLINES; i++) {
        int buffer_pos = 0;
        memset(headline_buffer, 0, BUFFER_SIZE);
        
        while ((bytes_received = recv(client_socket, buffer, 1, 0)) > 0) {
            if (buffer[0] == '\n') {
                break;
            }
            if (buffer_pos < BUFFER_SIZE - 1) {
                headline_buffer[buffer_pos++] = buffer[0];
            }
        }
        
        if (bytes_received > 0) {
            printf("Headline %d: %s\n", i + 1, headline_buffer);
        }
    }

    // Close socket
    close(client_socket);
    printf("Client shutting down.\n");
}

int main() {
    pid_t pid;

    // Fork a new process
    pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        return 1;
    }

    if (pid == 0) {
        // Child process acts as the client
        sleep(1); // Give the server a moment to start listening
        client_process();
    } else {
        // Parent process acts as the server
        server_process();
        wait(NULL); // Wait for the child process to finish
    }

    return 0;
}