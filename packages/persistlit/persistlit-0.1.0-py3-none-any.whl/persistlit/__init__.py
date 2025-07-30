import streamlit as st


def _store_value(key):
    # Safely initialize both keys if missing
    if key not in st.session_state:
        st.session_state[key] = None
    if f"_{key}" not in st.session_state:
        st.session_state[f"_{key}"] = None
    st.session_state[key] = st.session_state["_" + key]


def _load_value(key):
    # Safely initialize both keys if missing
    if key not in st.session_state:
        st.session_state[key] = None
    if f"_{key}" not in st.session_state:
        st.session_state[f"_{key}"] = None
    st.session_state[f"_{key}"] = st.session_state[key]
    return st.session_state[f"_{key}"]


def _make_on_change_callback(key, **kwargs):
    if "on_change" in kwargs:
        provided_on_change = kwargs.pop("on_change")

        def combined_callback(*args):
            provided_on_change(*args)
            _store_value(key)
            st.write(key, "updated")

        return kwargs, combined_callback

    else:
        return kwargs, lambda: _store_value(key)


def text_input(label, persistant=False, **kwargs):
    if persistant:
        key = kwargs.pop("key", label)

        kwargs, _on_change = _make_on_change_callback(key, **kwargs)

        x = st.text_input(
            label=label,
            value=_load_value(key),
            key=f"_{key}",
            on_change=_on_change,
            **kwargs,
        )
        return x

    else:
        return st.text_input(label=label, **kwargs)


def number_input(label, persistant=False, **kwargs):
    if persistant:
        key = kwargs.pop("key", label)

        kwargs, _on_change = _make_on_change_callback(key, **kwargs)

        x = st.number_input(
            label=label,
            value=_load_value(key),
            key=f"_{key}",
            on_change=_on_change,
            **kwargs,
        )
        return x

    else:
        return st.number_input(label=label, **kwargs)