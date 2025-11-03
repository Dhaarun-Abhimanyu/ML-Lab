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

void handleError(const char* msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

int main(){
    int sockfd, new_sock;
    struct sockaddr_in serv_addr, new_addr;
    socklen_t addr_size;
    char buffer[MAX_BUFFER];
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Error in socket creation");
    }
    printf("Server socket created successfully.\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Error in binding");
    }
    printf("Binding successful, lisenting on port %d\n", PORT);

    if(listen(sockfd, 5) != 0){
        handleError("Error in listening");
    }
    printf("Listening...\n");

    addr_size = sizeof(new_addr);

    new_sock = accept(sockfd, (struct sockaddr*)&new_addr, &addr_size);
    if(new_sock < 0){
        handleError("Error in accepting connection");
    }
    printf("Connection accepted from %s:%d\n", inet_ntoa(new_addr.sin_addr), ntohs(new_addr.sin_port));

    while(1){
        ssize_t nbytes = read(new_sock, buffer, MAX_BUFFER-1);
        if(nbytes <= 0){
            printf("Client disconnected or read error.\n");
            break;
        }

        buffer[nbytes] = '\0';
        printf("Client: %s", buffer);
        if(strncmp(buffer, "exit", 4) == 0){
            printf("Client sent exit. Closing connection...\n");
            break;
        }

        printf("Server: ");
        fgets(buffer, MAX_BUFFER, stdin);

        nbytes = write(new_sock, buffer, strlen(buffer));
        if(nbytes < 0){
            perror("Write error");
            break;
        }
        if(strncmp(buffer, "exit", 4) == 0){
            printf("Server sent exit. Closing connection...\n");
            break;
        }
    }
    close(new_sock);
    close(sockfd);
    return 0;
}