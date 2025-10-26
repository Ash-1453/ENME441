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
def web_page():
    html=f"""
        <html>
            <head>
                <title>LED Brightness Control</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                .slider-container {{ margin: 20px; }}
                label {{ font-size: 1.2em; }}
            </style>

            <script>
                function updateLED(ledIndex, value) {{
                    document.getElementById("val" + ledIndex).innerText = value + "%";

                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xhr.send("led=" + ledIndex + "&brightness=" + value);
                }}
            </script>
            </head>

            <body>
                <h1>LED Brightness Control</h1>

                <div class="slider-container">
                    <label>LED 1 Brightness: <span id="val0">{led_brightness[0]}%</span></label><br>
                    <input type="range" min="0" max="100" value="{led_brightness[0]}"
                        oninput="updateLED(0, this.value)">
                </div>

                <div class="slider-container">
                    <label>LED 2 Brightness: <span id="val1">{led_brightness[1]}%</span></label><br>
                    <input type="range" min="0" max="100" value="{led_brightness[1]}"
                        oninput="updateLED(1, this.value)">
                </div>

                <div class="slider-container">
                    <label>LED 3 Brightness: <span id="val2">{led_brightness[2]}%</span></label><br>
                    <input type="range" min="0" max="100" value="{led_brightness[2]}"
                        oninput="updateLED(2, this.value)">
                </div>
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
        conn.send(b'HTTP/1.1 200 OK\r\n')
        conn.send(b'Content-Type: text/html\r\n')
        if"brightness" in data_dict.keys() and "led" in data_dict.keys():
            pin_led=int(data_dict["led"])
            led_brightness[pin_led]=int(data_dict["brightness"])
            pwm_instance[pin_led].ChangeDutyCycle(led_brightness[pin_led])
        
            
            conn.sendall(web_page())  
        else:
               
            conn.sendall(web_page())
        conn.close()
except KeyboardInterrupt:
    print("exiting")
finally:
    for x in pwm_instance:
        x.stop()
    GPIO.cleanup()
    s.close()