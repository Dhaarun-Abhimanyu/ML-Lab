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

int isInt(char* token){
    int ret = 0, i=0;
    while(token[i] != '\0' && token[i] != '\n' && token[i] != ' '){
        if(token[i] < '0' || token[i] > '9'){
            return -1;
        }
        ret = (ret*10)+(int)(token[i]-48);
        i++;
    }
    return ret;
}

int main(){
    int sockfd, clientfd;
    struct sockaddr_in serv_addr, client_addr;
    socklen_t addr_size;
    char buffer[MAX_BUFFER];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Socket creation failed.\n");
    }
    printf("Created socket successfully.\n");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Socket binding failed");
    }
    printf("Socket binded successfully.\n");

    if(listen(sockfd, 5) != 0){
        handleError("Error in listening.\n");
    }
    printf("Socket listening for connections.\n");

    addr_size = sizeof(client_addr);
    clientfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_size);
    if(clientfd < 0){
        handleError("Error in accepting connection");
    }
    printf("Connected to %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

    while(1){
        ssize_t nbytes = read(clientfd, buffer, MAX_BUFFER-1);
        if(nbytes <= 0){
            perror("Error in reading/server disconnected.\n");
            break;
        }
        buffer[nbytes] = '\0';
        printf("Client: %s", buffer);
        char *token; int len = 0;
        int data[5];
        //printf("AA");
        token = strtok(buffer, " ");
        //printf("BB"); 
        if(token != NULL && strncmp(token, "exit", 4)==0){
            printf("Client disconnecting...\n");
            break;
        }
        while(token != NULL){
            //printf("Token : %s\n", token);
            int check = isInt(token);
            if(check==-1){
                printf("Data format wrong\n");
                break;
            }
            data[len++] = check;
            token = strtok(NULL, " ");
            if(len==5){ break; }
        }
        if(len != 5){
            printf("Not enough parameters.\n");
            break;
        }else if(token != NULL){
            while(token != NULL){ token = strtok(NULL, " "); }
            printf("Sent more parameters than expected.\n");
            break;
        }
        int res = data[0] + data[1] + data[2] - data[3] - data[4];
        printf("Server: Net salary: %d\n", res);
        snprintf(buffer, MAX_BUFFER, "%d\n", res);
        nbytes = write(clientfd, buffer, strlen(buffer));
        if(nbytes < 0){
            perror("Write failed.\n");
            break;
        }
    }
    close(sockfd);
    close(clientfd);

    return 0;
}