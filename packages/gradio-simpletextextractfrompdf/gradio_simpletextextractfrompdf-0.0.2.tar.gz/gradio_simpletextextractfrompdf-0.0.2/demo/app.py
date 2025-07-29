
import gradio as gr
from gradio_simpletextextractfrompdf import SimpleTextExtractFromPDF

def first_200_chars(text):
    return text[:200]


demo = gr.Interface(
    fn=first_200_chars,
    inputs=SimpleTextExtractFromPDF(),
    outputs=gr.Textbox(label="First 200 characters of the extracted text"),
    title="Simple Text Extract From PDF",
    description="Extract text from a PDF file or URL",
)


if __name__ == "__main__":
    demo.launch()
