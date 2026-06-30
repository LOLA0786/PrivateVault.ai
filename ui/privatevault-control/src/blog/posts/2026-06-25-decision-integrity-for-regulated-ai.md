---
title: Decision Integrity for Regulated AI
date: 2026-06-25
excerpt: Securing the model is not the same as proving the decision. In a regulated industry, only one of those holds up.
---

The agentic AI safety conversation is aimed one layer too high.

Walk the field today and you find a hundred companies securing the model and the agent. Prompt injection defense, identity and least-privilege, runtime firewalls, red teaming, observability. All of it necessary. None of it answers the question a regulated institution actually has to answer.

When an AI agent denies someone a loan, rejects an insurance claim, or blocks a payment, the question is not whether the model was safe. The question is whether you can prove that this specific decision was authorized, that it stayed inside policy, and that it can be reconstructed. For an auditor. For a regulator. Eventually, for a court.

"The model was 97 percent aligned" is not an answer. It is an average. Regulators do not accept averages, and neither do the people whose lives the decision touched.

## Probabilistic safety is a liability wearing the word safety

Model safety is probabilistic by construction. You can lower the odds of a bad action. You cannot prove that a particular action was correct, bounded, and accountable. For a consumer chatbot, probabilistic is fine. For a consequential decision in a regulated industry, probabilistic is a liability that someone has labeled as protection.

The control boundary that matters is not where the model reasons. It is where the decision executes.

## What decision integrity actually requires

I call the missing layer decision integrity. It is a different requirement from security, and it answers to a different buyer. Security asks whether the agent is authenticated and whether it is under attack. Decision integrity asks whether this decision was allowed to happen, and whether you can prove why.

A regulated decision needs four things the model layer cannot give it.

Deterministic authorization before the action executes. A clear allow, review, or block at the moment of the decision, not a probability assigned afterward.

An immutable record that ties each action to the intent and the policy that authorized it. Tamper-evident, so the version you show a regulator in March is provably the one that existed in January.

Reconstruction on demand. The ability to replay any decision exactly as it happened, not a log you hope is complete.

Enforcement on outcomes, not only on steps. An agent can take ten individually permitted actions that add up to one prohibited result, and step-level checks will wave all ten through.

None of those are model problems. They are enforcement problems, and they live at the execution layer, below where almost all of today's tooling operates.

## The market is building for the wrong buyer

The reason the field keeps building the other thing is that it is built by security people, for security people. The crowded agent security landscape sells to the CISO and the SOC.

But the person who loses sleep over an automated credit decision is not the CISO. It is the Chief Risk Officer, the Head of Compliance, and the executive who has to sit across a table from a regulator and explain a pattern of denials. They do not need the agent secured. They need the decision proven. That is a different product, a different buyer, and right now a mostly empty space, because decision evidence for a regulator is far less exciting to build than blocking a prompt injection.

## This stops being philosophy in August

The EU AI Act high-risk obligations, including the record-keeping requirements in Article 12, land in August 2026. Credit scoring and a range of financial decisions sit squarely in scope. Fair-lending law in the United States already requires explainable, defensible adverse-action decisions. SR 11-7 governs model risk. India's RBI is tightening digital-lending accountability. The common thread across all of them is that "trust us, the model is fair" is being replaced, in law, by "show the record."

The moment the requirement becomes show the record, every institution running AI into regulated decisions discovers that it has been generating decisions it cannot fully reconstruct. That is the gap. That is the bill coming due.

## The bet

So here is the bet. Model safety and decision integrity are different layers. The second one, deterministic and pre-execution and built to produce regulator-grade evidence for consequential decisions, is the one regulated industries will be forced to buy, and the one almost nobody is building for the right buyer.

If you own risk or compliance at a lender, an insurer, or a bank, and you are putting AI into decisions a regulator can question, I would like to compare notes on what proving the decision actually has to look like. That conversation is worth having before August, not after.

The model tells you what the agent might do. The decision record proves what it did, and why it was allowed to. In a regulated industry, only one of those holds up.
