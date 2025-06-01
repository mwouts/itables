"""Run this app with: streamlit run apps/streamlit/itables_app.py"""

from typing import Optional, Sequence, cast

import pyarrow  # type: ignore
import streamlit as st
from typing_extensions import Unpack

try:
    from st_aggrid import AgGrid  # type: ignore
except ImportError as e:
    import_error = e

    class AgGrid:
        def __init__(self, *args, **kwargs):  # type: ignore
            raise import_error


from streamlit.components.v1.components import MarshallComponentException

import itables
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
    default=itables.javascript.get_expanded_classes(itables.options.classes),
)
buttons = st.sidebar.multiselect(
    "Buttons",
    options=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
    default=["copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
)

style = st.sidebar.text_input(
    "Style", value=itables.javascript.get_compact_style(itables.options.style)
)

render_with = st.sidebar.selectbox(
    "Render with", ["st.dataframe", "streamlit-aggrid", "itables"], index=2
)

include_html = st.sidebar.checkbox("Include HTML")
df = itables.sample_dfs.get_countries(html=include_html)

it_args: itables.ITableOptions = {}
if select:
    it_args["select"] = True
    it_args["selected_rows"] = [0, 1, 2, 100, 207]
if classes != itables.javascript.get_expanded_classes(itables.options.classes):
    it_args["classes"] = classes
if style != itables.options.style:
    it_args["style"] = style

if buttons:
    it_args["buttons"] = buttons

if render_with == "st.dataframe":

    def render_table(df, key: str, caption: Optional[str], **not_used):  # type: ignore
        return st.dataframe(df, key=key)  # type: ignore

    snippet = """st.dataframe(df)
"""

elif render_with == "streamlit-aggrid":

    def render_table(df, key: str, caption: Optional[str], **not_used):  # type: ignore
        return AgGrid(df, key=key)  # type: ignore

    snippet = """from st_aggrid import AgGrid

AgGrid(df, key=None)
"""
else:
    formatted_args = ["df"] + [
        f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
        for key, value in it_args.items()
    ]
    formatted_args = ",\n                  ".join(formatted_args)

    def render_table(
        df: itables.DataFrameOrSeries,
        key: str,
        caption: Optional[str],
        **it_args: Unpack[itables.ITableOptions],
    ):
        return interactive_table(df, key=key, caption=caption, **it_args)

    snippet = f"""from itables.streamlit import interactive_table

interactive_table(df, caption='{caption}', {formatted_args})
"""

st.markdown(
    f"""```python
{snippet}
```
"""
)

t = render_table(df, caption=caption, key="my_table", **it_args)

st.header("Table state")
st.markdown(
    """The value returned by `interactive_table` is
a dict that contains the index of the selected rows:"""
)
st.write(t)  # type: ignore

st.header("More sample dataframes")
test_dfs = itables.sample_dfs.get_dict_of_test_dfs()
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
            pyarrow.lib.ArrowInvalid,  # pyright: ignore[reportUnknownMemberType,reportAttributeAccessIssue]
            MarshallComponentException,
        ) as e:  # pyright: ignore[reportUnknownVariableType]
            st.warning(e)  # pyright: ignore[reportUnknownArgumentType]
