#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define MAX_BUFFER 1024
#define SERVER_IP "127.0.0.1"

void handleError(const char* msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(){
    int clientfd;
    struct sockaddr_in serv_addr;
    char buffer[MAX_BUFFER];

    clientfd = socket(AF_INET, SOCK_STREAM, 0);
    if(clientfd < 0){
        handleError("Error in socket creation");
    }
    printf("Client socket created successfully.\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0){
        handleError("Invalid address (or) Address not supported");
    }
    
    if(connect(clientfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Error in connection");
    }
    printf("Connected to server.\n");

    while(1){
        printf("Client: ");
        fgets(buffer, MAX_BUFFER, stdin);

        ssize_t nbytes = write(clientfd, buffer, strlen(buffer));
        if(nbytes < 0){
            perror("Write error");
            break;
        }

        if(strncmp(buffer, "exit", 4) == 0){
            printf("Client sent exit. Closing connection...\n");
            break;
        }

        nbytes = read(clientfd, buffer, MAX_BUFFER-1);
        if(nbytes <= 0){
            printf("Server disconnected or read error.\n");
            break;
        }

        buffer[nbytes] = '\0';
        printf("Server: %s", buffer);
        if(strncmp(buffer, "exit", 4)==0){
            printf("Server sent exit. Closing connection...\n");
            break;
        }
    }
    close(clientfd);

    return 0;
}