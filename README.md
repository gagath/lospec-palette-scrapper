<!--
SPDX-FileCopyrightText: 2022 Agathe Porte <microjoe@microjoe.org>

SPDX-License-Identifier: MIT
-->

<p align="center">
  <img alt="Logo" src="docs/logo.png">
</p>

# Lospec palette scrapper

A web scrapper for the [Lospec color palettes](https://lospec.com/palette-list).

## Rationale

The [palettes](https://lospec.com/palette-list) on [Lospec](https://lospec.com/) are a great resource for pixel artists to use. However, one may not want to have all of the other bells of whistles of the Lospec website ([tutorials](https://lospec.com/pixel-art-tutorials), [jobs (??)](https://lospec.com/jobs)…). The goal of this software is to make all of the listed palettes on Lospec available offline for users. They may even be able to reuse the data and make nice software to browse it offline.

## SQLite DB

A SQLite database generated from the scrapped data [is available](lospec-palettes.sqlite).

![First 16 rows of the 'palette' SQL table](docs/sql-entries.png)

## Data

To mitigate possible future scrapping blocking policy, the scrapped data is available in the `palettes/` directory.

## Data copyright

### Palettes

Color palettes cannot be copyrighted:

> No, color palettes cannot be copyrighted in general terms. A business can copyright colors and color combinations for their brand but only for similar products when using a non-functional color (an example of a functional color is green for lawn products) if the public strongly associates the color with the brand.

[Question: How To Choose Pixel Art Palettes](https://www.seniorcare2share.com/how-to-choose-pixel-art-palettes/#Are_color_palettes_copyrighted) on [SeniorCare2Share](https://www.seniorcare2share.com/)

### Examples

However, example images provided by users may be copyrighted, although the website does not make it clear wether if they are still the property of their users (under which license?) or if they become the property of Lospec on upload. For this reason, **example images are not stored in the repository**. However, they will be downloaded if you run `scrap.py` on your own.

## Usage

If you want to get more up-to-date data or need the example images, you will need to run the `scrap.py` program.

This can usually be done using the `poetry run ./scrap.py` command.

### Rate-limit

The implementation has been written in a fully-[async](https://docs.python.org/3/library/asyncio.html) way. This was initially done because the web server took almost one second to answer every palette page request. However, it turned out that sending many requests in parallel to the web server would almost *bring it down*. So, a **rate-limit** mechanism (1 request every 10 seconds) has been implemented in order to protect the server.

## Licenses

This project is [REUSE-compliant](https://reuse.software/).

| Component | License                           |
|-----------|-----------------------------------|
| Software  | [MIT](LICENSES/MIT.txt)           |
| Data      | [CC0-1.0](LICENSES/CC0-1.0.txt)   |
| Database  | [ODbL-1.0](LICENSES/ODbL-1.0.txt) |