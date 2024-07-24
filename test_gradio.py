# Gradio多种页面布局样例

import gradio as gr
strings = 'sdfsagrehtrhf'
def greet(name):
    return "Hello, " + name + "!" 


def get_param(request: gr.Request):
    param1 = request.username
    return param1

with gr.Blocks() as demo:
    # 基于Markdown建立格式化文本    
    ui_param1 = gr.State(strings)
    gr.Markdown(
    """
    # Hello World!
    Start typing below to see the output.
    """)
    gr.Markdown(f"hello {ui_param1}!")
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
                text2 = gr.Textbox(label="prompt 2")
                inbtw = gr.Button("Between")
                text4 = gr.Textbox(label="prompt 1")
                text5 = gr.Textbox(label="prompt 2")
            with gr.Column():
                img1 = gr.Image("llama3.png")
                btn = gr.Button("Go", size="sm")
                radio = gr.Radio(choices=[("记叙文","Narration"),("议论文","Argumentation")], 
                                label="文体", value="Narration")
                btn.click(fn=greet, inputs=radio, outputs=img1)
            with gr.Column():
    #            name = gr.Textbox(label="Name")
            # 不可交互
            # output = gr.Textbox(label="Output Box")
            # 可交互
                output = gr.Textbox(label="Output", interactive=True)
                greet_btn = gr.Button("Greet")
                greet_btn.click(fn=greet, inputs=ui_param1, outputs=output)
    
    demo.load(get_param, None, ui_param1, queue=False)


if __name__ == "__main__":
# 本地运行gradio监听来自所有IP的访问
    demo.launch(server_name='0.0.0.0', auth=[('username', 'password'), ('username2', 'password2')])
    # demo.launch(share=True)    # 分享到gradio官网
