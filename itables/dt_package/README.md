This package is a ESM bundle of [DataTable](https://datatables.net/)
and some of its extensions for [ITables](https://github.com/mwouts/itables/).

# How to compile the bundle

Run the following commands:
```bash
npm install
npm run build
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
