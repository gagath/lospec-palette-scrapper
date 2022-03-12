#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 Agathe Porte <microjoe@microjoe.org>
#
# SPDX-License-Identifier: MIT

from pathlib import Path
import asyncio
import json
import math

import aiohttp

RATE_LIMIT = 0.1  # max requests per second


async def rate_limit(*futures, per_sec):
    tasks = []
    for f in futures:
        tasks.append(asyncio.ensure_future(f))
        await asyncio.sleep(1 / per_sec)

    await asyncio.gather(*tasks)


async def save_palette(palette):
    hashtag = palette["hashtag"]

    d = Path(f"palettes/{hashtag}")
    d.mkdir(parents=True, exist_ok=True)

    with open(d / f"{hashtag}.json", "w") as f:
        json.dump(palette, f, indent=4)

    futures = [get_image(d, e["image"]) for e in palette["examples"]]
    await asyncio.gather(*futures)

    print(f"DONE: {hashtag}")


async def get(client, url):
    async with client.get(url) as response:
        assert response.status == 200, f"got status {response.status} for {url}"
        return await response.read()


async def get_image(paldir, path):
    async with aiohttp.ClientSession(loop=loop) as client:
        url = f"https://lospec.com/palette-examples/{path}"
        data = await get(client, url)
        out = paldir / Path(path).name
        out.write_bytes(data)


async def get_palette_list(page):
    url = (
        "https://lospec.com/palette-list/load"
        "?colorNumberFilterType=any"
        "&colorNumber=2151"
        f"&page={page}"
        "&tag="
        "&sortingType=default"
    )

    async with aiohttp.ClientSession(loop=loop) as client:
        data = await get(client, url)

    return json.loads(data.decode("utf-8"))


async def scrap_palette_list(page):
    print(f"SCRAP PAGE {page}")
    jn = await get_palette_list(page)
    futures = [save_palette(p) for p in jn["palettes"]]
    await asyncio.gather(*futures)


async def scrap_all():
    jn = await get_palette_list(1)
    total = jn["totalCount"]

    print(f"TOTAL: {total}")

    max_page = math.ceil(total / 8.0)
    full_range = True

    if full_range:
        futures = [scrap_palette_list(page) for page in range(1, max_page)]
    else:
        # Test range
        futures = [scrap_palette_list(page) for page in range(1, 3)]

    await rate_limit(*futures, per_sec=RATE_LIMIT)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap_all())
