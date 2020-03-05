
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>
int ftp(int socketfd, char* filename, char type);
int main(int argc, char* argv[]) {
    int so;
    char s[100];
    struct sockaddr_in ad;

    socklen_t ad_length = sizeof(ad);
    struct hostent *hep;

    // create socket
    int serv = socket(AF_INET, SOCK_STREAM, 0);
    if (argc == 1) {
    	printf("Usage: ./client <ip>\n");
	exit(1);
    }
    // init address
    hep = gethostbyname(argv[1]);
    memset(&ad, 0, sizeof(ad));
    ad.sin_family = AF_INET;
    ad.sin_addr = *(struct in_addr *)hep->h_addr_list[0];
    ad.sin_port = htons(12345);

    // connect to server
    connect(serv, (struct sockaddr *)&ad, ad_length);
    printf("ftp [-r receive|-s send] filename\n");
    printf("Ex: ftp -r file.ext\n");
    while (1) {
        // after connected, it's client turn to chat

        // send some data to server
        printf("client>");
        fgets(s, 100, stdin);
        
	write(serv, s, strlen(s) + 1);
	
	if (strncmp(s, "ftp ",4) == 0) {
		char file[100];
		strncpy(file, s+7, 100);
		int f = ftp(serv, file, s[5]);
		continue;
	}
        
	// then it's server turn
        read(serv, s, sizeof(s));
        printf("server says: %s\n", s);
    }
}

int ftp(int socketfd, char* filename, char type) {
    int fd; 
    char buff[100];

   *(rindex(filename, '\n')) = '\0'; // remove newline char in filepath 

    if (type == 'r') {
	fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC , S_IRWXU);
	read(socketfd, buff, 100); 
	while (buff[0] != '\0') {
	        printf("%s", buff);
		write(fd, buff, 100);
	   	read(socketfd, buff, 100);	
	}
	write(fd, '\0', 1);
	printf("Success downloading file: %s\n", filename);
	close(fd);
	return 1;
    }

    if (type == 's') {
    	printf("Starting transfer file: %s\n", filename);
	fd = open(filename, O_RDONLY);
	while (read(fd, buff, 100)) {
		write(socketfd, buff, 100);
	}
	write(socketfd, "\0", 1);
	close(fd);
	printf("Transfer complete\n");
        return 1;
    }
}
