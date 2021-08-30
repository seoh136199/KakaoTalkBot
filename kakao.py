import time, win32con, win32api, win32gui, ctypes
from pywinauto import clipboard
from pyautogui import *
import win32clipboard
import time

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
PostMessage = win32api.PostMessage
SendMessage = win32gui.SendMessage
FindWindow = win32gui.FindWindow
IsWindow = win32gui.IsWindow
GetCurrentThreadId = win32api.GetCurrentThreadId
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
AttachThreadInput = _user32.AttachThreadInput

MapVirtualKeyA = _user32.MapVirtualKeyA
MapVirtualKeyW = _user32.MapVirtualKeyW

MakeLong = win32api.MAKELONG

def printCurrTime():
    now = time.localtime()
    print("[%04d-%02d-%02d %02d:%02d:%02d] " %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec), end='')


def PostKeyEx(hwnd, key, shift, specialkey):
    if IsWindow(hwnd):

        ThreadId = GetWindowThreadProcessId(hwnd, None)

        lparam = MakeLong(0, MapVirtualKeyA(key, 0))
        msg_down = win32con.WM_KEYDOWN
        msg_up = win32con.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        if len(shift) > 0:
            pKeyBuffers = PBYTE256()
            pKeyBuffers_old = PBYTE256()

            SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, True)
            GetKeyboardState(ctypes.byref(pKeyBuffers_old))

            for modkey in shift:
                if modkey == win32con.VK_MENU:
                    lparam = lparam | 0x20000000
                    msg_down = win32con.WM_SYSKEYDOWN
                    msg_up = win32con.WM_SYSKEYUP
                pKeyBuffers[modkey] |= 128

            SetKeyboardState(ctypes.byref(pKeyBuffers))
            time.sleep(0.001)
            PostMessage(hwnd, msg_down, key, lparam)
            time.sleep(0.001)
            PostMessage(hwnd, msg_up, key, lparam | 0xC0000000)
            time.sleep(0.001)
            SetKeyboardState(ctypes.byref(pKeyBuffers_old))
            time.sleep(0.001)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, False)

        else:
            SendMessage(hwnd, msg_down, key, lparam)
            SendMessage(hwnd, msg_up, key, lparam | 0xC0000000)


def copyChat(chatroom_name):
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndListControl = win32gui.FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)
    PostKeyEx(hwndListControl, ord('A'), [win32con.VK_CONTROL], False)
    time.sleep(0.001)
    PostKeyEx(hwndListControl, ord('C'), [win32con.VK_CONTROL], False)
    time.sleep(0.07)

    tryCnt = 0
    while (tryCnt < 3):
        tryCnt += 1
        try:
            win32clipboard.OpenClipboard()
            break
        except:
            printCurrTime()
            print("OpenClipboard()에서 에러가 발생했습니다.")
            time.sleep(0.001)

    if (tryCnt > 1):
        printCurrTime()
        print("OpenClipboard() 실행에 성공했습니다.")

    ctext = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return ctext


def sendText(chatroom_name, text):
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RICHEDIT50W", None)
    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    sendReturn(hwndEdit)


def sendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.001)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def openChatroom(chatroom_name):
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakaoEdit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakaoEdit2_1 = win32gui.FindWindowEx(hwndkakaoEdit1, None, "EVA_Window", None)
    hwndkakaoEdit2_2 = win32gui.FindWindowEx(hwndkakaoEdit1, hwndkakaoEdit2_1, "EVA_Window", None)
    hwndkakaoEdit3 = win32gui.FindWindowEx(hwndkakaoEdit2_2, None, "Edit", None)

    win32api.SendMessage(hwndkakaoEdit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(0.5)
    sendReturn(hwndkakaoEdit3)
    time.sleep(0.5)
