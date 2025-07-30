
import gradio as gr
from app import demo as app
import os

_docs = {'IFrame': {'description': 'A custom Gradio component for embedding iframes.', 'members': {'__init__': {'value': {'type': 'str', 'default': '""', 'description': None}, 'src': {'type': 'str | None', 'default': 'None', 'description': None}, 'width': {'type': 'str | int', 'default': '"100%"', 'description': None}, 'height': {'type': 'str | int', 'default': '400', 'description': None}, 'sandbox': {'type': 'str | None', 'default': 'None', 'description': None}, 'interactive': {'type': 'bool', 'default': 'True', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool', 'default': 'True', 'description': None}}, 'postprocess': {'value': {'type': 'str | None', 'description': None}}, 'preprocess': {'return': {'type': 'str | None', 'description': None}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the IFrame changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the IFrame.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'IFrame': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_iframecomponent`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

iframe
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_iframecomponent
```

## Usage

```python
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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `IFrame`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["IFrame"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["IFrame"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "IFrame-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          IFrame: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
