# Latency Budget

Target:

< 8 ms

Budget:

Trust Evaluation      1 ms
Consensus             2 ms
Economics             1 ms
Routing               1 ms
Evidence              1 ms
Safety Margin         2 ms

Forbidden:

- Database calls
- OPA round trips
- LLM calls
- Remote policy fetches

inside execution path.
