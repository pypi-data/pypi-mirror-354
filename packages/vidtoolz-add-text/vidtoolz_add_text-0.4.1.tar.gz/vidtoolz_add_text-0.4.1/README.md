# vidtoolz-add-text

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-add-text.svg)](https://pypi.org/project/vidtoolz-add-text/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-add-text?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-add-text/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-add-text/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-add-text/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-add-text/blob/main/LICENSE)

Add text to a video file

![Demo](https://raw.githubusercontent.com/sukhbinder/vidtoolz-add-text/refs/heads/main/demo.png)

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-add-text
```
## Usage

type ``vid addtext --help`` to get help

```bash
usage: vid addtext [-h] [-t TEXT] [-mt MULTI_TEXT] [-o OUTPUT]
                   [-p {top-left,top-right,bottom-left,bottom-right,center,bottom}]
                   [-st START_TIME] [-et END_TIME] [-f FONTSIZE]
                   [-pad PADDING] [-d DURATION]
                   main_video

Add text to a video file

positional arguments:
  main_video            Path to the main video file.

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to write
  -mt MULTI_TEXT, --multi-text MULTI_TEXT
                        Multi-text in format "text,start,duration". Can be
                        used multiple times. ex "hello,1:20,10"
  -o OUTPUT, --output OUTPUT
                        Output video file name (default: None)
  -p {top-left,top-right,bottom-left,bottom-right,center,bottom}, --position {top-left,top-right,bottom-left,bottom-right,center,bottom}
                        Position of the text (default: bottom)
  -st START_TIME, --start-time START_TIME
                        Start time when text should appear: (default: 0)
  -et END_TIME, --end-time END_TIME
                        End time when text should disappear. (default: None)
  -f FONTSIZE, --fontsize FONTSIZE
                        Fontsize (default: 50)
  -pad PADDING, --padding PADDING
                        Padding (default: 50)
  -d DURATION, --duration DURATION
                        Duration in seconds (default: 4)



```


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-add-text
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
