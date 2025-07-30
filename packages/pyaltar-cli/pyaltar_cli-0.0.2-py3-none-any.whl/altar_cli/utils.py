import re

import click


def parse_version_slug(slug: str) -> str:
    refs, version = slug.split("@", maxsplit=1)

    if not refs or refs in ["release", "tag"]:
        refs = "tags"
    elif refs == "branch":
        refs = "heads"
    else:
        raise click.BadArgumentUsage("Invalid specifier: {}.")

    match version:
        case "latest":
            # TODO: Fetch the latest tag by querying Github releases
            parsed_slug = f"{refs}/v0.3.0"
        case _:
            if re.match(r"^v\d+\.\d+\.\d+$", version):
                parsed_slug = f"{refs}/{version}"
            else:
                parsed_slug = f"{refs}/{version}"

    return parsed_slug
