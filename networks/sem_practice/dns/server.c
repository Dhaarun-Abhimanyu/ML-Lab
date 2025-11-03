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
#define DNS_SIZE 4


struct dns {
    char domain[32];
    char ip[32];
};

struct dns dns_db[DNS_SIZE] = {
    {"www.google.com", "1.1.1.1"},
    {"www.idk.com", "1.1.1.2"},
    {"www.github.com", "10.1.10.169"},
    {"www.youtube.com", "1.3.1.1"}
};

int resolve_domain(char* domain, char* ip){
    for(int i=0; i<DNS_SIZE;i++){
        if(strncmp(dns_db[i].domain, domain, strlen(dns_db[i].domain)) == 0){
            strcpy(ip, dns_db[i].ip);
            return 1;
        }
    }
    return 0;
}

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
        handleError("Socket creation failed.\n");
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    memset(&client_addr, 0, sizeof(client_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Error in binding...\n");
    }
    printf("Server binded successfully.\n");

    addr_size = sizeof(client_addr);

    while(1){
        ssize_t nbytes = recvfrom(sockfd, buffer, MAX_BUFFER-1, 0,
                                  (struct sockaddr*)&client_addr, &addr_size);
        if(nbytes < 0){
            handleError("Error in recvfrom.\n");
        }

        buffer[nbytes] = '\0';
        printf("Client : %s\n", buffer);
        if(strncmp(buffer, "exit", 4) == 0){
            printf("Client sent exit. Shutting down...\n");
            break;
        }

        char ip[32];
        int check = resolve_domain(buffer, ip);
        if(check == 1){
            printf("Resolved. ip of domain %s: %s\n", buffer, ip);
            sendto(sockfd, ip, strlen(ip), 0, 
                   (struct sockaddr*)&client_addr, addr_size);
        }else{
            printf("Domain not found.\n");
            sendto(sockfd, "Domain not found.\n", strlen("Domain not found.\n"), 0, 
                   (struct sockaddr*)&client_addr, addr_size);
        }
    }
    
    close(sockfd);
    return 0;
}