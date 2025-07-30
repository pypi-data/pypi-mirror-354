import gradio as gr
from gradio_iframecomponent import IFrame

def create_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# IFrame Component Demo")
        
        iframe = IFrame(
            label="Web Page Viewer",
            value="https://www.gradio.app",
            interactive=True,
            height=500
        )
        
        url_input = gr.Textbox(
            label="Enter URL",
            placeholder="https://example.com"
        )
        
        load_btn = gr.Button("Load URL")
        
        load_btn.click(
            fn=lambda url: url,
            inputs=url_input,
            outputs=iframe
        )
    
    return demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
