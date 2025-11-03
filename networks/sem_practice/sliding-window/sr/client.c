#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <time.h>
#include "../packet.h"

#define SERVER_IP "127.0.0.1"

clock_t timer_start;
int timer_running = 0;

void start_timer(){
    timer_start = clock();
    timer_running = 1;
}

void stop_timer() {
    timer_running = 0;
}

int timeout(){
    if(timer_running==0){ return 0;}
    double elapsed = (double)(clock() - timer_start) / CLOCKS_PER_SEC;
    return elapsed >= TIMEOUT_SEC;
}

int main(){
    int sockfd;
    struct sockaddr_in serv_addr;
    Packet packet,  ack;

    int data[TOTAL_NUMS] = {10,20,30,40,50,60,70,80,90,100};
    int base = 0, next_seq_num=0;

    int ack_marker[TOTAL_NUMS];
    for(int i=0;i<TOTAL_NUMS;i++){
        ack_marker[i] = 0;
    }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0){
        handleError("Socket creation failed.\n");
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if(inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0){
        handleError("Wrong address.\n");
    }
    if(connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0){
        handleError("Connection failed.\n");
    }

    int flags = fcntl(sockfd, F_GETFL, 0);
    if(flags==-1){
        handleError("fcntl error");
    }if(fcntl(sockfd, F_SETFL, flags | O_NONBLOCK)==-1){
        handleError("Error setting non block");
    }
    
    while(base < TOTAL_NUMS){
        while(next_seq_num < base+WINDOW_SIZE && next_seq_num < TOTAL_NUMS){
            packet.type = DATA_TYPE;
            packet.seq_num = next_seq_num;
            packet.data = data[next_seq_num];
            printf("Sending packet: %d\n", next_seq_num);
            write(sockfd, &packet, sizeof(Packet));
            if(base == next_seq_num){ start_timer(); }
            next_seq_num++;
        }

        ssize_t nbytes = read(sockfd, &ack, sizeof(Packet));
        if(nbytes == 0){
            printf("Server disconnected.\n");
        }else if(nbytes > 0){
            if(ack.type == ACK_TYPE){
                printf("Received: ACK %d\n", ack.seq_num);
                if(ack.seq_num < TOTAL_NUMS){
                    ack_marker[ack.seq_num] = 1;
                }

                if(ack.seq_num == base){
                    while(base < TOTAL_NUMS && ack_marker[base]){ base++; }
                    printf("Window slided to %d.\n", base);
                }
                if(base == next_seq_num){
                    stop_timer();
                }else{
                    start_timer();
                }
            }
        }

        if(timeout()){
            printf("TIMEOUT!!! Selectively resend from %d\n", base);
            start_timer();
            
            for(int i=base;i<next_seq_num;i++){
                if(!ack_marker[i]){
                    packet.type = DATA_TYPE;
                    packet.seq_num = i;
                    packet.data = data[i];
                    printf("Resending packet: %d\n", i);
                    write(sockfd, &packet, sizeof(Packet));
                }
            }
        }
    }
    printf("All numbers sent and ACKed.\n");
    close(sockfd);
    return 0;
}