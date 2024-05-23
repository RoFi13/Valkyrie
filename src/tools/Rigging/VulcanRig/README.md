
# Vulcan Rig

Enter module summary here.

## Getting Started

### Standard Setup

- Clone this repository to your local storage
- Set up a virtual environment at the root via `py -m venv venv`
- Enter the python virtual environment via `venv\Scripts\activate`
- Install the package in this repository via `pip install .`
    Note: Assuming at root level or repository, replace `.` to point to location
    of the `setup.py` found at the root of this repository.

### Development Setup
You can see the realtime team's Python Development Environment details [here][PythonEnvSetup].
- Clone this repository to your local storage
- Set up a virtual environment at the root via `py -m venv venv`
- Enter the python virtual environment via `venv\Scripts\activate`
- Install the dev requirements for this repository via `pip install -r requirements.txt`
- Install an editable version of this repository via `pip install -e .`
    Note: Assuming at root level or repository, replace `.` to point to location
    of the `setup.py` found at the root of this repository.
- Run the unit tests to verify everything synced correctly via `pytest`
- Run the desired package invoking it by its name as logged in the Tools Index
   section disclosed below.

## Contributing

Contributions to the Vulcan Rig tool repository are highly encouraged
and welcomed. Please ensure:
- The required [one-pagers][RealtimeOnePager] and/or [Technical Design Documents][RealtimeTDD]
    are approved prior to contribution in accordance with the change process workflow
    adopted by the Realtime Team.
- The code you are submitting *must pass ALL unit tests and must have a minumum test coverage
    threshold of 80%*. Refer to the Testing section disclosed below.

### Testing

This repository relies on `pytest` for all unit/integration tests and `pytest-cov` for
code coverage tracking. To see more unit testing info, go [here][UnitTestingLink]. To run the tests:
- Open a command line terminal
- Navigate to the root of the repository
- Run `pytest --cov .` and verify the results are in line with the requirements of this
    repository.


### Code Style

- Code must conform to DNEG's coding standards and style guides whenever possible.
    - [Python][PythonStyleGuide]
    - [C++][CPPStyleGuide]
    - [C#][CSharpStyleGuide]

### Pull Request Process

To help get your pull request accepted please follow these steps:
- Ensure that your [one pager][RealtimeOnePager] / [TDD][RealTimeTDD] document has been approved prior to
    any work taking place.
- Create a new `feature/` or `bugfix/` branch applicable to your contribution.
- Author your contributions to the repo.
- Ensure that your code passes all tests and meets the minimum test coverage threshold.
- When creating the pull request, make sure you are merging into the correct
   staging branch. The staging branch for this repository is `develop`
- When creating the pull request, the maintainer will be added automatically
    to the PR. If this is not the case please email [rnd-realtime@dneg.com][RealtimeContact]
- Rely, whenever possible, on the auto-merging feature of stash. Rebase &
    re-test your changes if any conflicts arise.
- Unless there is an explicit reason to not, delete your branch following a
    successful merge.

## Versioning

We use [SemVer][SemVer] for versioning of the applicable packages.
For the versions available, see the tags on this repository.

## Maintainers

This repository is maintained by the RealTime Development Team.
You can contact them at [rnd-realtime@dneg.com][RealtimeContact]

## Further Reading (if any)

[PythonEnvSetup]:http://dnet.dneg.com/display/REALTIME/Python+Environment+Setup+for+Development+in+the+Realtime+Space
[UnitTestingLink]:http://dnet.dneg.com/pages/viewpage.action?spaceKey=REALTIME&title=Python+Unit+Test+Standards+enforced+on+the+Realtime+Team
[RealtimeContact]:mailto:rnd-realtime@dneg.com
[RealtimeOnePager]:https://docs.google.com/document/d/1PNi8_Mm4_vtVPT6efRHiITJBCWa0ZREyc46t63_lZKQ/edit?usp=sharing
[RealtimeTDD]:https://docs.google.com/document/d/18XflNCz0MpbpWcXEGWCq9kIUHecJZW1bO8XVy9_VZp8/edit?usp=sharing
[SemVer]:http://semver.org
[PythonStyleGuide]:http://i/tools/SITE/doc/coding-standards/latest/standards/languages/python/python_style_guide.html
[CPPStyleGuide]:http://i/tools/SITE/doc/coding-standards/latest/standards/languages/cpp/cpp_style_guide.html