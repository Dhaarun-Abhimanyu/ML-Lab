#ifndef PACKET_H
#define PACKET_H

#define PORT 8080
#define WINDOW_SIZE 4
#define TOTAL_NUMS 10

#define DATA_TYPE 0
#define ACK_TYPE 1
#define TIMEOUT_SEC 2.0

typedef struct {
    int type;
    int seq_num;
    int data;
} Packet;

void handleError(const char* msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

#endif