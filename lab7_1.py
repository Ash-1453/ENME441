import RPi.GPIO as GPIO
import threading
from time import sleep
import socket
GPIO.setmode(GPIO.BCM)
led_pin=[14,15,18]
pwm_instance=[]
led_brightness=[0,0,0]
y=0
for x in led_pin:
    GPIO.setup(x,GPIO.OUT)
    pwm=GPIO.PWM(x,1000)
    pwm_instance.append(pwm)
    pwm_instance[y].start(0)
    y+=1
def web_page(led_brightness):
    html="""
    <html>
    <head>
        <title>LED Brightness control </title>
    </head>
    <body>
        <form action="/" method="POST">
            <p>Brightness level:</p>
            <input type="range" name="brightness" min ="0" max="100"
            value ="50"/><br><br>
            <label>Select LED:</label><br>
            <input type="radio" name="led" value="0" checked> LED 1 (""" +str(led_brightness[0])+ """%) <br>
            <input type="radio" name="led" value="1"> LED 2 (""" +str(led_brightness[1])+ """%)<br>
            <input type="radio" name="led" value="2"> LED 3 (""" +str(led_brightness[2])+ """%)<br><br>
            <input type="submit" value="Change Brightness">
        </form>
    </body>
    </html>"""
    return bytes(html, 'utf-8')
def parsePOSTdata(data):
    data_dict = {}
    data=data.decode('utf-8')
    idx = data.find('\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict
def client_web_page():
    conn, (client_adress,client_port)=s.accept()
    data_dict=parsePostdata(conn.recv(2048))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",80))
s.listen(3)
try:
    while True:
        conn, (client_adress,client_port)=s.accept()
        data_dict=parsePOSTdata(conn.recv(2048))
        if"brightness" in data_dict.keys() and "led" in data_dict.keys():
            pin_led=int(data_dict["led"])
            led_brightness[pin_led]=int(data_dict["brightness"])
            pwm_instance[pin_led].ChangeDutyCycle(led_brightness[pin_led])
        
            conn.send(b'HTTP/1.1 200 OK\r\n')
            conn.send(b'Content-Type: text/html\r\n')  
        else:
            conn.send(b'HTTP/1.1 200 OK\r\n')
            conn.send(b'Content-Type: text/html\r\n')   
            conn.sendall(web_page(led_brightness))
        conn.close()
except KeyboardInterrupt:
    print("exiting")
finally:
    for x in pwm_instance:
        x.stop()
    GPIO.cleanup()
    s.close()