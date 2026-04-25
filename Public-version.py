import win32api
import win32con
import time
import threading
running = True
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def toggle_program():
    """按 F8 启动/停止程序"""
    global running
    print(f"程序 {'启动' if running else '停止'}")
def click_at(x, y, times=1, interval=0.1,t=0.05):
    """在指定坐标连续点击鼠标左键"""
    for i in range(times):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(t)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(interval)
def press_key(key_code,t=0.05):
    win32api.keybd_event(key_code, 0, 0, 0)
    time.sleep(t)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
def throw():
    for i in [0x31,0x33,0x34,0x35,0x36]:
        time.sleep(0.5)
        press_key(i)
        time.sleep(0.5)
        click_at(50,100,1,0.1,0.7)
    time.sleep(0.5)
def pose():
    time.sleep(1)
    press_key(0x09)  # tab
    time.sleep(1)
    press_key(0x32)  # 2
    time.sleep(4)
    press_key(0x1b)  # esc
    time.sleep(1)
    press_key(0x32)  # 2
    time.sleep(1)
    press_key(0x52)  # r
    time.sleep(19)
    press_key(0x58)  # x
    time.sleep(1)
def auto_press_keys():
    time.sleep(2)
    throw()
    while True:
        if running:
            pose()
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    # print("按 F8 启动/停止程序")
    if is_admin():
        print("有管理员权限")
    else:
        print("无管理员权限，请同意")
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    print("本程序默认在2号位放置灵巧精灵，其他位放奇丽草。")
    input("按回车后开始，按回车后请立刻自行切换回洛克王国：")
    # 启动自动按键线程

    thread = threading.Thread(target=auto_press_keys, daemon=True)
    thread.start()
    toggle_program()
    # 监听 F8 按键
    try:
        while True:
            # 检测 F8 是否被按下
            if win32api.GetAsyncKeyState(0x77) & 0x8000:  # F8 = 0x77
                toggle_program()
                time.sleep(0.3)  # 防止重复触发
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n程序已停止。")
