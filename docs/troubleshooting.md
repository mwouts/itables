# Troubleshooting

If the table just says "Loading...", then maybe
- You loaded a notebook that is not trusted (run "Trust Notebook" in View / Activate Command Palette)
- You forgot to run `init_notebook_mode`, or you deleted that cell or its output
- Or you ran `init_notebook_mode(connected=True)` but you are not connected to the internet?

Please note that if you change the value of the `connected` argument in
the `init_notebook_mode` cell, you will need to re-execute all the cells
that display interactive tables.

If the above does not help, please check out the [ChangeLog](changelog.md)
and decide whether you should upgrade `itables`.
