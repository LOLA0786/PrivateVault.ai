import json
from pathlib import Path


def export_snapshot(snapshot, output_file):

    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_file, "w") as f:
        json.dump(
            snapshot.__dict__,
            f,
            indent=2,
            default=str
        )

    return output_file


def load_snapshot(path):

    with open(path, "r") as f:
        return json.load(f)
