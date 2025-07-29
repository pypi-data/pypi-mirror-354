
import gradio as gr
from gradio_chatagui import ChatAGUI


example = ChatAGUI().example_value()

demo = gr.Interface(
    lambda x:x,
    ChatAGUI(),  # interactive version of your component
    ChatAGUI(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
