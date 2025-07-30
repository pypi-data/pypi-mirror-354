
import gradio as gr
from app import demo as app
import os

_docs = {'SimpleTextExtractFromPDF': {'description': "This component extracts text from a PDF file.\nThe extracted text can be submitted as an input {string} to the function.\nOnly the text is extracted. Images are not extracted and table structures are not preserved\nPDF file can be uploaded from user's device or from a URL.\nThis component was designed to be used as an input component.\nAs an output component, it will display {string} content in a textarea.", 'members': {'__init__': {'value': {'type': 'str | None', 'default': 'None', 'description': 'The extracted text from the file. This value is set by the component and can be submitted as an input {string} to the function.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'label': {'type': 'str | I18nData | None', 'default': 'None', 'description': 'the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': "in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render."}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': "A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor."}}, 'postprocess': {'value': {'type': 'str | None', 'description': 'Expects a {string} returned from the function and sets component value to it.'}}, 'preprocess': {'return': {'type': 'str | None', 'description': 'Passes the extracted text into the function - string'}, 'value': None}}, 'events': {'submit': {'type': None, 'default': None, 'description': ''}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'SimpleTextExtractFromPDF': []}}}

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
# `gradio_simpletextextractfrompdf`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_simpletextextractfrompdf/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_simpletextextractfrompdf"></a>  
</div>

Extracts text from pdf documents
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_simpletextextractfrompdf
```

## Usage

```python

import gradio as gr
from gradio_simpletextextractfrompdf import SimpleTextExtractFromPDF

def first_200_chars(text):
    return text[:200]


demo = gr.Interface(
    fn=first_200_chars,
    inputs=SimpleTextExtractFromPDF(),
    outputs=gr.Textbox(label="First 200 characters of the extracted text"),
    title="Simple Text Extract From PDF",
    description=\"\"\"
## Component Description
This space is to demo the usage of the SimpleTextExtractFromPDF component.
This component provides a simple interface to extract text from a PDF file. The extracted text can be submitted as a string input to a function for further processing.
- **Text Extraction Only:** Only the text content is extracted from the PDF. Images and table structures are not preserved.
- **Flexible Upload Options:** Users can upload a PDF file from their device or provide a URL to the PDF.
- **Input Component:** The component is primarily designed to be used as an input, allowing users to submit the extracted text to other functions.
- **Output Display:** When used as an output component, the extracted string content is displayed in a textarea.
The demo app here uses the SimpleTextExtractFromPDF component as an input component to extract the text from a PDF file and then show the first 200 characters of the extracted text.
\"\"\",
    article=\"\"\"
<p>
    <code>pip install gradio-simpletextextractfrompdf</code>
    <br>
    <a href="https://pypi.org/project/gradio-simpletextextractfrompdf/"> https://pypi.org/project/gradio-simpletextextractfrompdf/</a>
</p>
\"\"\",
)


if __name__ == "__main__":
    demo.launch()
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `SimpleTextExtractFromPDF`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["SimpleTextExtractFromPDF"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["SimpleTextExtractFromPDF"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the extracted text into the function - string.
- **As output:** Should return, expects a {string} returned from the function and sets component value to it.

 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "SimpleTextExtractFromPDF-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          SimpleTextExtractFromPDF: [], };
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
