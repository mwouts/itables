# PyDataTablesRenderers for Dash

## Maintainer note

`react-docgen` is intentionally pinned to `^5.4.3` in this package.

Reason: `dash-generate-components` (used by `npm run build:backends`) expects
`react-docgen.parse(...)` to return a single doc object. Newer `react-docgen`
majors can return an array shape, which breaks Dash metadata extraction with:

`TypeError: Cannot convert undefined or null to object`

If you want to upgrade `react-docgen`, verify that
`npm run build` still succeeds for this package, including the
`dash-generate-components` step.
