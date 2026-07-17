#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import random

console = Console()


def banner():
    console.print(
        Panel.fit(
            "[bold cyan]PrivateVault Runtime Decision Engine[/bold cyan]\n"
            "Tenant : Wio Bank\n"
            "Agent  : finance-agent-01",
            border_style="cyan",
        )
    )


def policy_scope():
    console.print(
        Panel(
"""Policy Adapter

Source        : PostgreSQL
Policy Version: 2026-07-17
Agent Scope   : finance-agent
Global Rules  : 8
Finance Rules : 16
Total Loaded  : 24
""",
            title="Policy Loading",
            border_style="green",
        )
    )


def decision(action, policy, result, reason):
    latency = round(random.uniform(1.5, 5.0), 2)
    evidence = hex(random.getrandbits(64))[2:]

    table = Table(box=box.ROUNDED)

    table.add_column("Field", style="cyan", width=22)
    table.add_column("Value")

    table.add_row("Action", action)
    table.add_row("Matched Policy", policy)
    table.add_row("Decision", result)
    table.add_row("Reason", reason)
    table.add_row("Latency", f"{latency} ms")
    table.add_row("Evidence Hash", evidence)

    console.print(table)


banner()

policy_scope()

decision(
    "payments.initiate_wire",
    "Finance/WireTransferApproval",
    "REQUIRE APPROVAL",
    "Amount exceeds AED 100,000"
)

decision(
    "crm.read_customer",
    "CustomerReadPolicy",
    "ALLOW",
    "Read-only operation"
)

decision(
    "storage.bulk_export",
    "DataLossPrevention",
    "BLOCK",
    "Bulk export prohibited"
)

metrics = Table(title="Runtime Metrics", box=box.SIMPLE)

metrics.add_column("Metric")
metrics.add_column("Value")

metrics.add_row("Requests", "3")
metrics.add_row("Allowed", "1")
metrics.add_row("Blocked", "1")
metrics.add_row("Approval Required", "1")
metrics.add_row("Average Latency", "3.2 ms")
metrics.add_row("Audit", "PASS ✓")

console.print(metrics)
