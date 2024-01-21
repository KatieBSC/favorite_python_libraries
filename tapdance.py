"""Tap Dance Combination Generator

Usage:
  tapdance.py [--file=<path>] [--bpm=<int>] [--measures=<int>]
  tapdance.py --help

Options:
  -h, --help        Show this screen.
  --file=<path>     Input csv file [default: ./data/tap_steps.txt].
  --bpm=<int>       Beats per measure.
                    Supports simple time signatures.
                    1 < beats < 5 [default: 4].
  --measures=<int>  Total measures.
                    0 < measures < 33 [default: 4].
"""

import os
import csv
from random import choice
from docopt import docopt
from schema import Schema, And, Const, Use, SchemaError
from attrs import frozen, field, validators


@frozen
class TapStep:
    """Tap dance step.

    Attributes:
        name:   Name of the step.
        sounds: Number of sounds in the step.

    Raises:
        ValueError: If length of `name` is less than 1.
        ValueError: If `sounds` is greater than 4 or less than 1.

    """

    name: str = field(validator=validators.min_len(1))
    sounds: int = field(converter=int, validator=[validators.ge(1), validators.le(4)])

    @classmethod
    def from_row(cls, row):
        """
        Initialize a `TapStep` from a row
        object with `name` and `sounds` keys.
        """
        return cls(row["name"], row["sounds"])


def get_steps(file: str | os.PathLike) -> list[TapStep]:
    """Get `TapStep`s from a file.

    Args:
        file: csv file with `name` and `sounds` columns.

    Returns:
        A list of `TapStep`s corresponding to each row in the file.
    """
    with open(file, "r") as csvfile:
        return [TapStep.from_row(row) for row in csv.DictReader(csvfile)]


def get_combination(steps: list[TapStep], bpm: int, measures: int) -> str:
    """Get a tap dance combination.

    Generate a random, with replacement, string of
    tap dance step names over a given number of measures.

    Args:
        steps: List of `TapStep` objects.
        bpm: Beats per measure.
        measures: Total measures.

    Returns:
        String of `TapStep` names with pipe ("|") measure breaks.
    """
    combination = []

    while measures > 0:
        rest_beats = bpm
        possible_steps = [x for x in steps if x.sounds <= rest_beats]
        while rest_beats > 0 and possible_steps:
            step = choice(possible_steps)
            combination.append(step.name)
            rest_beats -= step.sounds
            possible_steps = [x for x in possible_steps if x.sounds <= rest_beats]
        combination.append("|")  # Measure break
        measures -= 1
    return " ".join(combination)


if __name__ == "__main__":
    args = docopt(__doc__)

    args_schema = Schema(
        {
            "--file": Const(Use(open, error="--file=<path> should be readable")),
            "--bpm": And(
                Use(int),
                lambda n: 1 < n < 5,
                error="--bpm=N should be integer 1 < N < 5",
            ),
            "--measures": And(
                Use(int),
                lambda n: 0 < n < 33,
                error="--measures=N should be integer 0 < N < 33",
            ),
            object: object,
        }
    )

    try:
        args = args_schema.validate(args)
    except SchemaError as error:
        exit(error)

    steps = get_steps(args["--file"])

    combination = get_combination(steps, args["--bpm"], args["--measures"])

    print(combination)
