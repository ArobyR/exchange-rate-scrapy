# Exchage rate scrapy

## Requirements

### Minimum required versions

- Python >= 3.7
- Scrapy >= 2.0 (!= 2.4.0)
- Playwright >= 1.15

[check scrapy playwright doc](https://github.com/scrapy-plugins/scrapy-playwright)

## Installation

Creating the environment:

    python -m venv env

Active the env.:

    source /path/to/venv/bin/activate

Download the packages:

    pip3 install -r requirements.txt

Move to the project, in my case the name is ratescrapy.

Install the required browsers

```bash
playwright install
```

It's also possible to install only a subset of the available browsers:

```bash
playwright install firefox chromium
```

## Run

You can run with the custom configuration:

```bash
scrapy crawl <spider_name>
```

with params for save in .json, for example:

```bash
scrapy crawl <spider_name> -o output.json
```

or create your own custom settings.

## Notes / Disclaimer

1. This scrapy script respect the ROBOTSTXT_OBEY (ROBOTSTXT_OBEY = True).
2. The repo need some updates, example: for a better env and performance you can delete selenium and just use playwright.
