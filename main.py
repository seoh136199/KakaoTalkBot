from kakao import *
from answer import *

def main():
    
    openChatroom(myRoomName)
    sleep(0.1)

    firstProcessChat(myRoomName)

    while (True):
        tmpList = processChat(myRoomName)
        checkCommand(tmpList[0], tmpList[1])
        sleep(0.01)


if __name__ == '__main__':
    main()