# phan ma ket noi su dung ma ID va mat khau xac thuc
# connecting 2 computers using an ID and OTP
import socket, pynput, random, string, mss, PIL, keyboard, mouse, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cau lenh tuong trung cho o cam (socket) cua may khach

def otp_generator():
    result = str("")
    rand_list = list(string.ascii_lowercase).append(['0','1','2','3','4','5','6','7','8','9'])
    for i in range(8):
        character = random.choice(rand_list)
        result += character
    return result

# chuc nang ket noi 2 may tinh su dung mat khau xac thuc va id
def function_1():
    id_server = random.randint(100000000000, 999999999)
    pass_server = otp_generator()
    # cho de lap trinh phan in id va pass mgau nhien len man hinh may chu
    # phan nhap id va pass tren may khach
    isValid = False
    times_to_input = 5
    while not isValid and times_to_input != 0:
        id_client = int(input("Nhap id: "))
        pass_client = str(input("Nhap otp: "))
        isValid = id_server == id_client and pass_server == pass_client
        if not isValid:
            times_to_input -= 1
            print("Ban con " + str(times_to_input) + " lan nhap.\n")    
    else:
        if isValid:
            print('Dang nhap thanh cong')
            return True
        elif not times_to_input:
            print('Dang nhap that bai')
            return False

# chuc nang chup anh man hinh
def function_3_capture():
    # if (flag = 3.5)
    bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    with mss.mss() as sct:
        sct_img = sct.grab(bounding_box)
        # luu lai thong tin man hinh
        img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # in anh ra man hinh
        output = "screenshot.png"
        img.save(output)
        print(output)
        return output
    
# chuc nang su dung chuot de dieu khien thiet bi theo mong muon
def function_5_mouse():
    mouse_events = []

    def on_move(x, y):
        # cau lenh tuong trung nham luu lai du lieu ve hanh dong cua chuot
        mouse_events.append(('move', (x, y)))
        # cau lenh tuong trung viec tim cach gui du lieu la mang tinh (tuple) tren sang may chu
        s.sendall(str(('move', (x, y))).encode())

    def on_click(x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        mouse_events.append(('click', (x, y, button, action)))
        # cau lenh tuong trung viec tim cach gui du lieu la mang tinh (tuple) tren sang may chu
        s.sendall(str(('click', (x, y, button, action))).encode())

    def on_scroll(x, y, dx, dy):
        mouse_events.append(('scroll', (x, y, dx, dy)))
        # cau lenh tuong trung viec tim cach gui du lieu la mang tinh (tuple) tren sang may chu
        s.sendall(str(('scroll', (x, y, dx, dy))).encode())

    # Lay thong tin ve cac hanh dong cua chuot
    
    listener = pynput.mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    listener.start()
    #if (# nguoi dung yeu cau huy ket noi):
        #listener.stop()
"""
Mot cach khac de tiep can cho ham nay:
with mouse.Events() as events:
    for event in events:
        if # nguoi dung yeu cau huy ket noi:
            break
        else:
            s.sendall(str(event).encode())
nhung khi do viec phan giai thanh event se tuong doi kho
"""


"""Ben may chu can lam nhu the nay de giai ma:
# Nhận dữ liệu từ máy khách
data = conn.recv(1024)

# Giải mã dữ liệu nhị phân thành chuỗi
data_str = data.decode()

# Phân giải chuỗi thành tuple
mouse_event = literal_eval(data_str)

# Kiểm tra dữ liệu
if isinstance(mouse_event, tuple) and mouse_event[0] == 'click':
    # Lấy thông tin từ tuple
    action = mouse_event[1]"""

# chuc nang su dung ban phim de dieu khien thiet bi theo mong muon
def function_5_keyboard():
    keyboard_events = []
    def on_press(key):
        try:
            keyboard_events.append(('press', key.char))
            s.sendall(str(('press', key.char)).encode())
        except AttributeError:
            keyboard_events.append(('press', key))
            s.sendall(str(('press', key)).encode())

    def on_release(key):
        print('{0} released'.format(
            key))
        keyboard_events.append(('release', key))
        s.sendall(str(('release', key)).encode())

    listener = pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    #if (# nguoi dung yeu cau huy ket noi):
        #listener.stop()

# chuc nang chan su dung chuot cua thiet bi dieu khien
def function_6_mouse():
    # if (flag == 6.5)
    global executing_mouse_disability
    executing_mouse_disability = True  # Khởi tạo biến với giá trị True để bắt đầu di chuyển chuột

    def disable_mouse():
        # Hàm này sẽ di chuyển chuột đến vị trí (1,0) cho đến khi biến executing là False
        global executing_mouse_disability
        pos = mouse.get_position()
        while executing_mouse_disability:
            mouse.move(*pos, absolute=True, duration=0)  # Di chuyển chuột tai dung vi tri nay mai mai

    def stop_infinite_mouse_control():
        # Hàm này sẽ dừng việc chan di chuyển chuột khi co tin hieu dung viec chan tu may khach 
        # if (flag == 6.55)
        global executing_mouse_disability
        executing_mouse_disability = False  # Đặt biến executing thành False để dừng vòng lặp trong hàm disable_mouse
    threading.Thread(target=disable_mouse).start()

    # Tạo và khởi chạy luồng mới để dừng việc chan di chuyển chuột khi co tin hieu dung viec chan tu may khach 
    threading.Thread(target=stop_infinite_mouse_control).start()


# chuc nang chan su dung ban phim cua thiet bi dieu khien
def function_6_keyboard():
    # if (flag == 6)
    global executing_keyboard_disability
    executing_keyboard_disability = True  # Khởi tạo biến với giá trị True để bàn phim khong hoat hong

    def disable_keyboard():
        # Hàm này sẽ chan su dung toan bo ban phim
        global executing_keyboard_disability
        while executing_keyboard_disability:
            for i in range(150):
                keyboard.block_key(i)

    def stop_infinite_keyboard_control():
        # Hàm này sẽ dừng việc chan ban phim khi co tin hieu dung viec chan tu may khach 
        # if (flag == 6.05)
        global executing_keyboard_disability
        executing_keyboard_disability = False  # Đặt biến executing thành False để dừng vòng lặp trong hàm move_mouse
    threading.Thread(target=disable_keyboard).start()

    # Tạo và khởi chạy luồng mới để dừng việc di chuyển chuột khi co tin hieu dung viec chan tu may khach 
    threading.Thread(target=stop_infinite_keyboard_control).start()

