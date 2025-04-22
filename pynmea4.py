import serial
import pynmea2
import time

port = "/dev/ttyACM0"  # Replace with your serial port
baud = 9600

try:
    serialPort = serial.Serial(port, baudrate=baud, timeout=0.5)
    while True:
        try:
            data = serialPort.readline().decode().strip()
            if data.startswith("$GPGGA"):
                msg = pynmea2.parse(data)
                timestamp = msg.timestamp
                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
                num_sats = msg.num_sats

                log_string = f"{timestamp}, Lat: {latitude:.6f}, Lon: {longitude:.6f}, Alt: {altitude}, Sats: {num_sats}"
                print(log_string)

                # Optional: Log to a file
                with open("gps_log2.txt", "a") as log_file: #change file name to create a differnt file instead of over writing it
                    log_file.write(log_string + "\n")

        except pynmea2.ParseError as e:
            print(f"Parse error: {e}")
        except UnicodeDecodeError as e:
            print(f"Decode error: {e}")
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Serial port error: {e}")
finally:
    if 'serialPort' in locals() and serialPort.is_open:
        serialPort.close()