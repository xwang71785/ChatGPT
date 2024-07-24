# 运行与后台服务器端,读取上传来的jpg文件,转发到百度OCR模型和ERNIE-4.0模型进行文本识别和批改,
# 返回识别结果和批改结果,并调用文件上传接口上传批改结果
import requests
import urllib.parse     
import json
import base64
import hashlib
import os
import datetime

from prompt import instruction_ocr, message_ocr
from prompt import instruction_revise, message_revise
from apikey import auth_host, ocr_client_id, ocr_client_secret
from apikey import api_host, ernie_client_id, ernie_client_secret
from apikey import ernie_40_interface, ernie_40_0329_interface

# 获取百度OCR模型的ocr_access_token和请求地址ocr_request_url
ocr_token_url = auth_host + ocr_client_id + ocr_client_secret
ocr_response = requests.get(ocr_token_url)
ocr_access_token = ocr_response.json().get('access_token')
ocr_request_url = api_host + "rest/2.0/ocr/v1/handwriting"

# 获取ERNIE-4.0模型的ernie_access_token和请求地址ernie_request_url
url = auth_host + ernie_client_id + ernie_client_secret
payload = json.dumps("")
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
ernie_access_token = response.json().get("access_token")
ernie_request_url = api_host + ernie_40_interface


def sign_data(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    signature = sha256.hexdigest()
    return signature


def baidu_ocr(image):
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    f.close()
    print('read image success')
    params = {"image":img}
    request_url = ocr_request_url + "?access_token=" + ocr_access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    print('OCR success')
    return response


def baidu_ocr_hq(image_file):
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())
    # 单字识别返回位置和置信度并检测涂改
    params = {"image": img,
                "recognize_granularity": "small",
                "detect_alteration": "true"}
    # access_token = '[调用鉴权接口获取的token]'
    request_url = ocr_request_url + "?access_token=" + ocr_access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    response_data = response.json().get('words_result')
    str = ''
    for chars in response_data:
        for char in chars['chars']:
            str = str + char['candidates'][0]['word']
            if char['candidates'][0]['prob'] < 0.90:
                str = str + "(" + char['candidates'][1]['word'] + ")"
    return str


def baidu_ernie(input, instruction, prompt):
    contents = instruction + input
    request_url = ernie_request_url + "?access_token=" + ernie_access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": contents}],
        "temperature": 0.1,
        "top_p": 0.1,
        "system": prompt})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST",
                                request_url,
                                headers=headers,
                                data=payload)
    result = json.loads(response.text)
    cost = result['usage']['total_tokens']
    final_text = result['result']
    print('ERNIE success')
    return final_text + " Total: " + str(cost) + " token"


# 处理单个文件的任务
def process_file(input_filepath, student_id):
    response = baidu_ocr(input_filepath)
    ocr_text = ''
    for line in response.json().get('words_result'):
        ocr_text += line['words']

    revised_text = baidu_ernie(ocr_text, instruction_revise, message_revise)
    revised_digest = urllib.parse.quote(revised_text)    # encodeURIComponent
    student_id = str(student_id)
    current_time = datetime.datetime.now()
    #formatted_date = current_time.strftime("%y%m%d")
    timestamp_msec = current_time.timestamp() * 1000
    timestamp_msec = str(int(timestamp_msec))
    salt = "pqcn240430mark"
    data = "cnResult=" + revised_digest + "&timestamp=" + timestamp_msec + "&uniCode=" + student_id + salt
    signature = sign_data(data)

    url = 'https://www.shszedu.com/webinterface/back/mark/cn/text/result'
    headers = {'Content-Type': 'application/json'}
    body = {"cnResult":revised_text, 
        "timestamp":timestamp_msec,
        "uniCode":student_id,
        "sign":signature}
    body = json.dumps(body)

    response =requests.post(url=url, data=body, headers=headers)
    print(student_id)
    print(response)

    # with open(output_filepath, 'w', encoding='utf-8') as output_file:
    #    output_file.write(revised_text)


# 主函数，用于创建并执行任务
def main():
    input_folder = './data/'
    output_folder = './result/'

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_filepath = os.path.join(input_folder, filename)
        last_dot_index = filename.rfind('.')
        student_id = filename[:last_dot_index]
        process_file(input_filepath, student_id)
        


if __name__ == "__main__":
    main()
