import os
import socket
import threading
import time
from configparser import ConfigParser
import json
import ssl
import pandas as pd
import matplotlib.pyplot as plt

import api
import timeseriesdb as tsdb
from logger import Logger as log
import config

class TCPClient:
    def __init__(self, host, port, its, server_cert):
        self.host = host
        self.port = port
        self.its = its
        self.user = None
        self.password = None
        self.client_socket = None
        self.connected = False
        self.result = False  # 로그인 성공 여부 플래그
        self.response = None
        self.msg = None
        self.server_cert = server_cert

    def set_user_password(self, user, password):
        self.user = user
        self.password = password

        return

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.server_cert)

        try:
            wrapped_socket = context.wrap_socket(self.client_socket, server_hostname=self.host)
            wrapped_socket.connect((self.host, self.port))
            self.client_socket = wrapped_socket
            self.connected = True
            print(f"Connected to {self.host}:{self.port} with SSL/TLS")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False
        '''
    def receive_messages(self):
        incomplete_data = ""  # 누적된 데이터를 저장할 변수

        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue

            try:
                while self.connected:
                    response = self.client_socket.recv(81920).decode()
                    if not response:
                        break

                    # 누적된 데이터에 새로 받은 데이터를 추가
                    incomplete_data += response

                    while True:
                        try:
                            # 누적된 데이터를 JSON으로 변환
                            response_dict = json.loads(incomplete_data)
                            
                            # JSON 변환에 성공하면 누적된 데이터를 비우고 처리
                            incomplete_data = ""

                            if 'data' in response_dict:
                                response_dict['data'] = json.loads(response_dict['data'])
                            self.message_parser(response_dict)

                        except json.JSONDecodeError:
                            # JSON 변환에 실패하면 더 많은 데이터가 필요하므로 루프를 벗어남
                            break

            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()
    '''
    def receive_messages(self):
        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue
            try:
                while self.connected:
                    response = self.client_socket.recv(4096).decode()
                    if not response:
                        break
                    # log.info(f"Received: {response}")
                    try:
                        response_dict = json.loads(response)
                        if 'data' in response_dict:
                            response_dict['data'] = json.loads(response_dict['data'])
                        self.message_parser(response_dict)
                    except json.JSONDecodeError:
                        log.error("Failed to decode JSON response")
            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()
    '''
    def send_message(self, message):
        if not self.connected:
            return
        try:
            self.client_socket.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def message(self, command, projectid = None, structureid = None):
        if command.lower() == 'login':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }
        elif command.lower() == 'get_project_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }

        elif command.lower() == 'get_structure_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid
            }
        
        elif command.lower() == 'get_device_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid,
                "structureid": structureid
            }

        elif command.lower() == 'get_project_structure_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }
        
        elif command.lower() == 'download_sensordata':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid,
                "structureid": structureid
            }

        else:
            response = {}
            response['result'] = 'Fail'
            response['msg'] = 'not defined command'
            return response

        # elif command.lower() == 'download_sensordata':
        #     message = {
        #         "command": command,
        #         "its": self.its,
        #         "user": self.user,
        #         "password": self.password,
        #         "projectid": projectid,
        #         "structureid": structureid
        #     }

        send_message = json.dumps(message)

        try:
            response = self.send_and_wait_for_response(send_message)
            return response
        except socket.error as e:
            print(f"Error sending data: {e}")
            response = {}
            response['result'] = 'Fail'
            response['msg'] = str(e)
            return
        
    def message_getdata(self, command, start_date, end_date, projectid=None, structureid=None, deviceid=None, channel=None):
        if command.lower() not in ['download_sensordata', 'download_sensordata_as_df', 'query_device_channel_data']:
            raise ValueError(f"Unsupported command: {command}")

        if command.lower() == 'query_device_channel_data':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "deviceid": deviceid,
                "channel": channel
            }

            send_message = json.dumps(message)

            try:
                response = self.send_and_wait_for_response(send_message)

                if response['result'] != 'Success':
                    print(f"Download Failed({response['msg']})")
                    return pd.DataFrame() if command == 'download_sensordata_as_df' else response

                # ✅ 1. 서버 응답 'data' 는 이미 dict(list) → DataFrame으로 변환
                df_info = pd.DataFrame(response['data'])

                # ✅ 2. 단일 센서만 오므로 첫 행만 처리
                row = df_info.iloc[0]
                d_id = row['deviceid']
                ch = row['channel']
                d_type = row['d_type']
                data_type = row['data_type']
                is3axis = row['is3axis']

                dbinfo = response['dbinfo']
                tsdb.tsdb_init(
                    dbinfo['host'], dbinfo['port'], dbinfo['token'], dbinfo['org'], dbinfo['bucket']
                )

                # start_date_str = str(start_date) + " 000000"
                # end_date_str = str(end_date) + " 235959"
                # formatted_start_date, formatted_end_date = api.date_formatted(start_date_str, end_date_str)
                formatted_start_date, formatted_end_date = api.date_formatted_flexible(start_date, end_date)


                df = tsdb.query_data(d_id, ch, formatted_start_date, formatted_end_date, d_type, sample_count=1)
                if df.empty:
                    print("No sensor data.")
                    return pd.DataFrame()

                df['device_id'] = d_id
                df['channel'] = ch
                df['d_type'] = d_type

                tsdb.tsdb_disconnect()

                return df

            except socket.error as e:
                print(f"Error sending data: {e}")
                tsdb.tsdb_disconnect()
                return pd.DataFrame() if command == 'download_sensordata_as_df' else {'result': 'Fail', 'msg': str(e)}

        else:
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid,
                "structureid": structureid
            }

            send_message = json.dumps(message)

            try:
                response = self.send_and_wait_for_response(send_message)

                if response['result'] != 'Success':
                    print(f"Download Failed({response['msg']})")
                    return pd.DataFrame() if command == 'download_sensordata_as_df' else response

                data = response['data']
                host = response['dbinfo']['host']
                port = response['dbinfo']['port']
                token = response['dbinfo']['token']
                org = response['dbinfo']['org']
                bucket = response['dbinfo']['bucket']

                tsdb.tsdb_init(host, port, token, org, bucket)

                df = pd.DataFrame(data)
                if df.empty:
                    print("No sensor info returned.")
                    return pd.DataFrame() if command == 'download_sensordata_as_df' else response

                # start_date_str = str(start_date) + " 000000"
                # end_date_str = str(end_date) + " 235959"
                # formatted_start_date, formatted_end_date = api.date_formatted(start_date_str, end_date_str)
                formatted_start_date, formatted_end_date = api.date_formatted_flexible(start_date, end_date)

                df.reset_index(drop=True, inplace=True)

                all_sensor_data = []
                df_failures = pd.DataFrame(columns=['device_id', 'channel'])
                Success_Count = 0
                Fail_Count = 0

                for index, row in df.iterrows():
                    try:
                        print(f"Querying sensor data : {index + 1} / {df.shape[0]}")
                        print(f"Success: {Success_Count} / Fail: {Fail_Count}")
                        d_id, ch, d_type, data_type, is3axis = row

                        sensor_data = tsdb.query_data(d_id, ch, formatted_start_date, formatted_end_date, d_type, sample_count=1)
                        if sensor_data.empty:
                            print(f"Empty Data: {d_id} {ch}")
                            Fail_Count += 1
                            df_failures = api.add_failure(df_failures, str(d_id), str(ch))
                            continue

                        sensor_data['device_id'] = d_id
                        sensor_data['channel'] = ch
                        sensor_data['d_type'] = d_type
                        all_sensor_data.append(sensor_data)
                        Success_Count += 1

                    except Exception as e:
                        log.error(f"Exception occurred: {str(e)}")
                        df_failures = api.add_failure(df_failures, str(d_id), str(ch))
                        Fail_Count += 1
                        continue

                tsdb.tsdb_disconnect()

                if command == 'download_sensordata_as_df':
                    return pd.concat(all_sensor_data, ignore_index=True) if all_sensor_data else pd.DataFrame()

                # ───── CSV 저장 + Plot 처리
                dir_path = config.DATA_DIR
                if dir_path[-1] != '/':
                    dir_path += '/'
                if projectid and structureid:
                    dir_path += f"{projectid}/{structureid}/"
                elif structureid:
                    dir_path += f"{structureid}/"
                elif projectid:
                    dir_path += f"{projectid}/"
                else:
                    response = {'result': 'Fail', 'msg': 'input projectid or structureid'}
                    return response

                os.makedirs(dir_path, exist_ok=True)

                for sensor_data in all_sensor_data:
                    d_id = sensor_data['device_id'].values[0]
                    ch = sensor_data['channel'].values[0]
                    d_type = sensor_data['d_type'].values[0]

                    if d_type in ['1', '3']:
                        save_cols = ['time', 'anal1', 'anal2']
                    else:
                        save_cols = ['time', 'humidity', 'sv', 'temperature']


                    filename = f"{dir_path}{d_id}_{ch}.csv"
                    # sensor_data.to_csv(filename, index=False)
                    sensor_data.to_csv(filename, encoding='utf-8-sig', index=False,
                    columns=[c for c in save_cols if c in sensor_data.columns])

                    # Plot 생성
                    fig, ax = plt.subplots(figsize=(15, 10))
                    d_type = sensor_data['d_type'].values[0]
                    try:
                        if d_type == '1' or d_type == '3':
                            ax.plot(sensor_data['time'], sensor_data['anal1'], label=f"{d_id} ch{ch} anal1")
                            ax.plot(sensor_data['time'], sensor_data['anal2'], label=f"{d_id} ch{ch} anal2")
                        else:
                            ax.plot(sensor_data['time'], sensor_data['sv'], label=f"{d_id} ch{ch} sv")

                        ax.set_title(f'Sensor Data for Device {d_id} Channel {ch}')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Value')
                        ax.legend()
                        ax.grid(True)

                        plt.savefig(f'{dir_path}sensor_{d_id}_{ch}.png')
                        plt.close()
                    except KeyError as e:
                        log.error(f"KeyError: {str(e)} - for Device {d_id} Channel {ch}")

                # 실패 로그 저장
                failure_filename = dir_path + 'failures.csv'
                df_failures.to_csv(failure_filename, index=False)

                # device_info 저장
                if 'device_info' in response:
                    device_info = response['device_info']
                    df_device_info = pd.DataFrame(json.loads(device_info))
                    df_device_info.to_csv(f'{dir_path}device_info.csv', index=False)

                return response

            except socket.error as e:
                print(f"Error sending data: {e}")
                tsdb.tsdb_disconnect()
                return pd.DataFrame() if command == 'download_sensordata_as_df' else {'result': 'Fail', 'msg': str(e)}

    def login(self):
        # if not self.connected:
        #     print("Server is not connected")
        #     return
        
        message = {
            "command": "login",
            "its": self.its,
            "user": self.user,
            "password": self.password
        }

        send_message = json.dumps(message)

        try:
            response = self.send_and_wait_for_response(send_message)
            return response
        except socket.error as e:
            print(f"Error sending data: {e}")

    def disconnect(self):
        self.client_socket.close()
        self.connected = False
        print("Connection closed.")

    def get_connect_status(self):
        return self.connected

    def get_login_status(self):
        return self.result
    
    def get_error_message(self):
        return self.msg
    
    def message_parser(self, response_dict):

        if response_dict.get("result") == "Success":
            self.result = True
        else:
            self.result = False
            
        self.response = response_dict

    def send_and_wait_for_response(self, message):
        self.response = None  # 이전 응답 초기화
        self.send_message(message)
        # 응답 대기
        while self.response is None:
            time.sleep(0.1)
        return self.response


'''
import socket
import threading
import time
from configparser import ConfigParser
import json

from logger import Logger as log

class TCPClient:
    def __init__(self, host, port, its, user, password):
        self.host = host
        self.port = port
        self.its = its
        self.user = user
        self.password = password
        self.client_socket = None
        self.connected = False

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False

    def receive_messages(self):
        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue
            try:
                while self.connected:
                    response = self.client_socket.recv(1024).decode()
                    if not response:
                        break
                    log.info(f"Received: {response}")
                    response_dict = json.loads(response)
                    message_parser(response_dict)
            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()

    def send_message(self, message):
        if not self.connected:
            return
        try:
            self.client_socket.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def login(self):
        if not self.connected:
            print("Server is not connected")
            return
        
        message = {
            "command" : "login",
            "its" : self.its,
            "user" : self.user,
            "password" : self.password
        }

        send_message = json.dumps(message)

        try:
            self.send_message(send_message)
        except socket.error as e:
            print(f"Error sending data: {e}")

    def disconnect(self):
        self.client_socket.close()
        self.connected = False
        print("Connection closed.")

    def get_connect_status(self):
        return self.connected
    
def message_parser(response_dict):

    print(response_dict)
'''