
import gradio as gr
from app import demo as app
import os

_docs = {'ChatAGUI': {'description': 'AG-UI Chat component that supports real-time streaming and tool execution.', 'members': {'__init__': {'value': {'type': 'str | Callable | None', 'default': 'None', 'description': 'Initial value for the component.'}, 'api_root': {'type': 'str', 'default': '""', 'description': 'Root URL for the AG-UI API endpoints.'}, 'initial_thread_id': {'type': 'str', 'default': '""', 'description': 'Initial thread ID for the conversation.'}, 'label': {'type': 'str | None', 'default': '"AG-UI Chat"', 'description': 'The label for this component.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continuously calls `value` to recalculate it if `value` is a function.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value`.'}, 'show_label': {'type': 'bool | None', 'default': 'True', 'description': 'If True, will display label.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'Relative size compared to adjacent Components.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'Minimum pixel width.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will be rendered as editable.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string assigned as the id of this component.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings assigned as classes.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not be rendered.'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': 'Used in gr.render for component identity across re-renders.'}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': 'Parameters preserved across re-renders.'}}, 'postprocess': {'value': {'type': 'typing.Union[str, typing.Dict, NoneType][str, Dict, None]', 'description': 'Value to send to the frontend.'}}, 'preprocess': {'return': {'type': 'typing.Optional[typing.Dict][Dict, None]', 'description': 'Processed message data.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ChatAGUI changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the ChatAGUI.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the ChatAGUI is focused.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'ChatAGUI': []}}}

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
# `gradio_chatagui`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_chatagui
```

## Usage

```python

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ChatAGUI`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["ChatAGUI"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["ChatAGUI"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, processed message data.
- **As output:** Should return, value to send to the frontend.

 ```python
def predict(
    value: typing.Optional[typing.Dict][Dict, None]
) -> typing.Union[str, typing.Dict, NoneType][str, Dict, None]:
    return value
```
""", elem_classes=["md-custom", "ChatAGUI-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          ChatAGUI: [], };
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
