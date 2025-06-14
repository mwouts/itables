from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, render_widget

from itables.sample_dfs import get_dict_of_test_dfs
from itables.widget import ITable

dfs = get_dict_of_test_dfs()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "table_selector",
            "Table",
            choices=list(dfs.keys()),
            selected="int_float_str",
        )
    ),
    output_widget("my_table", fillable=False),
    ui.markdown("Selected rows"),
    ui.output_code("selected_rows"),
    title="Using the ITable Widget in a Shiny App",
    fillable=True,
)


def server(input, output, session):  # type: ignore
    @render_widget
    def my_table():
        """
        This function creates the "my_table" widget. While we could
        pass the df or the other arguments here, it's nicer
        to use a "reactive.effect" to update the widget
        """
        return ITable(caption="A table rendered with ITable", select=True)

    @reactive.effect
    def _():
        """
        This "reactive.effect" uses the "update" method of the ITable widget
        to update the widget with the new inputs.
        """
        # Get the new inputs
        df = dfs[input.table_selector()]  # pyright: ignore[reportUnknownMemberType]
        selected_rows = list(range(0, len(df), 3))

        # Update the widget
        assert isinstance(
            my_table.widget, ITable
        )  # otherwise pyright complains it might be None
        my_table.widget.update(df, selected_rows=selected_rows)

    ui.markdown("Selected rows")

    @render.code
    def selected_rows():  # pyright: ignore[reportUnusedFunction]
        """
        Here we read the "selected_rows" attribute of the ITable widget
        """
        assert isinstance(
            my_table.widget, ITable
        )  # otherwise pyright complains it might be None
        return str(reactive_read(my_table.widget, "selected_rows"))


app = App(app_ui, server)  # type: ignore
