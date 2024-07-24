import gradio as gr
import requests
import json
import base64
import os

# 选择百度OCR模型转换作文图像jpg为文字
# 获取百度OCR模型的access_token
ocr_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'
ocr_client_id = 'client_id=E4DzdB21UtGEHHfKxbNY1ryE&'
ocr_client_secret = 'client_secret=CFbRJtFAIX6pIqp9Fm0XWP1HUxaZfX7O'
ocr_token_url = ocr_host + ocr_client_id + ocr_client_secret
ocr_response = requests.get(ocr_token_url)
ocr_access_token = ocr_response.json().get('access_token')
ocr_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

# 选择百度文心一言ERNIE-4.0模型对作文进行批改
# 获取ERNIE-4.0模型的access_token
ernie_host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&"
ernie_client_id = "client_id=MX1je75AatCUHojoZhkpfwaG&"
ernie_client_secret = "client_secret=Nh14ZkLhpZldCmQsXsxI4zQ4q6oxGAhq"
url = ernie_host + ernie_client_id + ernie_client_secret
    
payload = json.dumps("")
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
    
response = requests.request("POST", url, headers=headers, data=payload)
ernie_access_token = response.json().get("access_token")
ernie_request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"

def baidu_ocr(image):
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    # img = base64.b64encode(image)
    params = {"image":img}
    request_url = ocr_request_url + "?access_token=" + ocr_access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    str = ''
    if response:
        data = response.json().get('words_result')
        print(data)
        for element in data:
            str = str + element['words']
    return str


def AI_answer(input):
    instructions = '作为一名中学语文老师请对下面的这篇中学生作文打分,以100分为满分;并指出语句不够通顺,用词不够托贴的地方,为学生改写: '
    contents = instructions + input
    request_url = ernie_request_url + "?access_token=" + ernie_access_token
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": contents
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", request_url, headers=headers, data=payload)
    result = json.loads(response.text)
    ai_result = result['result']
    
    return ai_result


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



def process_data(image):
    if image is None:
        return "image is none", "image is none", get_file_list('./data')
    else:
        ocr_result = baidu_ocr(image)
        ai_result = AI_answer(ocr_result)
        return ocr_result, ai_result

demo = gr.Interface(
    fn=process_data,
    inputs=[gr.File(label="上传图片", file_count="multiple")],
    outputs=[gr.Text(label="OCR"), gr.Text(label="AI批改"), gr.File(label="保存图片", file_count="directory")],
)


if __name__ == "__main__":
    demo.launch()