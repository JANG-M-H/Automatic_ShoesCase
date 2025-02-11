import RPi.GPIO as GPIO 
import time
import Adafruit_DHT
from RPLCD import i2c

LED_PIN = 7
BUTTON_PIN = 8
sensor = Adafruit_DHT.DHT11  
pin = 22
FAN_PIN = 26
FAN_PIN1 = 19
GAS_pin = 9
UV_pin = 5
UV_pin1 = 11
BUZ_pin = 4

GPIO.setmode(GPIO.BCM)  
GPIO.setup(LED_PIN,GPIO.OUT) 
GPIO.setup(BUTTON_PIN,GPIO.IN)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN1, GPIO.OUT)
GPIO.setup(GAS_pin, GPIO.OUT)
GPIO.setup(UV_pin, GPIO.OUT)
GPIO.setup(UV_pin1, GPIO.OUT)
GPIO.setup(BUZ_pin, GPIO.OUT)

i2c_expander = 'PCF8574'  # I2C 확장 모듈 (PCF8574)을 사용하는 경우
i2c_address = 0x27  # LCD1602의 I2C 주소 (주소는 SSS실제 하드웨어에 따라 다를 수 있음)

lcd_columns = 16
lcd_rows = 2

lcd = i2c.CharLCD(i2c_expander, i2c_address, cols=lcd_columns, rows=lcd_rows)

def read_sensor():
    lcd.clear()
    lcd.write_string("TEST HUMIDITY")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('TEMP={0:0.1f}°C  HUM={1:0.1f}%'.format(temperature, humidity))
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("TEST HUMIDITY")
        lcd.cursor_pos = (1, 0)
        lcd.write_string('HUM={0:0.1f}%'.format(humidity))    
    else:
        print('again')
        
    return humidity

def turn_fan_on():
    GPIO.output(FAN_PIN, GPIO.HIGH)
    GPIO.output(FAN_PIN1, GPIO.HIGH)
    #print("ON")

def turn_fan_off():
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.output(FAN_PIN1, GPIO.LOW)
   # print("OFF")

def control_fan(status):
    if status == 'on':
        GPIO.output(GAS_pin, GPIO.HIGH)
        print("환풍기가 켜졌습니다.")
    elif status == 'off':
        GPIO.output(GAS_pin, GPIO.LOW)
        print("환풍기가 꺼졌습니다.")
    else:
        print("올바른 상태를 입력하세요.")


try:
    GPIO.output(GAS_pin, GPIO.LOW)
    GPIO.output(UV_pin, GPIO.LOW)
    GPIO.output(UV_pin1, GPIO.LOW)
    lcd.clear()
    lcd.write_string("START")
    time.sleep(1)
    
    while True:
        if GPIO.input(BUTTON_PIN) == False:    
            GPIO.output(LED_PIN, GPIO.HIGH) 
            read_sensor()
            humidity = read_sensor()
            time.sleep(1)
            #if humidity > 80:
                #print("ON")
            while humidity > 80:
                turn_fan_on()
                print("FAN ON")
                read_sensor()
                humidity = read_sensor()
                time.sleep(1)
            #print("OFF")
            if humidity <= 80:
                turn_fan_off()
                print("FAN OFF")
                lcd.clear()
                lcd.cursor_pos = (0, 0)
                lcd.write_string("HUMIDITER ON")
                control_fan('on')
                TIME = 10
                for sec in range(TIME + 1):
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string("HUMIDITER")
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string(f"Remained_Time:{TIME}s")
                    #lcd.write_string('HUM={0:0.2f}s'.format(TIME))
                    TIME -= 1
                    time.sleep(1)
                    lcd.clear()
                #time.sleep(10)
                control_fan('off')
                lcd.write_string("HUMIDITER OFF")
                time.sleep(1)
                lcd.clear()
                lcd.write_string("UV LIGHT ON")
                GPIO.output(UV_pin, GPIO.HIGH)
                GPIO.output(UV_pin1, GPIO.HIGH)
                print('UV TURN ON')
                TIME_UV = 5
                for sec in range(TIME_UV + 1):
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string("UV LIGHT")
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string(f"Remained_Time:{TIME_UV}s")
                    #lcd.write_string('HUM={0:0.2f}s'.format(TIME))
                    TIME_UV -= 1
                    time.sleep(1)
                    lcd.clear()
                lcd.write_string("UV LIGHT OFF")
                GPIO.output(UV_pin, GPIO.LOW)
                GPIO.output(UV_pin1, GPIO.LOW)
                print('UV TURN OFF')
                time.sleep(5)
                lcd.clear()
                GPIO.output(BUZ_pin, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZ_pin, GPIO.LOW)
                lcd.write_string("Ready for next!")
                time.sleep(5)
        
        
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(1)
            
except KeyboardInterrupt:
    GPIO.cleanup()
    print("END")
    lcd.clear()