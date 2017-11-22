"""Provide base options for processes"""
import argparse, os
from .settings import PERSONAL_DATASET_DIR

def get_options(description):
    DEFAULT_DATASET_DIR = os.path.expanduser(PERSONAL_DATASET_DIR)
    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument(
        '-d', '--directory',
        default=DEFAULT_DATASET_DIR,
        help="""Directory for storing datasets, default: %s""" % (
            DEFAULT_DATASET_DIR,)
    )
    parser.add_argument(
        '-c', '--corpus',
        choices=[
            'tedlium',
            'vctk',
            'librispeech',
            'speechcommands'
        ],
        action='append',
        default=[],
        help="Specify particular corpora (repeat option to specify multiple), default: all"
    )
    return parser
