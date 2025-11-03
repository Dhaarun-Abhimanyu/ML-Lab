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
    int sockfd;
    struct sockaddr_in serv_addr;
    socklen_t addr_size;
    char buffer[MAX_BUFFER];

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if(sockfd < 0){
        handleError("Error in socket creation");
    }
    printf("Client socket created successfully\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0){
        handleError("Invalid address (or) Address not supported");
    }
    addr_size = sizeof(serv_addr);

    while(1){
        printf("Client: ");
        fgets(buffer, MAX_BUFFER, stdin);
        sendto(sockfd, buffer, strlen(buffer), 0, 
               (const struct sockaddr*)&serv_addr, addr_size);
        
        if(strncmp(buffer, "exit", 4) == 0){
            printf("Client exiting. Shutting down.\n");
            break;
        }

        ssize_t nbytes = recvfrom(sockfd, buffer, MAX_BUFFER-1, 0, 
                                  (struct sockaddr*)&serv_addr, &addr_size);
        if(nbytes < 0){
            handleError("Error in recvfrom.\n");
        }
        buffer[nbytes] = '\0';
        printf("Server: %s\n", buffer);
        
        if(strncmp(buffer, "exit", 4)==0){
            printf("Server exiting. Shutting down...\n");
            break;
        }
    }
    close(sockfd);

    return 0;
}