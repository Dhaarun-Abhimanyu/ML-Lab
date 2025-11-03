#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include "../packet.h"

int main(){
    int sockfd, clientfd;
    struct sockaddr_in serv_addr, client_addr;
    socklen_t addr_size;
    Packet packet, ack_packet;

    int rcv_base = 0;
    int rcv_buffer[TOTAL_NUMS];
    int rcv_marker[TOTAL_NUMS];
    for(int i=0;i<TOTAL_NUMS;i++){
        rcv_marker[i] = 0;
    }
    srand(time(NULL));

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Socket creation failed.\n");
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Binding failed.\n");
    }
    if(listen(sockfd, 5) != 0){
        handleError("Listening failed.\n");
    }
    printf("Server listening...\n");

    addr_size = sizeof(client_addr);
    clientfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_size);
    if(clientfd < 0){
        handleError("Accepting failed.\n");
    }
    printf("Connection established.\n");

    while(rcv_base < TOTAL_NUMS){
        ssize_t nbytes = read(clientfd, &packet, sizeof(Packet));
        if(nbytes <= 0){
            printf("Client disconnected.\n");
            break;
        }

        if(rand()%10 < 3){
            printf("SIM LOSS: Packet %d dropped.\n", packet.seq_num);
            continue;
        }

        printf("Received seq: %d\n", packet.seq_num);
        ack_packet.type = ACK_TYPE;
        ack_packet.seq_num = packet.seq_num;

        if(packet.seq_num >= rcv_base && packet.seq_num < rcv_base + WINDOW_SIZE){
            printf("-> ACCEPTED & BUFFERED. Data: %d\n", packet.data);
            rcv_buffer[packet.seq_num] = packet.data;
            rcv_marker[packet.seq_num] = 1;
            write(clientfd, &ack_packet, sizeof(Packet));
            printf("->ACK sent: %d\n", packet.seq_num);

            while(rcv_base < TOTAL_NUMS && rcv_marker[rcv_base]){
                rcv_base++;
                printf("-> Window slided to %d\n", rcv_base);
            }
        }else if(packet.seq_num < rcv_base){
            printf("->DUPLICATE!!! ACK sent again: %d\n", packet.seq_num);
            write(clientfd, &ack_packet, sizeof(Packet));
        }else{
            printf("->DISCARDED. Outide window.\n");
        }
    }
    printf("Final list of Received data.\n");
    for(int i=0;i<TOTAL_NUMS;i++){
        printf("%d, ", rcv_buffer[i]); // Print from the buffer
    }
    printf("\nAll numbers received. Shutting down.\n");
    close(clientfd);
    close(sockfd);

    return 0;
}