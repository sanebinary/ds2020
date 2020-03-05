#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <fcntl.h>
 #include <unistd.h>
int ftp(int sockfd, char* filename, char type);
int main() {
    int ss, cli, pid;
    struct sockaddr_in ad;
    char s[100];
    socklen_t ad_length = sizeof(ad);

    // create the socket
    ss = socket(AF_INET, SOCK_STREAM, 0);

    // bind the socket to port 12345
    memset(&ad, 0, sizeof(ad));
    ad.sin_family = AF_INET;
    ad.sin_addr.s_addr = INADDR_ANY;
    ad.sin_port = htons(12345);
    bind(ss, (struct sockaddr *)&ad, ad_length);

    // then listen
    listen(ss, 0);

    while (1) {
        // an incoming connection
        cli = accept(ss, (struct sockaddr *)&ad, &ad_length);

        pid = fork();
        if (pid == 0) {
            // I'm the son, I'll serve this client
            printf("client connected\n");
            while (1) {
                // it's client turn to chat, I wait and read message from client
                read(cli, s, sizeof(s));
                printf("client says: %s\n",s);
		
		if (strncmp(s, "ftp ", 4) == 0) {
			char file[100];
			strncpy(file, s+7,100);
			printf(file);
			ftp(cli, file, s[5]);
			continue;
		} 
                 // now it's my (server) turn
                 printf("server>", s);
                 scanf("%s", s);
                 write(cli, s, strlen(s) + 1);
            }
            return 0;
        }
        else {
            // I'm the father, continue the loop to accept more clients
            continue;
        }
    }
    // disconnect
    close(cli);

}

int ftp(int sockfd, char* filename, char type) {
	char buff[100];
	int fd;
	
	*(rindex(filename, '\n')) = '\0'; // remove newline char in filepath
	
	// client download file
	if (type == 'r') {
		printf("Starting transfer file: %s\n", filename);
		fd = open(filename, O_RDONLY);
		while(read(fd, buff, 100)) {
			write(sockfd, buff, 100);
			memset(buff, 0, 100);
		}
		write(sockfd, "\0", 1);
		close(fd);
		printf("Transfer complete\n");
		return 1;
	}
	// client upload file 
	if (type == 's') {
		printf("Starting receive file: %s\n", filename);
		fd = creat(filename, S_IRWXG);
		read(sockfd, buff, 100);
		while(buff[0] != '\0') {
			write(fd, buff, 100);
			read(sockfd, buff, 100);
		}
		write(fd, '\0', 1);
		close(fd);
		printf("Success");
		return 1;
	}
}
