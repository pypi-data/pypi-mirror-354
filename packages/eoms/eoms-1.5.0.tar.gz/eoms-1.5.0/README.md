# EOMS
# 🚀 Quant‑EOMS

A modular Execution & Order Management System built for systematic trading desks.  
*Broker‑agnostic · Datafeed‑agnostic · GUI‑centric.*

## Features
| Module | Purpose |
|--------|---------|
| **Dashboard** | At‑a‑glance PNL, risk, latency stats |
| **Order Ticket** | Live quotes + smart routing |
| **Positions Mgr** | Real‑time net positions & exposures |
| **Order Mgr** | State machine for every order, amend/cancel |
| **Algo Mgr** | Load/run param‑driven algos |
| **PNL Window** | Tick‑level & aggregated PNL |

## Quick Start
```bash
git clone https://github.com/your‑org/quant‑eoms.git
cd quant‑eoms
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn quanteoms.api:app --reload   # optional REST gateway
python -m quanteoms.gui              # launch dashboard
```
## Architecture
```lua
                   +------------------+
   Market Data --> | DataFeed Plugin* |---+
                   +------------------+   |
                                           v
+-----------+    events     +------------------+
|  Brokers* | <-----------> | Event Bus (async)|
+-----------+               +------------------+
           ^                       |
           |                       v
           |               +---------------+
           +---------------| GUI Modules   |
                           +---------------+
(* = pluggable via entry_points)
```

## Adding a New Plugin
```bash
Create package quanteoms_<provider> implementing BrokerBase or FeedBase.
```

Add to setup.py:

```python
entry_points={
    "quanteoms.brokers": ["<name>=quanteoms_<provider>.broker:Broker"],
}
pip install -e . – the system auto‑discovers it.
```

## Roadmap
See TASKS.MD.
