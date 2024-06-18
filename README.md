# Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Rules](#rules)
- [Setup Instructions](#setup-instructions)
- [Errors Encountered During Installation](#errors-encountered-during-installation)

## Introduction
This repo contains automation for API, Mobile, Web, and Integration of all these platforms. They will have *different virtual environments*.

For API Test Automation, it is using Data-Driven Testing where all scenarios are placed in a csv file to easily maintain, reuse, and easily add new scenarios to test. (NOT INCLUDED HERE)

NOTE: THIS STILL NEEDS REFACTORING AND CLEANING!!!

## Requirements
1. Python = v3.10.6
- Use pyenv to easily maneuver to different Python versions.

2. Visual Studio Code
- We prefer using this since there are a lot of plugins we can use here.
- Plugins used
    - Python/Pylance:  _Fast, feature-rich language support for Python_
    - Edit csv:        _For editing CSV Files_
    - Flake8 :         _Linting Support for Python files_
    - Markdown Preview Enhanced: _For Markdown Previewer_
    - Git Stash:       _For easy stashing ui of git_
    - Sonarlint:       _Additional Linters_

## Rules
Insert Rules Here

## Setup Instructions
1. Create '.env' and copy all the required data.
Insert Setup Instructions Here

## Errors Encountered During Installation
Insert Errors Encountered During Installation

## Visual Studio Code Settings
1. Hide all cache files
    a. Open Settings: `Ctrl` + `,` or `Cmd` + `,`. You can also open it by clicking the Gear Icon on the lower left corner and select "Settings"

    b. Add File Exclusions. You can search for "exclude" to navigate directly and add the following pattern.
    `**/__pycache__`
    `**/.pytest_cache`