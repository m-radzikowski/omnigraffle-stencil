# OmniGraffle Stencil generator

Tool to create [OmniGraffle](https://www.omnigroup.com/omnigraffle/)
stencils from SVG icons.

Features:

- create multiple sheets by directory
- parametrize object magnets
- filter images and format icon names

Idea based on script from
[AWS-OmniGraffle-Stencils](https://github.com/davidfsmith/AWS-OmniGraffle-Stencils/)

## Usage

Requires Python 3.8+.

Install:

```bash
pip3 install omnigraffle-stencil
```

Run:

```bash
omnigraffle-stencil --help
```

to see all options:

```bash
usage: omnigraffle-stencil [-h] [--svg-dir SVG_DIR] [--stencil-file STENCIL_FILE] [--filename-includes [FILENAME_INCLUDES [FILENAME_INCLUDES ...]]] [--filename-excludes [FILENAME_EXCLUDES [FILENAME_EXCLUDES ...]]]
                           [--stencil-name-remove [STENCIL_NAME_REMOVE [STENCIL_NAME_REMOVE ...]]] [--no-vertex-magnets] [--side-magnets SIDE_MAGNETS] [--text-output]

Convert SVG files into OmniGraffle stencil

optional arguments:
  -h, --help            show this help message and exit
  --svg-dir SVG_DIR     svg files directory path (default: ./svg)
  --stencil-file STENCIL_FILE
                        name of output stencil file (default: output.gstencil)
  --filename-includes [FILENAME_INCLUDES [FILENAME_INCLUDES ...]]
                        strings to filter image file name by, taking only those which contains them all
  --filename-excludes [FILENAME_EXCLUDES [FILENAME_EXCLUDES ...]]
                        strings to filter image file name by, taking only those which do not contain any of them
  --stencil-name-remove [STENCIL_NAME_REMOVE [STENCIL_NAME_REMOVE ...]]
                        strings to be removed from image file name when creating stencil name (default: . - _)
  --no-vertex-magnets   don't create magnets on vertices (NE, NW, SE, SW)
  --side-magnets SIDE_MAGNETS
                        number of magnets for each side (default: 5)
  --text-output         write OmniGraffle data file as text instead of binary
```

Input files are taken from the given location (`./svg` by default)
and should be grouped into directories.
Every directory will be parsed to a separate canvas in output stencil.

SVG directories structure example:

```
svg/
├── Group 1/
│   ├── icon1.svg
│   ├── icon2.svg
│   ├── icon3.svg
└── Group 2/
    ├── icon4.svg
    └── icon5.svg
```

### AWS Architecture Icons example

To generate icons from
[AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)
download SVG zip file
(example: [AWS-Architecture-Icons_SVG_20200430](https://d1.awsstatic.com/webteam/architecture-icons/AWS-Architecture-Icons_SVG_20200430.974b253cb3059403544585500365fb828d305321.zip))
and unpack it.

Run script with options:

```bash
omnigraffle-stencil \
    --svg-dir "AWS-Architecture-Icons_SVG_20200430/SVG Light" \
    --stencil-file AWS_2020_light.gstencil \
    --filename-includes light-bg \
    --stencil-name-remove . - _ light-bg
```

Output stencil will be created as `AWS_2020_light.gstencil`.

## Development

Requires Python 3.8+ and [Poetry](https://python-poetry.org/).

Install dependencies in virtual env:

```bash
poetry shell
poetry install
```

Get virtual env path for the IDE:

```bash
poetry env info -p
```

Run script:

```bash
poetry run omnigraffle-stencil
```
