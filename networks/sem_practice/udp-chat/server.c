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

void handleError(char* msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(){
    int sockfd;
    struct sockaddr_in serv_addr, client_addr;
    socklen_t addr_size;
    char buffer[MAX_BUFFER];

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if(sockfd < 0){
        handleError("Error in socket creation");
    }
    printf("Socket created\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    memset(&client_addr, 0, sizeof(client_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Error in binding");
    }
    printf("Binding successful. Waiting for client...\n");

    addr_size = sizeof(client_addr);

    while(1){
        ssize_t nbytes = recvfrom(sockfd, buffer, MAX_BUFFER-1, 0, 
                                  (struct sockaddr*)&client_addr, &addr_size);
        if(nbytes < 0){
            handleError("Error in recvfrom");
        }
        buffer[nbytes] = '\0';

        printf("Client (%s:%d): %s\n", 
                inet_ntoa(client_addr.sin_addr),
                ntohs(client_addr.sin_port), 
                buffer);
        
        if(strncmp(buffer, "exit", 4)==0){
            printf("Client exit. Shutting down...\n");
            break;
        }

        printf("Server: ");
        fgets(buffer, MAX_BUFFER, stdin);
        
        sendto(sockfd, buffer, strlen(buffer), 0, 
               (struct sockaddr*)&client_addr, addr_size);
        if(strncmp(buffer, "exit", 4) == 0){
            printf("Server exiting. Shutting down...\n");
            break;
        }
    }
    close(sockfd);
    return 0;
}