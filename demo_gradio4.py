# 可选择的模型：Kimi大模型（https://huggingface.co/kimiyou/llama-7b-hf）、
# 阿里千问大模型（https://huggingface.co/aliyun/ernie-3.0-medium-zh）
# 百度OCR模型（https://ai.baidu.com/)
# 百度文心一言模型（https://ai.baidu.com/)

import gradio as gr
from openai import OpenAI    # Kimi大模型调用
import dashscope    # 阿里千问大模型
import requests
import json
import base64
import os
import random
from http import HTTPStatus
from prompt import instr_narr01, instr_narr02, instr_narr03, instr_narr04, instr_narr05, instr_narr06
from prompt import instr_argu01, instr_argu02, instr_argu03, instr_argu04, instr_argu05, instr_argu06

auth_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'
ocr_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
ernie_request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="

# 获取百度OCR模型的ocr_access_token
ocr_token_url = auth_host + os.getenv('ocr_client_id') + os.getenv('ocr_client_secret')
ocr_response = requests.get(ocr_token_url)
ocr_access_token = ocr_response.json().get('access_token')

# 获取ERNIE-4.0模型的ernie_access_token
url = auth_host + os.getenv('ernie_client_id') + os.getenv('ernie_client_secret')
payload = json.dumps("")
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)
ernie_access_token = response.json().get("access_token")


def baidu_ocr(image_file):
    # 二进制方式打开图片文件
    f = open(image_file, 'rb')
    img = base64.b64encode(f.read())
    # 行识别返回位置和置信度并检测涂改
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
    for i in range(3):    # 检查头三行的起首位置来判定是否为标题
        if response_data[i]['location']['left'] > 150:
            title = response_data[i]['words']

    return title, str_normal


def baidu_ernie(instruction, compsition):
    request_url = ernie_request_url + "?access_token=" + ernie_access_token
    payload = json.dumps({
        "messages": [
            {"role": "user",
            "content": compsition}],
        "temperature": 0.1,
        "top_p": 0.1,
        "system": instruction})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", request_url, headers=headers, data=payload)
    result = json.loads(response.text)
    cost = result['usage']['total_tokens']
    final_text = result['result']
    return final_text + " Total: " + str(cost) + " token"


# Kimi
client = OpenAI(
    api_key= os.getenv('kimi_api_key'),
    base_url="https://api.moonshot.cn/v1",
)

def kimi_gpt(instruction, compsition):
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": compsition}
            ],
        temperature=0.2)

    data = completion.choices[0].message.content
    return data

# Ali千问，需安装dashscope SDK
dashscope.api_key = os.getenv('ali_api_key')

def ali_qwen(instruction, compsition):
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
def process_ocr01(image01, image02):
    if image01 is None:
        return "image is none", "请上传图片"
    else:
        title1, ocr_result1 = baidu_ocr(image01)
        if image02 is None:
            ocr_result2 = ''
        else:
            title2, ocr_result2 = baidu_ocr(image02)
        ocr_result = ocr_result1 + " " + ocr_result2
        return title1, ocr_result

def process_ocr11(image01, image02, image03):
    if image01 is None:
        return "image is none", "请上传图片"
    else:
        title1, ocr_result = baidu_ocr(image01)
        if image02 is None:
            ocr_result2 = ''
        else:
            title2, ocr_result2 = baidu_ocr(image02)
        if image03 is None:
            ocr_result3 = ''
        else:
            title3, ocr_result3 = baidu_ocr(image03)
        ocr_result = ocr_result + " " + ocr_result2 + " " + ocr_result3
        return title1, ocr_result

def process_revice(instr, text):
    if text is None:
        return "text is none"
    else:
        ai_revised = baidu_ernie(text, instr)
        return ai_revised

def get_file_list(folder_path):
    file_list = []
    for filename in os.listdir(folder_path):
        file_name = os.path.join(folder_path, filename)
        if os.path.isfile(file_name):
            file_list.append(file_name)
    return file_list

def process_batch(image_file, genres, model):
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
                title, ocr_result = baidu_ocr(image)
                ai_result = baidu_ernie(instr_narr06, ocr_result)
                with open(output_filepath, 'w', encoding='utf-8') as output_file:
                    output_file.write(ai_result)
                    print(f'保存文件：{output_filepath}')
            else:
                print(f'{output_filepath} already exists')
        return get_file_list('./result')

# 定义Gradio的用户界面
with gr.Blocks() as demo:
    gr.Markdown(
    """
    # 中学作文批改系统
    测试版本0.5.3
    ### 允许拍照上传，请尽力保持纸张平整，不留边框，字迹清晰，
    """)
    with gr.Tab("记叙文批改"):
        with gr.Row():
            with gr.Column():
                img01 = gr.Image(type='filepath', label='上传第一页JPG')
                img02 = gr.Image(type='filepath', label='上传第二页JPG')
                btn00 = gr.Button("上传", size="sm")
                title01 = gr.Text(label="作文标题")
                text00 = gr.Text(label="光学识别")
                btn06 = gr.Button("改写", size="sm")
                state06 = gr.State(instr_narr06)    # 利用state向界面函数传递参数
                text06 = gr.Text(label="AI 改写")
                btn00.click(fn=process_ocr01, inputs=[img01, img02], outputs=[title01, text00])
                btn06.click(fn=process_revice, inputs=[state06,text00], outputs=[text06])
            with gr.Column():
                with gr.Row():
                    btn01 = gr.Button("人物", size="sm")
                    btn02 = gr.Button("情感", size="sm")
                    state01 = gr.State(instr_narr01)
                    state02 = gr.State(instr_narr02)
                text01 = gr.Text(label='人物刻画')
                text02 = gr.Text(label='情感描写')
                with gr.Row():
                    btn03 = gr.Button("故事", size="sm")
                    btn04 = gr.Button("语言", size="sm")
                    btn05 = gr.Button("结构", size="sm")
                    state03 = gr.State(instr_narr03)
                    state04 = gr.State(instr_narr04)
                    state05 = gr.State(instr_narr05)
                text03 = gr.Text(label='故事叙述')
                text04 = gr.Text(label='语言表达')
                text05 = gr.Text(label='文章结构')
                btn01.click(fn=process_revice, inputs=[state01,text00], outputs=[text01])
                btn02.click(fn=process_revice, inputs=[state02,text00], outputs=[text02])
                btn03.click(fn=process_revice, inputs=[state03,text00], outputs=[text03])
                btn04.click(fn=process_revice, inputs=[state04,text00], outputs=[text04])
                btn05.click(fn=process_revice, inputs=[state05,text00], outputs=[text05])
    with gr.Tab("议论文批改"):
        with gr.Row():
            with gr.Column():
                img11 = gr.Image(type='filepath', label='上传第一页JPG')
                img12 = gr.Image(type='filepath', label='上传第二页JPG')
                img13 = gr.Image(type='filepath', label='上传第二页JPG')
                btn10 = gr.Button("上传", size="sm")
                title11 = gr.Text(label="作文标题")
                text10 = gr.Text(label="光学识别")
                btn16 = gr.Button("改写", size="sm")
                state16 = gr.State(instr_argu06)
                text16 = gr.Text(label="AI 改写")
                btn10.click(fn=process_ocr11, inputs=[img11, img12,img13], outputs=[title11, text10])
                btn16.click(fn=process_revice, inputs=[state16,text10], outputs=[text16])
            with gr.Column():
                with gr.Row():
                    btn11 = gr.Button("逻辑", size="sm")
                    btn12 = gr.Button("论证", size="sm")
                    state11 = gr.State(instr_argu01)
                    state12 = gr.State(instr_argu02)
                text11 = gr.Text(label='逻辑结构')
                text12 = gr.Text(label='举例论证')
                with gr.Row():
                    btn13 = gr.Button("结论", size="sm")
                    btn14 = gr.Button("结构", size="sm")
                    btn15 = gr.Button("语言", size="sm")
                    state13 = gr.State(instr_argu03)
                    state14 = gr.State(instr_argu04)
                    state15 = gr.State(instr_argu05)
                text13 = gr.Text(label='结论提炼')
                text14 = gr.Text(label='段落衔接')
                text15 = gr.Text(label='语言表达')
                btn11.click(fn=process_revice, inputs=[state11, text10], outputs=[text11])
                btn12.click(fn=process_revice, inputs=[state12, text10], outputs=[text12])
                btn13.click(fn=process_revice, inputs=[state13, text10], outputs=[text13])
                btn14.click(fn=process_revice, inputs=[state14, text10], outputs=[text14])
                btn15.click(fn=process_revice, inputs=[state15, text10], outputs=[text15])
    with gr.Tab("批量作文改写"):
        file_list01 = gr.File(label="请上传jpg图片", file_count="multiple")
        choice01 = gr.Radio(label="文体", choices=[("记叙文","Narr"),("议论文","Argu")], value="Narr")
        choice02 = gr.Radio(label="模型", choices=["Baidu","Ali","Kimi"], value="Baidu")
        btn20 = gr.Button("上传", size="sm")
        file_list02 = gr.File(label="请保存批改结果", file_count="directory")
        btn20.click(fn=process_batch, inputs=[file_list01,choice01,choice02], outputs=file_list02)


if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0',
                auth=[('username', 'password'),
                    ('guest', 'abcd123')])
