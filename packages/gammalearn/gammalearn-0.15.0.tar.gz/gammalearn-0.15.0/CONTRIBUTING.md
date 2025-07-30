<!-- omit in toc -->
# Contributing to gammalearn

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued.
See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them.
Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved.
Thank you :)

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Share and talk about the project
> - Cite the project in your work

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [Join gitlab.in2p3.fr](#join-gitlabin2p3fr)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating in it is governed by the
[gammalearn Code of Conduct](https://gitlab.in2p3.fr/gammalearn/gammalearnblob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <thomas.vuillaume_a.t_lapp.in2p3.fr>.

## Join gitlab.in2p3.fr

To contribute through the gitlab platform, you need to have an account on [gitlab.in2p3.fr](https://gitlab.in2p3.fr/).
If you don't have an account yet, you can create one [here](https://gitlab.in2p3.fr/users/sign_in).

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://gammalearn.pages.in2p3.fr/gammalearn/).

Before you ask a question, it is best to search for existing [Issues](https://gitlab.in2p3.fr/gammalearn/gammalearn/issues) that might help you. 
In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://gitlab.in2p3.fr/gammalearn/gammalearn/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project version and running environment.

We will then take care of the issue as soon as possible.


## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Reporting Bugs


A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report.
Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://gammalearn.pages.in2p3.fr/gammalearn/). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://gitlab.in2p3.fr/gammalearn/gammalearn/issues).
- Also make sure to search the internet to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Environment (Conda, Docker,...)
  - GammaLearn version 
  - Possibly your input and the output
  - Can you reliably reproduce the issue? If so, what are the steps to reproduce it?


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for gammalearn, **including completely new features and minor improvements to existing functionality**.
Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Perform a [search](https://gitlab.in2p3.fr/gammalearn/gammalearn/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Open an [Issue](https://gitlab.in2p3.fr/gammalearn/gammalearn/issues/new) if you have not found a similar suggestion to discuss it with the community and maintainers before starting to work on it. Add the label `Improvement` to the issue.


### Your First Code Contribution

#### Get a development environment

To contribute to the project, you either need to run our docker development container, or install it with conda locally.
You can find the instructions in the [documentation](https://gammalearn.pages.in2p3.fr/gammalearn/).


#### Coding practices

Gammalearn aims to follow a [trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development). Please make your changes in a dedicated branch, and don't hesitate to ask for feedback in a merge request early in the development!

Gammalearn uses [`ruff`](https://docs.astral.sh/ruff/) to preserve a consistent code formating and linting. The projects rules are available in [`ruff.toml`](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/blob/master/ruff.toml). 
`ruff` is available in the development container. The checks will be run by the CI/CD and must pass. You can run checks and formatting this way:
```bash
# apply linter
(base) mambauser@...:/src$ ruff check
# format code
(base) mambauser@...:/src$ ruff format
```

More automated ways exist depending on your preferences: IDE extensions, pre-commit hooks...


#### Improving The Documentation

Improving the documentation is a great way to contribute to the project. 
We appreciate your efforts to make the documentation more understandable and complete.

Gammalearn follows `numpy`'s [style guide](https://numpydoc.readthedocs.io/en/latest/format.html) for documentation via the python docstrings.

The documentation is build using sphinx. The following command will build the documentation locally in the `htmldoc` folder.
```bash
# from inside a development container, in the gammalearn root directory:
sphinx-build -b html -j `nproc` --fail-on-warning docs htmldoc
```

#### Unit and integration tests

Please add unit and/or integration tests when introducing new code to ensure its reliability.
- Unit Tests: Focus on individual components or functions to verify their correctness in isolation. They should be implemented usying `pytest` framework in the `tests` module.
- Integration Tests: Assess the interaction between multiple components to ensure they work together seamlessly, especially used to test the training or inference of a model with a experiment settings. They are implemented directly in `.gitlab-ci.yml`.

## Styleguides

## Join The Project Team
Please email thomas.vuillaume_a_t_lapp.in2p3.fr if you are interested in joining the project team.

<!-- omit in toc -->
## Attribution
This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!
