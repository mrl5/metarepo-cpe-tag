#!/usr/bin/env python3


import asyncio
import json
import logging
import sys
from pathlib import Path

import pop.hub
from aiohttp import ClientSession, TCPConnector

hub = pop.hub.Hub()
hub.pop.sub.add(dyne_name="metarepo2json", omit_class=False)

ALLOWED_SOURCES = ["fs", "web"]


def exit_on_invalid_source(source):
    if source not in ALLOWED_SOURCES:
        sys.exit(f"Invalid source: {source}")


def process_errors(errors):
    sys.stderr.write("\n\n")
    for e in errors:
        logging.error(repr(e))
    sys.stderr.write("\n\nErrors encountered.\n")


async def setup_kits_instance(kits_instance):
    if type(kits_instance) is hub.metarepo2json.kits.kits_web.KitsFromWeb:
        uri = hub.OPT.metarepo2json.repo_web
        async with ClientSession() as session:
            await kits_instance.load_data(location=uri, session=session)
        await kits_instance.process_data()


async def setup_cats_instance(cats_instance, commit):
    if (
        type(cats_instance)
        is hub.metarepo2json.categories.categories_fs.CategoriesFromFileSystem
    ):
        await cats_instance.load_data(commit=commit)
        await cats_instance.process_data()
    if (
        type(cats_instance)
        is hub.metarepo2json.categories.categories_web.CategoriesFromWeb
    ):
        uri = hub.OPT.metarepo2json.repo_web
        async with ClientSession() as session:
            await cats_instance.load_data(uri, session=session, commit=commit)
        await cats_instance.process_data()


async def setup_catpkgs_instance(catpkgs_instance, category, commit):
    if (
        type(catpkgs_instance)
        is hub.metarepo2json.catpkgs.catpkgs_fs.CatPkgsFromFileSystem
    ):
        await catpkgs_instance.load_data(category=category, commit=commit)
    if type(catpkgs_instance) is hub.metarepo2json.catpkgs.catpkgs_web.CatPkgsFromWeb:
        uri = hub.OPT.metarepo2json.repo_web
        conn = TCPConnector(limit=10)
        async with ClientSession(connector=conn) as session:
            await catpkgs_instance.load_data(
                uri, session=session, category=category, commit=commit
            )
            await catpkgs_instance.process_data()


def get_sha1_for_recent_stable_branch(kit):
    prime_branches = list(filter(lambda x: x["stability"] == "prime", kit["branches"]))
    prime_branches_names = list(map(lambda x: x["name"], prime_branches))
    prime_branches_names.sort()
    recent_prime_branch = list(
        filter(lambda x: x["name"] == prime_branches_names.pop(), prime_branches)
    ).pop()
    return recent_prime_branch["sha1"]


async def create_kits_file(source, loc):
    kits_instance = hub.metarepo2json.factory.get_kits_instance(source=source)
    await setup_kits_instance(kits_instance)
    kits = await kits_instance.get_result()
    for kit in kits:
        commit = get_sha1_for_recent_stable_branch(kit)
        kit_path = Path(loc / f"{kit['name']}.json")
        kit_path.touch(mode=0o664)
        cats_instance = hub.metarepo2json.factory.get_categories_instance(
            kit=kit["name"], source=source
        )
        await setup_cats_instance(cats_instance, commit)
        categories = await cats_instance.get_result()
        for category in categories:
            catpkgs_instance = hub.metarepo2json.factory.get_catpkgs_instance(
                kit=kit["name"], source=source
            )
            await setup_catpkgs_instance(catpkgs_instance, category["name"], commit)
            category["packages"] = await catpkgs_instance.get_result()
        kit["catpkgs"] = categories
        with open(kit_path, "w") as f:
            f.write(json.dumps(kit))


if __name__ == "__main__":
    source = hub.OPT.metarepo2json.data_source
    exit_on_invalid_source(source)
    expected_errors = [
        hub.metarepo2json.errors.InvalidStructureError,
        hub.metarepo2json.errors.CorruptedMetarepoError,
        hub.metarepo2json.errors.GitServiceError,
        hub.metarepo2json.errors.GitHubRepoURIError,
        hub.metarepo2json.errors.FuntooStashRepoURIError,
    ]
    try:
        workdir = Path.home() / hub.OPT.metarepo2json.output_dir
        Path.mkdir(workdir, parents=True, exist_ok=True)
        errors = asyncio.run(create_kits_file(source, workdir))
        if errors:
            process_errors(errors)
            sys.exit(1)
    except Exception as e:
        if type(e) in expected_errors:
            sys.exit(f"{type(e).__name__}: {str(e)}")
        else:
            raise e
