
import threading
from pv_runtime.execution_controller.controller import ExecutionController

# --- INIT CONTROLLER ---
controller = ExecutionController()
from pv_runtime.rollback.financial_rollback import rollback_transfer
controller.rollback_engine.register("transfer", rollback_transfer)


# --- RESET STATE (AFTER INIT) ---
controller.idempotency.reset()
controller.wallet.reset()
controller.graph.reset()


def test_idempotency():
    action = {"action": "transfer", "amount": 100, "recipient": "vendor_a"}

    r1 = controller.execute("finance_agent", action)
    r2 = controller.execute("finance_agent", action)

    print("\n[IDEMPOTENCY]")
    print("First:", r1)
    print("Second:", r2)


def test_wallet():
    controller.wallet.set_budget("finance_agent", 50)

    action = {"action": "transfer", "amount": 100}

    r = controller.execute("finance_agent", action)

    print("\n[WALLET]")
    print(r)


def test_locking():
    action = {"action": "transfer", "amount": 10}

    def run():
        print(controller.execute("finance_agent", action))

    print("\n[LOCKING]")
    t1 = threading.Thread(target=run)
    t2 = threading.Thread(target=run)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def test_event_store():
    action = {"action": "transfer", "amount": 20}

    controller.execute("finance_agent", action)

    print("\n[EVENT STORE]")
    with open("pv_events.log") as f:
        lines = f.readlines()
        print("Last Event:", lines[-1])


def test_context_graph():
    action = {"action": "transfer", "amount": 5}

    controller.execute("finance_agent", action)

    data = controller.graph.query("finance_agent")

    print("\n[CONTEXT GRAPH]")
    print(data[-1])


def test_rollback():
    controller.wallet.reset()
    controller.idempotency.reset()

    action = {"action": "transfer", "amount": 10, "fail": True}

    r = controller.execute("finance_agent", action)

    print("\n[REAL ROLLBACK]")
    print(r)


if __name__ == "__main__":
    test_idempotency()
    test_wallet()
    test_locking()
    test_event_store()
    test_context_graph()
    test_rollback()

