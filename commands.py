import socket, pynput, random, string, mss, PIL, keyboard, mouse, threading, subprocess, pysftp, datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cau lenh tuong trung cho o cam (socket) cua may khach

# phan ma ket noi su dung ma ID va mat khau xac thuc
# connecting 2 computers using an ID and OTP
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

# chuc nang khoa may tinh
def function_8_logoff():
    # if (flag == 8.333)
    # cac canh bao tren giao dien nguoi dung nham xac nhan viec khoa may tinh va dang xuat
    subprocess.call(["shutdown", "/l "])

# chuc nang khoi dong lai may tinh
def function_8_restart():
    # if (flag == 8.666)
    # cac canh bao tren giao dien nguoi dung nham xac nhan viec khoi dong lai may tinh
    subprocess.call(["shutdown", "/r"])

# chuc nang tat may tinh
def function_8_shutdown():
    # if (flag == 8.999)
    # cac canh bao tren giao dien nguoi dung nham xac nhan viec tat nguon may tinh
    subprocess.call(["shutdown", "/s"])

# chuc nang tinh thoi gian da dieu khien. ham nay se o may khach de tien cho giao dien nguoi dung
def function_12():
    # cac cau lenh tuong trung
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65431        # The port used by the server
    server_address = (HOST, PORT)
    s.connect(server_address)
    conn, addr = s.accept()

    global time_start
    time_start = datetime.datetime.now()

    #....
    #if (flag == 12) truong hop chi khi nguoi dung can tinh toan thoi gian ta moi thuc hien
    time_end = datetime.datetime.now()
    timerun = time_end - time_start
    return timerun

    #if (flag == 12.5) truong hop thoi gian luon hien tren giao dien nguoi dung, khong ngung tin thoi gian theo thoi gian thuc
    # while (van con ket noi):
    # time_end = datetime.datetime.now()
    # timerun = time_end - time_start
    # return timerun


# chuc nang chuyen tep qua lai giua 2 may, truoc het la tu may khach sang may chu
def function_13_client_to_server():
    HOST = '127.0.0.1' # dia chi IP cua may chu minh hoa
    PORT = 65431       # port cua may chu minh hoa
    # if (flag == 13)
    with pysftp.Connection(HOST) as server_connection:
        # phan nhan ten hoac duong dan den ten tep can gui di
        server_connection.put("example.bin", "C:/Users/user/Documents/ExampleDest")
        """
        Phia may chu co the lam the nay de nhan tep:
        # if (flag == 13)
        with pysftp.Connection(client_ip) as server_connection:
            server_connection.get("example.bin", "C:/Users/user/Documents/ExampleDest")
        """

# chuc nang chuyen tep qua lai giua 2 may, sau do la chuyen tep tu may chu sang may khach
def function_13_server_to_client():
    conn, addr = s.accept() # minh hoa viec may chu nhan ket noi tu may khach, addr là dia chi IP cua may khach
    # if (flag == 13.5)
    with pysftp.Connection(addr) as client_connection:
        # phan nhan ten hoac duong dan den ten tep can gui di
        client_connection.put("example.bin", "C:/Users/user/Documents/ExampleDest")
        """
        Phia may khach co the lam the nay de nhan tep:
        # if (flag == 13.5)
        with pysftp.Connection(HOST) as client_connection:
            client_connection.get("example.bin", "C:/Users/user/Documents/ExampleDest")
        """