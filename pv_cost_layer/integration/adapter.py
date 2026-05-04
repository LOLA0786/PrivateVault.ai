from pv_cost_layer.integration.safe_integration import wrap_decision


def run_with_cost(decision_fn, context):
    wrapped = wrap_decision(decision_fn)
    return wrapped(context)
