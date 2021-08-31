from kakao import *
from answer import *

def main():
    
    openChatroom(roomName)
    sleep(0.1)

    firstProcessChat(roomName)

    while (True):
        tmpList = processChat(roomName)
        checkCommand(tmpList[0], tmpList[1])
        sleep(0.01)


if __name__ == '__main__':
    main()

    #commit test