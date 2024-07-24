import gradio as gr
import requests
import json
import base64
import os
import random
from http import HTTPStatus
import dashscope

from prompt import instruction_ocr, message_ocr
from prompt import instruction_revise, message_revise, ali_revise
from apikey import auth_host, ocr_client_id, ocr_client_secret
from apikey import api_host, ernie_client_id, ernie_client_secret
from apikey import ernie_40_interface
from apikey import ali_api_key


# 选择百度OCR模型转换作文图像jpg为文字
# 获取百度OCR模型的access_token
ocr_token_url = auth_host + ocr_client_id + ocr_client_secret
ocr_response = requests.get(ocr_token_url)
ocr_access_token = ocr_response.json().get('access_token')
# ocr_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
ocr_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"

# 选择百度文心一言ERNIE-4.0模型对作文进行批改
# 获取ERNIE-4.0模型的access_token
url = auth_host + ernie_client_id + ernie_client_secret
payload = json.dumps("")
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
ernie_access_token = response.json().get("access_token")
ernie_request_url = api_host + ernie_40_interface

output_folder = './result/'

def baidu_ocr(image):
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    f.close()
    print('read image success')
    params = {"image":img,
            "recognize_granularity":"small",
            "detect_alteration":"true"}
    request_url = ocr_request_url + "?access_token=" + ocr_access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    print('OCR success')
    str_normal = ''
    str_hq = ''
    if response:
        response_data = response.json().get('words_result')
        # print(response_data)
        for element in response_data:
            str_normal = str_normal + element['words']
            for char in element['chars']:
                str_hq = str_hq + char['candidates'][0]['word']
                if char['candidates'][0]['prob'] < 0.90:
                    str_hq = str_hq + "(" + char['candidates'][1]['word'] + ")"

        str_normal = str_normal.replace("☰", "")
    return str_normal


def baidu_answer(input):
    instructions = instruction_revise
    contents = instructions + input
    request_url = ernie_request_url + "?access_token=" + ernie_access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": contents}],
        "temperature": 0.1,
        "top_p": 0.1,
        "system": message_revise
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", request_url, headers=headers, data=payload)
    result = json.loads(response.text)
    ai_result = result['result']
    print('ERNIE success')
    return ai_result

def ali_answer(input):
    dashscope.api_key=ali_api_key
    messages = [{'role': 'system', 'content': ali_revise},
            {'role': 'user', 'content': input}]
    response = dashscope.Generation.call(
    "qwen-turbo",
    messages=messages,
    # set the random seed, optional, default to 1234 if not set
    seed=random.randint(1, 10000),
    # set the result to be "message" format.
    result_format='message',)
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content


def get_file_list(folder_path):
    """
    Returns a list of file names in the given folder.
    """
    file_list = []
    for filename in os.listdir(folder_path):
        file_name = os.path.join(folder_path, filename)
        if os.path.isfile(file_name):
            file_list.append(file_name)
    return file_list


def process_data(image_file):
    if image_file is None:
        return "image is none"
    else:
        for image in image_file:
            shutil.copy(image, './data')
        print('复制文件成功')
        for image in get_file_list('./data'):
            last_dot_index = image.rfind('.')
            output_file = image[:last_dot_index] + '_rev.txt'
            output_file = os.path.basename(output_file)
            output_filepath = os.path.join(output_folder, output_file)
            if not os.path.exists(output_filepath):
                ocr_result = baidu_ocr(image)
                ai_result = baidu_answer(ocr_result)
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(ai_result)
                    print(f'保存文件：{output_filepath}')
            else:
                print(f'{output_filepath} already exists')
        print('批改完成')
        return get_file_list('./result')

demo = gr.Interface(
    fn=process_data,
    inputs=gr.File(label="请上传jpg图片", file_count="multiple"), 
    outputs=gr.File(label="请保存批改结果", file_count="directory"),
    
    title="中学语文作文批改系统",
    description="因多次调用远程大模型需要花费较多时间,请耐心等待!",
)


if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0', auth=[('username', 'password'), ('username2', 'password2')])    # 本地运行gradio监听来自所有IP的访问
    # demo.launch(share=True)    # 分享到gradio官网