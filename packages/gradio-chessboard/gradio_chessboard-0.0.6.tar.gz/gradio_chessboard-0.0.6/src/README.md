---
tags: [gradio-custom-component, custom-component-track, chess, chessboard, games]
title: gradio_chessboard
short_description: Gradio component for chessboard interaction
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_chessboard`
<a href="https://pypi.org/project/gradio_chessboard/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_chessboard"></a> <a href="https://github.com/czakop/chess-agent/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> <a href="https://huggingface.co/spaces/czakop/gradio_chessboard/discussions" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/%F0%9F%A4%97%20Discuss-%23097EFF?style=flat&logoColor=black"></a>

Gradio component for chessboard interaction

## Installation

```bash
pip install gradio_chessboard
```

## Usage

```python
import random

import chess
import gradio as gr
from gradio_chessboard import Chessboard


def random_move(fen: str) -> str:
    board = chess.Board(fen)
    moves = list(board.legal_moves)
    move = random.choice(moves)
    board.push(move)
    return board.fen()


with gr.Blocks() as demo:
    gr.Markdown("# Play Chess with Gradio Chessboard")
    gr.Markdown(
        "This is a demo of the Gradio Chessboard component. You can play chess on it or use it to edit the position."
    )
    chessboard = Chessboard(label="Board", game_mode=True)
    chessboard.move(random_move, chessboard, chessboard)


if __name__ == "__main__":
    demo.launch()

```

## `Chessboard`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">default fen. If a function is provided, the function will be called each time the app loads to set the initial value of this component.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | I18nData | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will be rendered as a draggable chessboard; if False, dragging will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | tuple[int | str, ...] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render.</td>
</tr>

<tr>
<td align="left"><code>preserved_by_key</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>"value"</code></td>
<td align="left">A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor.</td>
</tr>

<tr>
<td align="left"><code>game_mode</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">if True, the chessboard will be rendered in game mode, allowing users to play chess on it. If False, it will be rendered in edit mode, allowing users to edit the chessboard without playing. Defaults to False.</td>
</tr>

<tr>
<td align="left"><code>orientation</code></td>
<td align="left" style="width: 25%;">

```python
Literal["white", "black"]
```

</td>
<td align="left"><code>"white"</code></td>
<td align="left">the orientation of the chessboard, either "white" or "black". Defaults to "white".</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `submit` | This listener is triggered when the user presses the Enter key while the Chessboard is focused. |
| `change` | Triggered when the value of the Chessboard changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `move` | Event triggered when a move is made on the chessboard in game mode. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, a FEN string representing the chessboard state if payload is provided, otherwise None.
- **As input:** Should return, fEN string representing the chessboard state, or None if no value is provided.

 ```python
 def predict(
     value: str | None
 ) -> str | None:
     return value
 ```
 
