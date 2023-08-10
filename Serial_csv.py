import serial
import csv
import time
import os

ser = serial.Serial('COM3', 115200)

data_folder = 'C:/dev/data'
os.makedirs(data_folder, exist_ok=True)

def generate_csv_file_path():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(data_folder, f'data_{timestamp}.csv')

csv_file_path = generate_csv_file_path()
csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)

# 제목 행 저장
csv_writer.writerow(["x", "y", "range", "angle", "vel_l", "vel_a", "rpm_l", "rpm_r"])
csv_file.flush()

save_data = True

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('ascii').strip()

            if 'T' in data:
                if save_data:
                    csv_file.close()
                    print("CSV 파일 저장 및 닫힘.")
                    save_data = False
            elif 'N' in data:
                if not save_data:
                    csv_file.close()
                    print("CSV 파일 닫힘.")
                    csv_file_path = generate_csv_file_path()
                    csv_file = open(csv_file_path, 'w', newline='')
                    csv_writer = csv.writer(csv_file)
                    # 제목 행 저장
                    csv_writer.writerow(["x", "y", "range", "angle", "vel_l", "vel_a", "rpm_l", "rpm_r"])
                    csv_file.flush()
                    print("CSV 파일 새로 생성됨.")
                    save_data = True
            else:
                if save_data:
                    # 데이터 분리 및 저장
                    data_list = data.split(' ')  # 데이터를 띄어쓰기로 분리
                    x, y, range_val, angle, vel_l, vel_a, rpm_l, rpm_r = data_list
                    
                    # 데이터 순서대로 저장
                    csv_writer.writerow([x, y, range_val, angle, vel_l, vel_a, rpm_l, rpm_r])
                    csv_file.flush()
                    print(data)
        
except KeyboardInterrupt:
    print("키보드 인터럽트 감지됨. 프로그램 종료됨.")
finally:
    csv_file.close()
    ser.close()
