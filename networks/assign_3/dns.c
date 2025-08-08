#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#define PORT 5354
#define BUFFER_SIZE 256
#define DNS_TABLE_SIZE 12
// Predefined DNS table
struct dns_entry {
 char ip[16];
 char domain[32];
};
struct dns_entry dns_table[DNS_TABLE_SIZE] = {
 {"93.184.216.34", "example.com"},
 {"142.250.190.14", "google.com"},
 {"104.18.12.123", "openai.com"},
 {"140.82.113.3", "github.com"},
 {"98.137.11.163", "yahoo.com"},
 {"176.32.103.205", "amazon.com"},
 {"157.240.20.35", "facebook.com"},
 {"17.172.224.47", "apple.com"},
 {"40.113.200.201", "microsoft.com"},
 {"52.26.14.20", "netflix.com"},
 {"129.164.179.22", "nasa.gov"},
 {"208.80.154.224", "wikipedia.org"}
};
// Function to find the domain name for a given IP
const char* resolve_ip(const char* ip) {
 for (int i = 0; i < DNS_TABLE_SIZE; i++) {
 if (strcmp(dns_table[i].ip, ip) == 0) {
 return dns_table[i].domain;
 }
 }
 return "IP not found";
}
void server_process() {
 int sockfd;
 struct sockaddr_in servaddr, cliaddr;
 socklen_t len = sizeof(cliaddr);
 char buffer[BUFFER_SIZE];

 // Creating socket file descriptor
 if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
 perror("socket creation failed");
 exit(EXIT_FAILURE);
 }

 memset(&servaddr, 0, sizeof(servaddr));
 memset(&cliaddr, 0, sizeof(cliaddr));

 // Filling server information
 servaddr.sin_family = AF_INET;
 servaddr.sin_addr.s_addr = INADDR_ANY;
 servaddr.sin_port = htons(PORT);

 // Bind the socket with the server address
 if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr))
< 0) {
 perror("bind failed");
 exit(EXIT_FAILURE);
 }

 printf("[Reverse DNS Server] Waiting for IP query...\n");
 fflush(stdout);

 // Receive IP query from client
 int n = recvfrom(sockfd, (char *)buffer, BUFFER_SIZE, 0, (struct
sockaddr *)&cliaddr, &len);
 buffer[n] = '\0';

 printf("[Reverse DNS Server] Query received for IP: %s\n", buffer);
 fflush(stdout);

 // Resolve IP to domain
 const char* domain = resolve_ip(buffer);

 printf("[Reverse DNS Server] Sent domain: %s\n", domain);
 fflush(stdout);

 // Send resolved domain back to client
 sendto(sockfd, domain, strlen(domain), 0, (const struct sockaddr
*)&cliaddr, len);

 close(sockfd);
}
void client_process(const char* ip_to_resolve) {
 int sockfd;
 struct sockaddr_in servaddr;
 char buffer[BUFFER_SIZE];

 // Creating socket file descriptor
 if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
 perror("socket creation failed");
 exit(EXIT_FAILURE);
 }

 memset(&servaddr, 0, sizeof(servaddr));

 // Filling server information
 servaddr.sin_family = AF_INET;
 servaddr.sin_port = htons(PORT);
 servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

 // Send IP query to server
 printf("[Reverse DNS Client] Query sent for IP: %s\n", ip_to_resolve);
 fflush(stdout);
 sendto(sockfd, ip_to_resolve, strlen(ip_to_resolve), 0, (const struct
sockaddr *)&servaddr, sizeof(servaddr));

 // Receive domain from server
 socklen_t len = sizeof(servaddr);
 int n = recvfrom(sockfd, (char *)buffer, BUFFER_SIZE, 0, (struct
sockaddr *)&servaddr, &len);
 buffer[n] = '\0';

 printf("[Reverse DNS Client] Domain received: %s\n", buffer);
 fflush(stdout);

 close(sockfd);
}
int main() {
 char ip_query[BUFFER_SIZE];

 if (fgets(ip_query, BUFFER_SIZE, stdin) == NULL) {
 return 1;
 }
 ip_query[strcspn(ip_query, "\n")] = 0; // Remove newline character

 pid_t pid = fork();

 if (pid < 0) {
 perror("fork failed");
 exit(EXIT_FAILURE);
 }

 if (pid == 0) { // Child process (client)
 sleep(1); // Wait for server to start
 client_process(ip_query);
 } else { // Parent process (server)
 server_process();
 }

 return 0;
}