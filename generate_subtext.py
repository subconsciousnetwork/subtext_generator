#!/usr/bin/python3
import random
import re
from pathlib import Path
import argparse


parser = argparse.ArgumentParser(
    description='Generate many random subtext files for testing'
)
parser.add_argument(
    '--src',
    type=str,
    default="the-prophet.subtext",
    help='The source text to draw from'
)
parser.add_argument(
    '--max',
    type=int,
    default=10,
    help='Max number of files to generate'
)


def random_hex():
    return "%030x" % random.randrange(16**30)


def random_hash():
    hex = random_hex()
    return hex[0:8]


def read_content_lines(filename):
    """Read all lines in file into an array"""
    with open(filename) as file:
        for line in file:
            clean_line = line.strip()
            if clean_line != "":
                yield clean_line


def generate_random_subtext_doc(lines):
    """
    Generate a random subtext document from an array of lines
    """
    nblocks = random.randint(3, 15)
    blocks = []
    for x in range(nblocks):
        block = random.choice(lines)
        blocks.append(block)
    return "\n\n".join(blocks)


def generate_random_subtext_docs(lines, count=10):
    """
    Generate N random subtext docs from lines.
    """
    for _ in range(count):
        yield generate_random_subtext_doc(lines)


def write_file(path, content):
    with open(path, "a") as file:
        file.write(content)


def to_slug(string):
    string = string[0:80]
    string = string.strip()
    string = string.lower()
    string = re.sub(
        r'[\n\/\*\'\"\.\:\;\,\!\?\@\#\$\%\^\&\(\)\[\]\{\}\~\`]',
        "",
        string
    )
    string = string.replace(" ", "-")
    return string


def to_uniq_path(string):
    slug = to_slug(string)
    hash = random_hash()
    return Path(f"{slug}-{hash}.subtext")


if __name__ == "__main__":
    args = parser.parse_args()
    src = Path("src")
    out = Path("out")
    out.mkdir(exist_ok=True)

    lines = list(read_content_lines(Path(src, args.src)))

    for content in generate_random_subtext_docs(lines, count=args.max):
        content_out_path = Path(out, to_uniq_path(content))
        write_file(content_out_path, content)