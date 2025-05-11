"""Run this app with: streamlit run apps/streamlit/itables_app.py"""

from typing import Sequence, cast

import pyarrow
import streamlit as st
from st_aggrid import AgGrid  # type: ignore
from streamlit.components.v1.components import MarshallComponentException

import itables.options as it_opt
from itables.javascript import get_compact_style, get_expanded_classes
from itables.sample_dfs import get_countries, get_dict_of_test_dfs
from itables.streamlit import interactive_table

st.set_page_config(
    page_title="ITables in Streamlit",
    page_icon="https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/loading.svg",
)
st.logo(
    "https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/logo.svg",
    link="https://mwouts.github.io/itables/streamlit.html",
)
st.markdown(
    "![ITables](https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/wide.svg)"
)
st.sidebar.markdown(
    """
                    # ITables in Streamlit
                    ![Stars](https://img.shields.io/github/stars/mwouts/itables)
                    """
)

caption = st.sidebar.text_input("Caption", value="Countries")
select = st.sidebar.toggle("Row selection", value=True)
classes = st.sidebar.multiselect(
    "Classes",
    options=["display", "nowrap", "compact", "cell-border", "stripe"],
    default=get_expanded_classes(it_opt.classes),
)
buttons = st.sidebar.multiselect(
    "Buttons",
    options=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
    default=["copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
)

style = st.sidebar.text_input("Style", value=get_compact_style(it_opt.style))

render_with = st.sidebar.selectbox(
    "Render with", ["st.dataframe", "streamlit-aggrid", "itables"], index=2
)

include_html = st.sidebar.checkbox("Include HTML")
df = get_countries(html=include_html)

it_args = {}
if select:
    it_args["select"] = True
    it_args["selected_rows"] = [0, 1, 2, 100, 207]
if classes != get_expanded_classes(it_opt.classes):
    it_args["classes"] = classes
if style != it_opt.style:
    it_args["style"] = style

if buttons:
    it_args["buttons"] = buttons


if caption:
    it_args = {"caption": caption, **it_args}

if render_with == "st.dataframe":

    def render_table(df, key: str, **not_used):  # type: ignore
        return st.dataframe(df, key=key)

    snippet = """st.dataframe(df)
"""

elif render_with == "streamlit-aggrid":

    def render_table(df, key: str, **not_used):  # type: ignore
        return AgGrid(df, key=key)

    snippet = """from st_aggrid import AgGrid

AgGrid(df, key=None)
"""
else:
    formatted_args = ["df"] + [
        f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
        for key, value in it_args.items()
    ]
    formatted_args = ",\n                  ".join(formatted_args)

    def render_table(df, key, **it_args):
        return interactive_table(df, key=key, **it_args)

    snippet = f"""from itables.streamlit import interactive_table

interactive_table({formatted_args})
"""

st.markdown(
    f"""```python
{snippet}
```
"""
)

t = render_table(df, "my_table", **it_args)

st.header("Table state")
st.markdown(
    """The value returned by `interactive_table` is
a dict that contains the index of the selected rows:"""
)
st.write(t)

st.header("More sample dataframes")
test_dfs = get_dict_of_test_dfs()
tabs = st.tabs(cast(Sequence[str], test_dfs.keys()))

for (name, df), tab in zip(test_dfs.items(), tabs):
    with tab:
        try:
            interactive_table(df, key=name, classes=classes, style=style)
        except (
            # ITables
            NotImplementedError,
            # st.dataframe
            ValueError,
            # streamlit-aggrid
            pyarrow.lib.ArrowInvalid,  # type: ignore
            MarshallComponentException,
        ) as e:
            st.warning(e)
