import json


def build_dashboard(report):

    return json.dumps(
        report.__dict__,
        indent=2
    )
