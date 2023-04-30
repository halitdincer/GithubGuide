
![githubguide banner](./images/banner.jpg)

Follow this [tutorial](https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/#load-unpacked) to install the RepoExplainer Chrome extension.

## Usage

1. After you've installed the extension, make sure it is enabled.
2. Once enabled, all GitHub repositories you visit will automatically have an info icon that tells you more information about each file and folder.
   If you hover over the info icon, a pop-up box containing information about the corresponding file/folder will appear.

## Example Output

```
--- REPOSITORY FILE TREE ---
README.md         : Project description
LICENSE           : License information
requirements.txt  : Required packages
setup.py          : Installation script
io (folder)       : Contains classes and auxiliary code for I/O operations
 ├─► json (folder)    : Contains packages and code related to json I/O
 ├─► xml  (folder)    : Contains classes related to converting data to/from XML
 └─► base.py          : Abstract implementation of the generic I/O interface
```

## Contributing

Contributions are always welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes. Before submitting your pull request, please ensure that your code includes tests for any new functionality.
