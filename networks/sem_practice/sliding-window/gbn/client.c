#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "../packet.h"

#define SERVER_IP "127.0.0.1"

int main(){
    int sockfd;
    struct sockaddr_in serv_addr;
    Packet packet, ack;

    int data[TOTAL_NUMS] = {10,20,30,40,50,60,70,80,90,100};

    int base = 0, next_seq_num = 0;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Error when creating socket...\n");
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0){
        handleError("Wrong address (or) Address not supported.\n");
    }

    if(connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Connection failed");
    }

    while(base < TOTAL_NUMS){
        while(next_seq_num < base + WINDOW_SIZE && next_seq_num < TOTAL_NUMS){
            packet.type = DATA_TYPE;
            packet.seq_num = next_seq_num;
            packet.data = data[next_seq_num];

            printf("Sending packet: %d\n", next_seq_num);
            write(sockfd, &packet, sizeof(Packet));
            next_seq_num++;
        }

        ssize_t nbytes = read(sockfd, &ack, sizeof(Packet));
        next_seq_num = base;
        if(nbytes <= 0){
            printf("Server disconnected.\n");
            break;
        } else {
            if(ack.type == ACK_TYPE) {
                printf("Received: ACK %d\n", ack.seq_num);
                if(ack.seq_num >= base) {
                    base = ack.seq_num + 1;
                    next_seq_num = base;
                    printf("-> Window slided to %d.\n", base);
                }
            }
        }
    }

    printf("All numbers sent and ACKed.\n");
    close(sockfd);

    return 0;
}