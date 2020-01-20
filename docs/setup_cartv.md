# CarTV Setup

The CarTV frontend requires Node.js (tested with version 8.11) to build. The framework is Vue.js, with the extensions Vue Router and Vuex a library for state management.

## 1) Load required software packages

In a Node.js project, the required software packages are stored in the package.json file. Go to the directory `src/Raspberry Pi/CarTV`.

Execute the following command to load the required software packages for development with the Node.js Package Manager (npm):

```bash
npm install --only=dev
```

## 2) Execute defined command

```bash
npm run build
npm run prod
```

These commands are the same and build the front end of the CarTV in production mode. This means that the generated files are optimized (e.g. additionally compressed).

It is then also no longer possible to examine the webapp using Vue Devtools (Chrome, Firefox).

```bash
npm run dev
```

This command builds the frontend of the CarTV in debug mode. Generated files are not compressed and the webapp can be examined with Vue Devtools (Chrome, Firefox).

```bash
npm run watch
```

This command, like npm run dev, builds the CarTV in debug mode. Afterwards, as long as this command is running, changes in the source files are watched for and necessary files are rebuilt.

```bash
npm run clean
```

This command cleans up the generated files (deletes the static folder).
Recommendation

For easy testing use the build/prod command. For further development of the webapp use the watch command.
