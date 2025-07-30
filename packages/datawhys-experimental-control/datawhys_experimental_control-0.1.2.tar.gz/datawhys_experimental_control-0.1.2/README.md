# datawhys_experimental_control

[![Github Actions Status](https://github.com/aolney/datawhys-experimental-control/workflows/Build/badge.svg)](https://github.com/aolney/datawhys-experimental-control/actions/workflows/build.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aolney/datawhys-experimental-control/main?urlpath=lab)


A JupyterLab extension that locks down the user interface and provides additional controls for running experiments using the JupyterLab platform. It is not configurable but may serve as an example for other projects.

## How to use

- Install the extension (see below)
- Append `lock=1` to the URL query string to lock out parts of the JLab interface
- Append `qualtrics=1` to the URL query string if you want the user to sequentially navigate notebooks from qualtrics questions

If the `lock` parameter is not set, the extension will not be active.

The following `lock` behaviors are implemented:

- Left navbar collapsed (e.g. file explorer)
- Left navbar hidden
- Launcher and terminal tabs hidden
- Notebook tab close button disabled
- Bottom status bar hidden
- Auto renders markdown in case users accidentally double click

The following `qualtrics` behavior are implemented

- For WE/PS1, checks the expected number of code cells have been executed before giving password

**Qualtrics integration:** Have a qualtrics question with a link to the notebook and a text entry box. Put a validator on the text entry box for the password returned by the extension. During the survey, the link out will take the participant to a JHub with the extension installed. When they complete a notebook, a link will appear giving them a password to enter on the Qualtrics side. Once they enter the password, Qualtrics will let them advance to the next question.

## Requirements

- JupyterLab >= 4.0.0

## Install

To install the extension, execute:

```bash
pip install datawhys_experimental_control
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall datawhys_experimental_control
```

## Contributing

- Andrew Olney

### Development install

Creating a virtual environment is recommended:

```
    curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
    bash Miniforge3-$(uname)-$(uname -m).sh

    !!! Edit the environment.yml file to change the environment name as you like !!!

    mamba env create -f environment.yml

    /home/ubuntu/miniforge3/bin/mamba init

    mamba activate <NAME>
```

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the datawhys_experimental_control directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

*The watch.sh script runs JupyterLab in watch mode with the Chrome browser*

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall datawhys_experimental_control
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `datawhys_experimental_control` within that folder.

### Testing the extension

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
