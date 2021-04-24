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

```
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
  --group-name-remove GROUP_NAME_REMOVE [GROUP_NAME_REMOVE ...]
                        strings to be removed from group (sheet) name (default: . - _)
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

As an example, we can generate stencil from
[AWS Architecture Icons](https://aws.amazon.com/architecture/icons/).

New AWS Icons are published from time to time.
Different versions have different directories structure.

### v20210131

Download
[AWS-Architecture_Asset-Package_20210131](https://d1.awsstatic.com/webteam/architecture-icons/q1-2021/AWS-Architecture_Asset-Package_20210131.a41ffeeec67743738315c2585f5fdb6f3c31238d.zip)
and unpack it.

It contains 3 more zip files.
Service, Category, and Resource icons are in separate packages.
Unpack `Architecture-Service-Icons_01-31-2021.zip`.

Run script with options:

```bash
omnigraffle-stencil \
    --svg-dir "Asset-Package_20210131/Architecture-Service-Icons_01-31-2021" \
    --stencil-file AWS_20210131_Services.gstencil \
    --filename-includes _48 \
    --stencil-name-remove Arch_ _48 . - _ \
    --group-name-remove Arch_ . - _
```

Output stencil will be created as `AWS_20210131_Services.gstencil`.

Check out the [AWS 2021-01-31 stencil in Stenciltown](https://stenciltown.omnigroup.com/stencils/aws-2021-01-31-all/) -
it contains all Category, Service, and Resource icons.

### v20200911

Download
[AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911](https://d1.awsstatic.com/webteam/architecture-icons/Q32020/AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911.478ff05b80f909792f7853b1a28de8e28eac67f4.zip)
and unpack it.

Run script with options:

```bash
omnigraffle-stencil \
    --svg-dir "AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911/AWS-Architecture-Service-Icons_20200911" \
    --stencil-file AWS_20200911_Services.gstencil \
    --filename-includes _48 \
    --stencil-name-remove Arch_ _48 . - _ \
    --group-name-remove Arch_ . - _
```

Output stencil will be created as `AWS_20200911_Services.gstencil`.

Check out the [AWS 2020-09-11 stencil in Stenciltown](https://stenciltown.omnigroup.com/stencils/aws-2020-09-11-all/) -
it contains all Service and Resource icons.

## Development

Requires Python 3.8+ and [Poetry](https://python-poetry.org/).

Install dependencies in virtual env:

```bash
poetry shell
poetry install
```

Troubleshooting installing `pillow` library on MacOS:
https://akrabat.com/installing-pillow-on-macos-10-15-calatalina/

Get virtual env path for the IDE:

```bash
poetry env info -p
```

Run script:

```bash
poetry run omnigraffle-stencil
```

## Publishing

Build and publish package:

```bash
poetry build
poetry publish
```
