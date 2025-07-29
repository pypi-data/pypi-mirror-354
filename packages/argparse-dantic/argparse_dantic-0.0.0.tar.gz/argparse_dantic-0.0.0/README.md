<div align="center">
<!-- Logo -->
<a href="https://pydantic-argparse.supimdos.com"><img src="https://raw.githubusercontent.com/SupImDos/pydantic-argparse/master/docs/assets/images/logo.svg" width="50%"></a>
<!-- Headings -->
<h1>Argparse Dantic</h1>
<p><em>Typed Argument Parsing with Pydantic Enhanced</em></p>
<!-- Badges (Row 1) -->
<a href="https://pypi.python.org/pypi/argparse-dantic"><img src="https://img.shields.io/pypi/v/pydantic-argparse"></a>
<a href="https://pepy.tech/project/pydantic-argparse"><img src="https://img.shields.io/pepy/dt/pydantic-argparse?color=blue"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/blob/master/LICENSE"><img src="https://img.shields.io/github/license/SupImDos/pydantic-argparse"></a>
<br>
</div>

## Help
See [documentation](https://pydantic-argparse.supimdos.com) for help.

## Requirements
Requires Python 3.8+, and is compatible with the Pydantic v1 API.

## Installation
Installation with `pip` is simple:
```console
$ pip install argparse-dantic
```

## Example
```py
from argparse_dantic import ArgumentParser, BaseModel, Field


class Arguments(BaseModel):
    # Required Args
    string: str = Field(description="a required string", aliases=["-s"])
    integer: int = Field(description="a required integer", aliases=["-i"])
    flag: bool = Field(description="a required flag", aliases=["-f"])

    # Optional Args
    second_flag: bool = Field(False, description="an optional flag")
    third_flag: bool = Field(True, description="an optional flag")


def main() -> None:
    # Create Parser and Parse Args
    parser = ArgumentParser(
        model=Arguments,
        prog="Example Program",
        description="Example Description",
        version="0.0.1",
        epilog="Example Epilog",
    )
    args = parser.parse_typed_args()

    # Print Args
    print(args)


if __name__ == "__main__":
    main()
```

```console
$ python3 example.py --help
usage: Example Program [-h] [-v] [-s STRING] [-i INTEGER] [-f | --flag | --no-flag]
                       [--second-flag] [--no-third-flag]

Example Description

required arguments:
  -s STRING, --string STRING
                        a required string
  -i INTEGER, --integer INTEGER
                        a required integer
  -f, --flag, --no-flag
                        a required flag

optional arguments:
  --second-flag         an optional flag (default: False)
  --no-third-flag       an optional flag (default: True)

help:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Example Epilog
```

```console
$ python3 example.py --string hello -i 42 -f
string='hello' integer=42 flag=True second_flag=False third_flag=True
```

## Advanced Example
```py
from argparse_dantic import ArgumentParser, BaseModel, Field, ActionNameBind

class GlobalModel(BaseModel):
    action_name: ActionNameBind # This is a special field that binds the action name to the model
    verbose: bool = Field(False, description="verbose output", global_=True)
    debug: bool = Field(False, description="debug output", global_=True)

class PubOptionsModel(BaseModel):
    target: str = Field(description="build target", aliases=["-t"])
    clean: bool = Field(False, description="clean build", aliases=["--c"])

class BuildCommandModel(GlobalModel, PubOptionsModel):
    build_type: str = Field(description="build type", aliases=["-bt"])

class InstallCommandModel(GlobalModel, PubOptionsModel):
    install_type: str = Field(description="install type", aliases=["-it"])

class BasicModel(GlobalModel):
    build: BuildCommandModel = Field(aliases=["bd"], description="build command")
    install: InstallCommandModel = Field(aliases=["ins"], description="install command")

def main() -> None:
    # Create Parser and Parse Args
    parser = ArgumentParser(
        model=BasicModel,
        prog="Example Program",
        description="Example Description",
        version="0.0.1",
        epilog="Example Epilog",
    )
    args = parser.parse_typed_args()

    # Print Args
    print(args)

    # Get Command Arguments Faster
    command_arguments = getattr(args, args.action_name)

    # Get Global Arguments Faster
    verbose = args.global_data.get("verbose")
    debug = args.global_data.get("debug")
    # In child models you can also access global data
    # verbose = command_arguments.global_data.get("verbose")
    # debug = command_arguments.global_data.get("debug")
```

## License
This project is licensed under the terms of the MIT license.
