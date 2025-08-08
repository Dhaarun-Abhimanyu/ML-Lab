#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define PORT 5354
#define BUFFER_SIZE 256
#define DNS_TABLE_SIZE 12
// Predefined DNS records
struct dns_record {
 char domain[32];
 char ip[16];
};
struct dns_record dns_database[DNS_TABLE_SIZE] = {
 {"example.com", "93.184.216.34"},
 {"google.com", "142.250.190.14"},
 {"openai.com", "104.18.12.123"},
 {"github.com", "140.82.113.3"},
 {"yahoo.com", "98.137.11.163"},
 {"amazon.com", "176.32.103.205"},
 {"facebook.com", "157.240.20.35"},
 {"apple.com", "17.172.224.47"},
 {"microsoft.com", "40.113.200.201"},
 {"netflix.com", "52.26.14.20"},
 {"nasa.gov", "129.164.179.22"},
 {"wikipedia.org", "208.80.154.224"}
};
// Function to find the IP address for a given domain
const char* resolve_domain(const char* domain_name) {
 for (int i = 0; i < DNS_TABLE_SIZE; i++) {
 if (strcmp(dns_database[i].domain, domain_name) == 0) {
 return dns_database[i].ip;
 }
 }
 return "Domain not found";
}
int main() {
 int sockfd_server, sockfd_client;
 struct sockaddr_in servaddr, cliaddr;
 char buffer[BUFFER_SIZE];

 // Read the domain name from standard input
 if (fgets(buffer, BUFFER_SIZE, stdin) == NULL) {
 return 1;
 }
 buffer[strcspn(buffer, "\n")] = 0; // Remove newline character
 const char* domain_query = strdup(buffer);
 // --- SERVER LOGIC ---

 // Creating server socket
 if ((sockfd_server = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
 perror("server socket creation failed");
 exit(EXIT_FAILURE);
 }

 memset(&servaddr, 0, sizeof(servaddr));

 // Filling server information
 servaddr.sin_family = AF_INET;
 servaddr.sin_addr.s_addr = inet_addr("127.0.0.1"); // Using loopback address
 servaddr.sin_port = htons(PORT);

 // Bind the socket with the server address
 if (bind(sockfd_server, (const struct sockaddr *)&servaddr,
sizeof(servaddr)) < 0) {
 perror("server bind failed");
 exit(EXIT_FAILURE);
 }

 printf("[DNS Server] Waiting for domain query...\n");
 fflush(stdout);
 // --- CLIENT LOGIC ---

 // Creating client socket
 if ((sockfd_client = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
 perror("client socket creation failed");
 exit(EXIT_FAILURE);
 }

 // Send domain query to the server
 printf("[DNS Client] Query sent for: %s\n", domain_query);
 fflush(stdout);
 sendto(sockfd_client, domain_query, strlen(domain_query), 0, (const
struct sockaddr *)&servaddr, sizeof(servaddr));

 // --- SERVER CONTINUES ---
 socklen_t len = sizeof(cliaddr);
 int n = recvfrom(sockfd_server, (char *)buffer, BUFFER_SIZE, 0,
(struct sockaddr *)&cliaddr, &len);
 buffer[n] = '\0';

 printf("[DNS Server] Query received for domain: %s\n", buffer);
 fflush(stdout);

 // Resolve the domain and get the IP
 const char* ip_response = resolve_domain(buffer);

 printf("[DNS Server] Sent IP: %s\n", ip_response);
 fflush(stdout);

 // Send the IP response back to the client
 sendto(sockfd_server, ip_response, strlen(ip_response), 0, (const
struct sockaddr *)&cliaddr, len);

 // --- CLIENT CONTINUES ---
 // Receive IP response from the server
 n = recvfrom(sockfd_client, (char *)buffer, BUFFER_SIZE, 0, (struct
sockaddr *)&servaddr, &len);
 buffer[n] = '\0';

 printf("[DNS Client] IP received: %s\n", buffer);
 fflush(stdout);

 // Close sockets
 close(sockfd_server);
 close(sockfd_client);
 free((void*)domain_query);
 return 0;
}
