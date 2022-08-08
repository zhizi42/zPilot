#pragma once

#include <iostream>
#include <WinSock2.h>

bool initConnect();
int sendMsg(char* msg);
char* recvMsg();