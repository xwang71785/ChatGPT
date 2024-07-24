import gradio as gr
import requests
import json
import base64
import os
import random
from http import HTTPStatus
from prompt import instr_narr01, instr_narr02, instr_narr03, instr_narr04, instr_narr05, instr_narr06
from prompt import instr_argu01, instr_argu02, instr_argu03, instr_argu04, instr_argu05, instr_argu06
from apikey import ocr_host, ocr_client_id, ocr_client_secret
from apikey import ernie_host, ernie_client_id, ernie_client_secret

# 获取百度OCR模型的ocr_access_token和请求地址ocr_request_url
ocr_token_url = ocr_host + ocr_client_id + ocr_client_secret
ocr_response = requests.get(ocr_token_url)
ocr_access_token = ocr_response.json().get('access_token')
ocr_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"

# 获取ERNIE-4.0模型的ernie_access_token和请求地址ernie_request_url
url = ernie_host + ernie_client_id + ernie_client_secret
payload = json.dumps("")
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
ernie_access_token = response.json().get("access_token")
ernie_request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"



def baidu_ocr(image_file):
    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())
    # 单字识别返回位置和置信度并检测涂改
    params = {"image": img}

    # access_token = '[调用鉴权接口获取的token]'
    request_url = ocr_request_url + "?access_token=" + ocr_access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    response_data = response.json().get('words_result')
    title = ''
    str_normal = ''
    for chars in response_data:
        str_normal = str_normal + chars['words']
    str_normal = str_normal.replace("☰", "")
    for i in range(3):
        if response_data[i]['location']['left'] > 150:
            title = response_data[i]['words']

    return title, str_normal


def baidu_ernie(instruction, compsition):
    request_url = ernie_request_url + "?access_token=" + ernie_access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": compsition}],
        "temperature": 0.1,
        "top_p": 0.1,
        "system": instruction})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST",
                                request_url,
                                headers=headers,
                                data=payload)
    result = json.loads(response.text)
    cost = result['usage']['total_tokens']
    final_text = result['result']
    return final_text + " Total: " + str(cost) + " token"



    messages = [{'role': 'system', 'content': instruction},
            {'role': 'user', 'content': compsition}]
    
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        result_format='message',)

    if response.status_code == HTTPStatus.OK:
        data = response.output.choices[0].message.content
    return data

# Gradio process fuctions
def process_one(image_file, category):
    if image_file is None:
        return "image is none"
    else:
        title, ocr_result = baidu_ocr(image_file)
        ai_character = baidu_ernie(ocr_result, instr_narr01)
        ai_emotion = baidu_ernie(ocr_result, instr_narr02)
        ai_story = baidu_ernie(ocr_result, instr_narr03)
        ai_language = baidu_ernie(ocr_result, instr_narr04)
        ai_structure = baidu_ernie(ocr_result, instr_narr05)
        ai_revised = baidu_ernie(ocr_result, instr_narr06)
        return ocr_result, ai_character, ai_emotion, ai_story, ai_language, ai_structure, ai_revised


def process_multi(image_file1, image_file2, image_file3, category):
    if image_file2 is None:
        return "image2 is none"
    else:
        title, ocr_result1 = baidu_ocr(image_file1)
        title2, ocr_result2 = baidu_ocr(image_file2)
        if image_file3 is None:
            ocr_result3 = ''
        else:
            title3, ocr_result3 = baidu_ocr(image_file3)
        ocr_result = ocr_result1 + ocr_result2 + ocr_result3
        ai_character = baidu_ernie(ocr_result, instr_argu01)
        ai_emotion = baidu_ernie(ocr_result, instr_argu02)
        ai_story = baidu_ernie(ocr_result, instr_argu03)
        ai_language = baidu_ernie(ocr_result, instr_argu04)
        ai_structure = baidu_ernie(ocr_result, instr_argu05)
        ai_revised = baidu_ernie(ocr_result, instr_argu06)
        return ocr_result, ai_character, ai_emotion, ai_story, ai_language, ai_structure, ai_revised


def get_file_list(folder_path):
    file_list = []
    for filename in os.listdir(folder_path):
        file_name = os.path.join(folder_path, filename)
        if os.path.isfile(file_name):
            file_list.append(file_name)
    return file_list


def process_batch(image_file):
    output_folder = './result'
    if image_file is None:
        return "image is none"
    else:
        for image in image_file:
            last_dot_index = image.rfind('.')
            output_file = image[:last_dot_index] + '_rev.txt'
            output_file = os.path.basename(output_file)
            output_filepath = os.path.join(output_folder, output_file)
            if not os.path.exists(output_filepath):
                ocr_result, ocr_result_normal = baidu_ocr(image)
                ai_result = baidu_ernie(ocr_result_normal)
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(ai_result)
                    print(f'保存文件：{output_filepath}')
            else:
                print(f'{output_filepath} already exists')
        return get_file_list('./result')

# 定义Gradio的用户界面
one_page = gr.Interface(fn=process_one,
                        inputs=[gr.Image(type='filepath',label='上传JPG'),
                                gr.Radio(label="文体", choices=[("记叙文","narr"),("议论文","argu")], value="narr"),
                                ],
                        outputs=[gr.Text(label="光学识别"),
                                gr.Text(label='人物刻画'),
                                gr.Text(label='情感描写'),
                                gr.Text(label='故事叙述'),
                                gr.Text(label='语言表达'),
                                gr.Text(label='文章结构'),
                                gr.Text(label="AI 改写")],
                        title="中学作文智能批改",
                        description="Demo Version 0.3.3")

two_pages = gr.Interface(fn=process_multi,
                        inputs=[gr.Image(type='filepath', label='上传第一页JPG'),
                                gr.Image(type='filepath', label='上传第二页JPG'),
                                gr.Image(type='filepath', label='上传第三页JPG'),
                                gr.Radio(label="文体", choices=[("记叙文","narr"),("议论文","argu")], value="narr"),
                                ],
                        outputs=[gr.Text(label="光学识别"),
                                gr.Text(label='逻辑结构'),
                                gr.Text(label='举例论证'),
                                gr.Text(label='结论提炼'),
                                gr.Text(label='段落衔接'),
                                gr.Text(label='语言表达'),
                                gr.Text(label="AI 改写")],
                        title="中学作文智能批改",
                        description="Demo Version 0.3.3")

batch_files = gr.Interface(fn=process_batch,
                            inputs=[gr.File(label="请上传jpg图片", file_count="multiple"),
                                    #gr.Radio(label="文体", choices=["Narration","Argumentation"], value="Narration"),
                                    #gr.Radio(label="模型", choices=["Baidu","Ali","Kimi"], value="Baidu")
                                    ],
                            outputs=gr.File(label="请保存批改结果", file_count="directory"),
                            title="中学语文作文批改系统",
                            description="因多次调用远程大模型需要花费较多时间,请耐心等待!"
)

demo = gr.TabbedInterface([one_page, two_pages, batch_files], ['单页上传', '多页上传', '批量上传'])

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0',
                auth=[('username', 'password'),
                    ('guest', 'abcd123')])
