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

    int expected_seq_num = 0;
    int data[TOTAL_NUMS];
    srand(time(NULL));

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Socket creation failed");
    }
    
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Bind failed.\n");
    }
    printf("Binded successfully.\n");

    if(listen(sockfd, 5) != 0){
        handleError("Listen failed.\n");
    }
    printf("GBN Server listening...\n");

    addr_size = sizeof(client_addr);
    clientfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_size);
    if(clientfd < 0){
        handleError("Accept failed.\n");
    }
    printf("Client connected.\n");

    while(expected_seq_num < TOTAL_NUMS){
        ssize_t nbytes = read(clientfd, &packet, sizeof(Packet));
        if(nbytes <= 0){
            printf("Client disconnected.\n");
            break;
        }

        if(rand() % 10 < 3){
            printf("\nSIM LOSS: Packet %d dropped.\n", packet.seq_num);
            continue;
        }

        printf("Received seq: %d\n", packet.seq_num);
        ack_packet.type = ACK_TYPE;
        if(packet.seq_num == expected_seq_num){
            printf("-> ACCEPTED. Data : %d\n", packet.data);
            ack_packet.seq_num = expected_seq_num;
            data[expected_seq_num] = packet.data;
            write(clientfd, &ack_packet, sizeof(Packet));
            printf("-> ACK sent: %d\n", expected_seq_num);
            expected_seq_num++;
        } else {
            printf("-> DISCARDED. Expected %d, Got %d", expected_seq_num, packet.seq_num);
            ack_packet.seq_num = expected_seq_num-1;
            write(clientfd, &ack_packet, sizeof(Packet));
            printf("-> DUPLICATE ACK sent: %d\n", expected_seq_num-1);
        }
    }

    printf("Final list of Received data.\n");
    for(int i=0;i<TOTAL_NUMS;i++){
        printf("%d, ",data[i]);
    }
    printf("\nAll numbers received. Shutting down.\n");
    close(clientfd);
    close(sockfd);

    return 0;
}