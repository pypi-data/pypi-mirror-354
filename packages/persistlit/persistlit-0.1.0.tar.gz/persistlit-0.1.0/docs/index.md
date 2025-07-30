# Persistlit

Convenient `streamlit` widgets that persist between pages.

## Installation

Persistlit is hosted on pypi. Install using pip:

`pip install persistlit`

or (preferably) a dependency manager like `uv`:

`uv add persistlit`

## Purpose

Perhaps you require a widget that persists between pages. This might be a configuration options or global variable that you would like to be able to access and adjust from multiple places within your app. It would be nice if something like this worked:

```python title="/pages/page1.py"
x = st.number_input("A number used across multiple pages", key='x')
do_something_with_x(x)
```

```python title="/pages/page2.py"
x = st.number_input("A number used across multiple pages", key='x')
do_something_different_with_x(x)
```

```python title="/pages/page3.py"
st.write(st.session_state["x"])
```

This will persist between page reload (utilizing `session_state["x"]`). But, when the page is changed both `x` and `session_state["x"]` are overwritten by the instantiated widget. Neither the displayed widget value nor `x` nor `session_state["x"]` are persisted as `x` is set to an empty string each time the widget is rendered.

### **Persistlit Solution**

`persistlit` adds a `persistant` boolean keyword argument to achieve precisely this: 

```python title="/pages/page1.py"
x = pt.text_input("Persistlit text input", peristant=True)
do_something_with_x(x)
```

```python title="/pages/page2.py"
x = pt.text_input("Persistlit text input", peristant=True)
do_something_different_with_x(x)
```

```python title="/pages/page3.py"
st.write(st.session_state['x'])
```

The widget is otherwise functionally equivalent to `st.text_input()`


### **Native Streamlit Solution**

This *can* be achieved in native `streamlit` by leveraging the `session_state` and using a combination of `x` and `_x` (for example) as keys for the "local" widget value and the "globally" accessible value associated with your widget respectively:
```python title="/pages/page1.py"
x = st.text_input(
    label="Streamlit text input",
    value=st.session_state.get('_x', None),
    key='x',
    on_change=lambda: st.session_state.update({'_x': st.session_state['x']})
)
st.write(x)
do_something_with_x(x)
```

```python title="/pages/page2.py"
x = st.text_input(
    label="Streamlit text input",
    value=st.session_state.get('_x', None),
    key='x',
    on_change=lambda: st.session_state.update({'_x': st.session_state['x']})
)
do_something_different_with_x(x)
```

```python title="/pages/page3.py"
st.write(st.session_state["_x"])
```

The primary problems with this are:
1. Is verbose for a reasonably common usecase
2. Requires using a key that *is not* the widget's primary key to access the variables on pages that do not contain the widget
3. Complicates the implementation of `on_change` in scenarios where other callbacks are required in addition to managing `session_stat["_x"]`.