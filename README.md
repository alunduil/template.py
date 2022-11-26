# template.py

[Homepage][repository]

By Alex Brandt <alunduil@gmail.com>

## Description

You can use template.py to create a new GitHub repository.  The repository will
have poetry, VS Code devcontainers, and various GitHub actions ready to use.

template.py is related to [Cookiecutter] because both are templates for
bootstrapping projects.  template.py allows you to have a full development
environment with only VS Code and it's "Remote Development" plugin.
[Cookiecutter] expects you to re-use your development environment for multiple
projects.
## Terms of use

You are free to use template.py as a basis for your own projects without any
conditions.  See the [LICENSE] file for details.

## Prerequisites

1. VS Code with "Remote Development" installed

## How to use this template

1. Visit [the repository][repository]
1. Click "Use this template"
1. Follow the GitHub Docs to [Create a repo][create a repo]
1. Open VS Code
1. Open the command prompt (ctrl+shift+p)
1. Type "clone repository in container" and hit return
1. Input the GitHub URL of your new repository
1. In the resulting terminal (ctrl+\`), run: `poetry run initialise`
1. Resolve the README update issue that is generated
1. Continue working on your awesome project

## Documentation

* [LICENSE]: The license governing use of template.py

## Getting Help

* [GitHub Issues][issues]: Support requests, bug reports, and feature requests

## How to Help

* Submit [issues] for problems or questions
* Submit [pull requests] for proposed changes

[create a repo]: https://docs.github.com/en/get-started/quickstart/create-a-repo
[issues]: https://github.com/alunduil/template.py/issues
[LICENSE]: ./LICENSE
[pull requests]: https://github.com/alunduil/template.py/pulls
[repository]: https://github.com/alunduil/template.py
[Cookiecutter]: https://github.com/cookiecutter/cookiecutter
