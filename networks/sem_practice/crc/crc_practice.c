#include <stdio.h>
#include <string.h>

#define N 100

void xor(char* dividend, char* divisor, int pos){
    for(int i=0; divisor[i] != '\0'; i++){
        dividend[pos+i] = (dividend[pos+i] == divisor[i]) ? '0' : '1';
    }
}

void crcCompute(char data[], char gen[], char remainder[]){
    char temp[N];
    int data_len = strlen(data);
    int gen_len = strlen(gen);

    strcpy(temp, data);
    for(int i=0;i<gen_len-1;i++){
        temp[i+data_len] = '0';
    }
    temp[data_len + gen_len - 1] = '\0';

    for(int i=0;i <= strlen(temp) - gen_len; i++){
        if (temp[i] == '1'){
            xor(temp, gen, i);
        }
    }

    strcpy(remainder, temp+strlen(temp) - gen_len + 1);
}

int main() {
    char data[N], gen[N], remainder[N], transmitted[N], recv_data[N];

    printf("Enter data bits: ");
    scanf("%s", data);
    printf("Enter generator polynomial: ");
    scanf("%s", gen);

    crcCompute(data, gen, remainder);

    strcpy(transmitted, data);
    strcat(transmitted, remainder);

    printf("Transmitted codeword: %s\n", transmitted);
    printf("\nEnter received data (correct or wrong): ");
    scanf("%s", recv_data);

    crcCompute(recv_data, gen, remainder);

    int error_flag = 0;
    for(int i=0; remainder[i] != '\0'; i++){
        if(remainder[i] == '1'){
            error_flag = 1;
            break;
        }
    }

    if(error_flag){
        printf("\nError detected!!!\n");
    }else{
        printf("\nNo error detected. Data received correctly.\n");
    }

    return 0;
}