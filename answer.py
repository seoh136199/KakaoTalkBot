import requests
from bs4 import BeautifulSoup
import random
from jamo import h2j, j2hcj
from unicode import *

from kakao import *

chatData = []
dataIdx = 0
ansCnt = 0

GGMEGData = []

roomName = "카톡봇 테스트"
chatCommands = ["!시각", "!날씨", "!미세먼지", "!삼육구", "!끝말잇기"]

def sendWeather(chatroom_name):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=날씨"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    location = soup.find("span", attrs={"class":"btn_select"}).find("em").get_text()
    currTemp = soup.find("span", attrs={"class":"todaytemp"}).get_text()
    
    currsensibleTemp = soup.find("span", attrs={"class":"sensible"}).find("span", attrs={"class":"num"}).get_text()
    todayMinTemp = soup.find("span", attrs={"class":"min"}).find("span", attrs={"class":"num"}).get_text()
    todayMaxTemp = soup.find("span", attrs={"class":"max"}).find("span", attrs={"class":"num"}).get_text()
    currPrecipitation = soup.find("span", attrs={"class":"rainfall"})
    if (currPrecipitation == None): currPrecipitation = 0
    else: currPrecipitation = currPrecipitation.find("span", attrs={"class":"num"}).get_text()

    text = f"<{location[location.find(' ')+1:]} 날씨>"
    text += f"\n현재 기온 : {currTemp}℃\n체감 기온 : {currsensibleTemp}℃"
    text += f"\n최저/최고 : {todayMinTemp}℃ / {todayMaxTemp}℃"
    text += f"\n시간당 강수량 : {currPrecipitation}mm"

    sendText(chatroom_name, text)


def sendFineDust(chatroom_name):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=날씨"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    location = soup.find("span", attrs={"class":"btn_select"}).find("em").get_text()
    tmpList = soup.find("dl", attrs={"class":"indicator"}).find_all("span", attrs={"class":"num"})
    currFineDust = int(tmpList[0].get_text()[:-3])
    currUltraFineDust = int(tmpList[1].get_text()[:-3])

    explanation = ["좋음😀", "보통😑", "나쁨😨", "매우나쁨🤬"]
    if (currFineDust <= 30): currFineDustIdx = 0
    elif (currFineDust <= 80): currFineDustIdx = 1
    elif (currFineDust <= 150): currFineDustIdx = 2
    else: currFineDustIdx = 3

    if (currUltraFineDust <= 30): currUltraFineDustIdx = 0
    elif (currUltraFineDust <= 80): currUltraFineDustIdx = 1
    elif (currUltraFineDust <= 150): currUltraFineDustIdx = 2
    else: currUltraFineDustIdx = 3

    text = f"<{location[location.find(' ')+1:]} 미세먼지>"
    text += f"\n미세먼지 : {currFineDust}㎍/㎥ {explanation[currFineDustIdx]}"
    text += f"\n초미세먼지 : {currUltraFineDust}㎍/㎥ {explanation[currUltraFineDustIdx]}"

    sendText(chatroom_name, text)


def firstProcessChat(roomName): 
    global dataIdx

    text = copyChat(roomName)
    chatList = text.split('\r\n') 
    del chatList[len(chatList)-1]

    i = 0
    printCurrTime()
    if (len(chatList) - i > 0):
        print(f"기존 채팅이 {len(chatList) - i}개 있습니다.")
    else:
        print("기존 채팅이 없습니다.")

    while (i < len(chatList)):
        if (dataIdx == 100):
            del chatData[0]
            chatData.append(chatList[i])
        else:
            chatData.append(chatList[i])
            dataIdx += 1

        i += 1

    printCurrTime()
    print(f"현재 채팅 데이터 개수 : {dataIdx}")


def processChat(roomName): 
    global dataIdx, ansCnt

    text = copyChat(roomName)
    chatList = text.split('\r\n') 
    del chatList[len(chatList)-1]

    isSame = 0
    currListIdx = len(chatList) - 1
    while (isSame == 0 and currListIdx >= 0):
        if (dataIdx == 0):
            currListIdx = 0
        elif (chatList[currListIdx] == chatData[dataIdx - 1]):
            isSame = 1

            tmpListIdx = currListIdx - 1
            tmpDataIdx = dataIdx - 2
            while (tmpListIdx >= 0 and tmpDataIdx >= 0):
                if (chatList[tmpListIdx] != chatData[tmpDataIdx]):
                    isSame = 0

                tmpListIdx -= 1
                tmpDataIdx -= 1

        currListIdx -= 1
    
    newChatIdx = currListIdx + 2
    cntNewChat = len(chatList) - newChatIdx

    return cntNewChat, chatList[newChatIdx:]


def checkCommand(cntNewChat, chatList): 
    global dataIdx, ansCnt

    if (cntNewChat > 0):
        printCurrTime()
        print(f"새 채팅이 {cntNewChat - ansCnt}개 있습니다.")
    ansCnt = 0

    idx = 0
    while (idx < cntNewChat):
        if (dataIdx == 100):
            del chatData[0]
            chatData.append(chatList[idx])
        else:
            chatData.append(chatList[idx])
            dataIdx += 1

            printCurrTime()
            print(f"현재 채팅 데이터 개수 : {dataIdx}")

        if (chatList[idx][0] == '['):
            contents = chatList[idx].split("] ")[2]
            for cmd in chatCommands:
                if (contents == cmd):
                    printCurrTime()
                    print(f"{cmd} 명령어가 발견되었습니다.")
                    sendAnswer(cmd)

        idx += 1


def cnt369(num):
    cnt = 0
    while (num > 0):
        if (num % 10 == 3 or num % 10 == 6 or num % 10 == 9): cnt += 1
        num //= 10
    return cnt


def play369(roomName):
    global dataIdx, ansCnt
    
    isPlaying369 = 1
    currNum = 1
    printCurrTime()
    print("삼육구 게임이 시작되었습니다.")
    sendText(roomName, "제가 먼저 시작할게요!")
    sleep(0.05)
    sendText(roomName, "1")

    ansCnt += 2
    
    while(isPlaying369):

        tmpList = processChat(roomName)
        cntNewChat = tmpList[0]
        chatList = tmpList[1]
        idx = 0
        while (idx < cntNewChat):
            if (dataIdx == 100):
                del chatData[0]
                chatData.append(chatList[idx])
            else:
                chatData.append(chatList[idx])
                dataIdx += 1

                printCurrTime()
                print(f"현재 채팅 데이터 개수 : {dataIdx}")

            idx += 1

        if (cntNewChat - ansCnt > 1): 
            sendText(roomName, "제 차례를 기다려주세요!")
            ansCnt += 1
            isPlaying369 = 0

        elif (cntNewChat - ansCnt == 1):
            currNum += 1
            contents = chatList[-1].split("] ")[2]
            if ((cnt369(currNum) == 0 and contents == str(currNum)) or (cnt369(currNum) != 0 and contents == "짝" * cnt369(currNum))):
                currNum += 1

                if (cnt369(currNum) == 0): sendText(roomName, str(currNum))
                else: sendText(roomName, "짝" * cnt369(currNum))
                ansCnt += 1

            else:
                sendText(roomName, "틀리셨습니다!")
                ansCnt += 1
                isPlaying369 = 0

        else: ansCnt = 0

        sleep(0.05)

    sleep(0.01)
    sendText(roomName, "다음에 다시 시도해주세요><")


def getWord(firstLetter):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

    myWord = ""

    case = 1
    cuttedLetter = j2hcj(h2j(firstLetter))
    dooum1 = cuttedLetter
    dooum2 = cuttedLetter

    if (cuttedLetter[0] == 'ㄹ'):
        tmp = dooum1
        dooum1 = 'ㅇ' + tmp[1:]
        dooum2 = 'ㄴ' + tmp[1:]
        case = 3
    elif (cuttedLetter[0] == 'ㄴ'):
        dooum1 = 'ㅇ' + dooum1[1:]
        case = 2
    dooum1 = join_jamos(dooum1)
    dooum2 = join_jamos(dooum2)


    caseList = [dooum1, dooum2, firstLetter]

    for i in range(case):
        length = ["두 글자", "세 글자", "네 글자", "다섯 글자", "여섯 글자 이상"]
        for len in length:
            if (myWord == ""):
                url = "https://wordrow.kr/시작하는-말/" + caseList[i] + "/" + len
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, "lxml")
                if (res.status_code != 200):
                    continue

                wordLst = soup.find("div", attrs={"class":"larger"}).find_all("li")
                if (wordLst != None):
                    myWord = random.choice(wordLst)
                    wordLst.remove(myWord)
                    myWord = myWord.find("a")["href"][4:-1]
                    while (myWord in GGMEGData and len(wordLst) > 0):
                        myWord = random.choice(wordLst)
                        wordLst.remove(myWord)
                        myWord = myWord.find("a")["href"][4:-1]

    return myWord

def getProperJosa(word):
    cuttedWord = j2hcj(h2j(word))
    idx = len(cuttedWord) - 1
    while (not is_hangul_compat_jamo(cuttedWord[idx])): idx -= 1

    if (cuttedWord[idx] in CHAR_FINALS): return "은"
    else: return "는"


def playGGMEG(roomName):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

    startWordList = ["사각근", "회전체", "변호사", "전자쌍", "자기장", "와이파이", "실라스타틴나트륨", "고양이", "발사대", "파이썬", "국자", "의미", "실현", "식단", "복사", "이부프로펜", "아이돌", "법원", "아가메온", "보크사이트", "일몰", "보가즈쾨이", "일거삼득", "물리치료", "똠얌꿍"]

    global dataIdx, ansCnt
    
    playGGMEG = 1
    currWord = random.choice(startWordList)
    printCurrTime()
    print("끝말잇기 게임이 시작되었습니다.")

    sendText(roomName, "제가 먼저 시작할게요!")
    sleep(0.05)
    sendText(roomName, currWord)
    
    GGMEGData.append(currWord)

    ansCnt += 2
    
    while(playGGMEG):

        tmpList = processChat(roomName)
        cntNewChat = tmpList[0]
        chatList = tmpList[1]
        idx = 0
        while (idx < cntNewChat):
            if (dataIdx == 100):
                del chatData[0]
                chatData.append(chatList[idx])
            else:
                chatData.append(chatList[idx])
                dataIdx += 1

                printCurrTime()
                print(f"현재 채팅 데이터 개수 : {dataIdx}")

            idx += 1

        if (cntNewChat - ansCnt > 1): 
            sendText(roomName, "제 차례를 기다려주세요!")
            ansCnt += 1
            playGGMEG = 0

        elif (cntNewChat - ansCnt == 1):
            contents = chatList[-1].split("] ")[2]

            cuttedLetter = j2hcj(h2j(currWord[-1]))
            dooum1 = cuttedLetter
            dooum2 = cuttedLetter

            if (cuttedLetter[0] == 'ㄹ'):
                tmp = dooum1
                dooum1 = 'ㄴ' + tmp[1:]
                dooum2 = 'ㅇ' + tmp[1:]
            elif (cuttedLetter[0] == 'ㄴ'):
                dooum1 = 'ㅇ' + dooum1[1:]
            dooum1 = join_jamos(dooum1)
            dooum2 = join_jamos(dooum2)

            url = "https://wordrow.kr/의미/" + contents
            res = requests.get(url, headers=headers)
            
            if (res.status_code == 404):

                sendText(roomName, contents + getProperJosa(contents) + " 없는 단어입니다!")
                ansCnt += 1
                playGGMEG = 0

            elif (contents in GGMEGData):
                sendText(roomName, contents + getProperJosa(contents) +" 이미 나온 단어입니다!")
                ansCnt += 1
                playGGMEG = 0
            
            elif (len(contents) == 1):
                sendText(roomName, "틀리셨습니다!")
                ansCnt += 1
                playGGMEG = 0

            elif (currWord[-1] == contents[0] or dooum1 == contents[0] or dooum2 == contents[0]):
                currWord = getWord(contents[-1])

                if (currWord == ""):
                    sendText(roomName, contents[-1] + "로 시작하는 단어를 찾지 못했어요!")
                    sleep(0.001)
                    sendText(roomName, "당신의 승리입니다!!!")
                    ansCnt += 2
                
                else:
                    GGMEGData.append(contents)
                    sendText(roomName, currWord)
                    GGMEGData.append(currWord)
                    ansCnt += 1

            else:
                sendText(roomName, "틀리셨습니다!")
                ansCnt += 1
                playGGMEG = 0

        else: ansCnt = 0

        sleep(0.05)
        
    sleep(0.01)
    sendText(roomName, "다음에 다시 시도해주세요><")


def sendAnswer(cmd):
    global ansCnt

    if (cmd == "!시각"):
        targetText = ""
        now = time.localtime()
        targetText += "지금은 %04d년 %d월 %d일\n%0d시 %d분 %d초입니다." %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        sendText(roomName, targetText)
        printCurrTime()
        print("시각 응답을 발송했습니다.")
    elif (cmd == "!날씨"): 
        sendWeather(roomName)
        printCurrTime()
        print("날씨 응답을 발송했습니다.")
    elif (cmd == "!미세먼지"): 
        sendFineDust(roomName)
        printCurrTime()
        print("미세먼지 응답을 발송했습니다.")
    elif (cmd == "!삼육구"): 
        play369(roomName)
        printCurrTime()
        print("삼육구 게임이 종료되었습니다.")
    elif (cmd == "!끝말잇기"): 
        playGGMEG(roomName)
        printCurrTime()
        GGMEGData.clear()
        print("끝말잇기 게임이 종료되었습니다.")

    ansCnt += 1