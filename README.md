# OmniGraffle SVG to Stencil

Create OmniGraffle stencil from SVG icons.

Idea based on script from
[AWS-OmniGraffle-Stencils](https://github.com/davidfsmith/AWS-OmniGraffle-Stencils/)

## Development

Requires Python 3.8+ and [Poetry](https://python-poetry.org/)

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
poetry run python omnigraffle_svg_to_stencil
```

## Usage

Run:

```bash
poetry run python omnigraffle_svg_to_stencil --help
```

to see options.

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
poetry run python omnigraffle_svg_to_stencil \
    --svg-dir "AWS-Architecture-Icons_SVG_20200430/SVG Light" \
    --stencil-file AWS_2020_light.gstencil \
    --filename-includes light-bg \
    --stencil-name-remove . - _ light-bg
```

Output stencil will be created as `AWS_2020_light.gstencil`.
