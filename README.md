# Integration Intelligence — Composio Take-Home

A Python-based research prototype for evaluating how buildable third-party app integrations are for AI agents.

## Project Overview

This project explores 100 apps across 10 categories and investigates:

- Authentication methods
- Developer access models
- Public API availability
- MCP support
- Integration blockers and buildability

The goal is to identify which integrations appear easier to build and which require further investigation or external access.

## Research Pipeline

1. **Discover:** Search for developer documentation, API references, authentication guides and MCP documentation.
2. **Prioritize:** Rank candidate sources using documentation-related keywords and domain signals.
3. **Classify:** Compare source domains against known app domains.
4. **Verify:** Review source authority and relevance manually.
5. **Evaluate:** Compare a small manually reviewed sample against automated classifications.

## Technology Used

- Python
- CSV
- DuckDuckGo Search (DDGS)
- URL parsing
- HTML, CSS

## Project Structure

```text
composio-product-ops/
├── data/             # Input app list and source references
├── src/              # Research and evaluation scripts
├── reports/          # Research evidence and output CSV files
├── verification/     # Human review and evaluation
├── site/             # HTML case study
└── README.md
```

## How to Run

Run these commands from the project root:

```bash
py -m pip install ddgs
py src/main.py
py src/research_agent.py
py src/filter_evidence.py
py src/prepare_research_queue.py
py src/evaluate_verification.py
```

The scripts generate CSV files under `reports/` and `verification/`.

## Verification and Limitations

The initial manual review covered eight candidate records from Salesforce and HubSpot. Seven definite source-domain classifications agreed with the automated classification. This small sample is not a measure of overall research accuracy.

Official-domain matching does not establish that a source supports a particular integration claim. Human review is required to verify relevance and product capabilities.

Detailed structured research is currently complete only for Salesforce. The remaining apps require further verification. Search results and ranked links are research leads, not confirmed findings.

## Case Study

Open `site/index.html` in a browser to view the research case study.

## Future Improvements

- Complete structured research for all 100 apps.
- Expand verification across all categories.
- Compare first-pass and second-pass source quality.
- Add stronger source validation and claim-level evidence checks.
- Explore Composio SDK and MCP-based integration workflows.
