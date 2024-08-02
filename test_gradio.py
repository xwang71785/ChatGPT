# Gradio多种页面布局样例

css = """
.textinput textarea {color: red; font-size: 20px; border: inset}
.textoutput {box: 5px 5px 5px #888888;}
.btn-primary {border: groove;}

footer.svelte-laxltoq {display: none;}
"""

import gradio as gr
strings = 'sdfsagrehtroohf'
def greet(name):
    return "Hello, " + name + "!" 


def get_param(request: gr.Request):
    param1 = request.username
    return param1

with gr.Blocks(css=css) as demo:
    # 基于Markdown建立格式化文本    
    username = gr.State(strings)    # 创建一个State变量，用于存放username
    gr.Markdown(
    """
    # Hello World!
    Start typing below to see the output.
    """)
    gr.Markdown(f"hello {username}!")
    # 基于Column,Row和Tab建立布局
    with gr.Tab("Flip Image"):
        with gr.Row(variant="panel"):
            file_list2 = gr.Image(type='filepath', label='上传第一页JPG'),
            with gr.Column():
                img1 = gr.Image("llama3.png")
                img2 = gr.Image("llama3.png")
                file_list1 = gr.File(label="请上传jpg图片", file_count="multiple")
            with gr.Column():
                text2 = gr.Textbox(label="prompt 2",)   
                btn = gr.Button("Go", size="sm")
                file_list3 = gr.File(label="请保存批改结果", file_count="directory")
    with gr.Tab("Flip Text"):
        img1 = gr.Image(label="image 1", type="filepath")
        file_list2 = gr.File(label="file list 2", file_count="multiple", file_types=[".txt"])
        drop3 = gr.Dropdown(choices=["a", "b", "c"], label="d3")
        
        with gr.Row():
            with gr.Column():
                audio1 = gr.Audio(label="audio 1")
                text2 = gr.Textbox(label="prompt 2", elem_classes="textinput")
                inbtw = gr.Button("Between")
                text4 = gr.Textbox(label="prompt 1")
                text5 = gr.Textbox(label="prompt 2")
            with gr.Column():
                img1 = gr.Image("llama3.png")
                btn = gr.Button("Go", size="sm", elem_classes="btn-primary")
                radio = gr.Radio(choices=[("记叙文","Narration"),("议论文","Argumentation")], 
                                label="文体", value="Narration")
                btn.click(fn=greet, inputs=radio, outputs=img1)
            with gr.Column():
    #            name = gr.Textbox(label="Name")
            # 不可交互
            # output = gr.Textbox(label="Output Box")
            # 可交互
                output = gr.Textbox(label="Output", interactive=True, elem_classes="textoutput")
                greet_btn = gr.Button("Greet")
                greet_btn.click(fn=greet, inputs=username, outputs=output)
    
    #启动demo时调用get_param函数，将Request中的用户名赋值给username
    demo.load(get_param, None, username, queue=False)


if __name__ == "__main__":
# 本地运行gradio监听来自所有IP的访问
    demo.launch(server_name='0.0.0.0', auth=[('username', 'password'), 
                                            ('username2', 'password2'), 
                                            ('arnold', 'arnold')])
    # demo.launch(share=True)    # 分享到gradio官网
