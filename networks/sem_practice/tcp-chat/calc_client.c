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

void handleError(char* msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(){
    int clientfd;
    struct sockaddr_in serv_addr;
    char buffer[MAX_BUFFER];

    clientfd = socket(AF_INET, SOCK_STREAM, 0);
    if(clientfd < 0){
        handleError("Socket creating failed...\n");
    }
    printf("Created client socket.\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0){
        handleError("Invalid address (or) Address not supported.\n");
    }

    if(connect(clientfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Failed connecting to server");
    }
    printf("Connected to server.\n");

    while(1){
        printf("Client: ");
        fgets(buffer, MAX_BUFFER, stdin);
        ssize_t nbytes = write(clientfd, buffer, strlen(buffer));
        if(nbytes < 0){
            perror("Write error.\n");
            break;
        }
        if(strncmp(buffer, "exit", 4)==0){
            printf("Client disconnecting...\n");
            break;
        }
        nbytes = read(clientfd, buffer, MAX_BUFFER-1);
        if(nbytes <= 0){
            perror("Read failed.\n");
            break;
        }
        buffer[nbytes] = '\0';
        printf("Server: %s\n", buffer);
    }
    close(clientfd);
    return 0;
}