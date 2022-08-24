#include "Connect.h"
#include <string>
#include <stdlib.h>
#pragma warning(disable:4996)

SOCKET s;

bool initConnect()
{
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    SOCKADDR_IN addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
    addr.sin_port = htons(446);
    int connectResult = connect(s, (SOCKADDR*)&addr, sizeof(SOCKADDR));
    if (connectResult == 0) {
        return true;
    }
    else {
        return false;
    }
}

int sendMsg(char* msg) {
    int sendLen = send(s, msg, strlen(msg), 0);
    return sendLen;
}

char* recvMsg() {
    char len[5];
    recv(s, len, 4, 0);
    int recvLen = atoi(len);
    char* msg = new char[recvLen + 1]();
    recv(s, msg, recvLen, 0);
    std::cout << msg << std::endl;
    return msg;
}