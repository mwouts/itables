![ITables logo](https://raw.githubusercontent.com/mwouts/itables/3f8e8bd75af7ad38a500518fcb4fbbc370ea6c4c/itables/logo/wide.svg)

This package is a ESM bundle of [DataTables](https://datatables.net/)
and some of its extensions for [ITables](https://github.com/mwouts/itables/).

# How to compile the bundle

Run the following commands:
```bash
npm install
npm run build:js
```

# How to update the dependencies

Run
```bash
npm update
```
and check whether there are any outdated package with `npm outdated`.

# How to publish a new version

Update the dependencies, bump the version in `package.json`, and then:

```bash
# Package the extension
npm pack

# Publish the package on npm with
npm publish --access=public
```
