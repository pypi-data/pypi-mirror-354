
### Fixed

- Sets the lower-bound on `typing-extensions` to `4.14.0`. The
motivation for this is that currently installing pygen in a `pyodide`
environment causes a `ValueError: Requested 'typing-extensions>=4.14.0',
but typing-extensions==4.11.0 is already installed`. By setting
lower-bound should force `pyodide` to download the correct version of
`typing-extensions`.