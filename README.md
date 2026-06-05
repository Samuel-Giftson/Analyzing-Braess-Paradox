# Exploring the Relationship Between Network Topology and the Braess Paradox

**M.S. Thesis — Samuel Giftson Prabhakar**
**Mississippi State University, Department of Computer Science and Engineering**
**March 2024 | Advisor: Dr. Zhiqian Chen**

> Published thesis available via Mississippi State University Theses and Dissertations, No. 6160.

---

## The Problem

Traffic congestion in the United States costs **$94.6 billion per year** (2021) and is projected to exceed **$120 billion** annually. The instinctive engineering response — build more roads, add more connections — does not always help. In fact, under specific conditions, adding a new road to a network can make travel times *worse for everyone*.

This phenomenon is known as the **Braess Paradox**, and it has been observed in real-world systems:
- Stuttgart, Germany — closing a central road *reduced* city-wide travel time
- Seoul, South Korea — removing an elevated highway *improved* traffic flow
- New York City — closing Broadway to vehicles improved surrounding traffic patterns

The paradox arises from **decentralized, selfish decision-making**: when every traveler independently picks the route that seems best for them, the collective outcome can be suboptimal. Understanding *when* and *why* this happens requires studying the relationship between network structure and agent behavior — which is exactly what this project addresses.

---

## What This Research Does

This project investigates: **at what point in a network's growth does the Braess Paradox appear, and can a machine learning model predict it?**

The approach is empirical rather than purely analytical — most prior work on the Braess Paradox relies on fixed, hand-crafted networks. This system instead:

1. **Programmatically generates** diverse directed weighted scale-free networks (reflecting real-world topology patterns like road systems and power grids)
2. **Grows each network incrementally** from a base scale-free structure toward a complete graph, adding edges one at a time
3. **Simulates 100 autonomous agents (bots)** traversing the network at each growth stage, each independently selecting their optimal path
4. **Detects the Braess Paradox** by measuring whether average travel time *increases* as new edges are added
5. **Trains a Graph Neural Network (GNN)** on the resulting dataset to predict which graph configurations are at risk of triggering the paradox

---

## Simulation Design

Each simulation is far more than a simple routing exercise. It layers two interacting models:

### Agent Routing (Selfish Path Selection)
- 100 bots are placed on a directed weighted graph, each with a random source and destination
- Each bot independently selects its shortest available path (simulating selfish routing behavior)
- Bots move epoch by epoch; edge weights update dynamically based on congestion (number of bots currently traversing the edge)
- Travel time is recorded per bot per simulation; average travel time across all bots is the key metric

### Influence Maximization via Linear Threshold Model
- A secondary social network (scale-free bot network) models how routing *information* spreads between agents
- The Linear Threshold Model propagates influence across this network until 70% of bots adopt updated routing knowledge
- This captures how real-world travelers adapt their behavior based on information from others (navigation apps, word of mouth, etc.)

### Graph Growth Spectrum
- Each simulation does not test a single graph — it tests the **full spectrum** of graph states, from the initial scale-free topology up to a directed weighted complete graph
- At each incremental edge addition, the full simulation (100 bots × multiple epochs) is re-run
- This produces a curve of average travel time vs. number of edges — the Braess Paradox appears as an *increase* in that curve after a new edge is added

### Computational Scale
Each top-level simulation involves:
- ~40,000+ individual agent-level operations (bot movements, path recalculations, edge weight updates)
- ~35,000 edge propagation operations from the Linear Threshold Model
- Repeated across the full graph growth spectrum (multiple edge-addition stages)

The cumulative dataset already contains **4.3 million+ recorded simulation states**, representing hundreds of billions of individual agent decisions — providing statistically robust grounding for the findings.

---

## Key Findings

Experiments were conducted across graph sizes of **8, 9, 10, and 11 nodes**, each tested with 100 bots:

- The Braess Paradox was **consistently observed** as graphs grew from scale-free toward complete
- The paradox tends to emerge at a **specific density threshold** — not at the beginning or end of graph growth, but at an intermediate point
- Larger graphs (more nodes) produced **more frequent and more pronounced** Braess Paradox occurrences
- A **real-world test case** using the Mississippi State University campus road network (Starkville, MS) confirmed the findings extend beyond synthetic graphs
- The trained **Graph Neural Network** successfully learned to identify structural features associated with paradox-triggering configurations

---

## System Architecture

```
graph_generator1.py          — Directed weighted scale-free graph generation and edge-by-edge growth
simulation_starter.py        — Core simulation engine: bot routing, path assignment, travel time tracking
bot_class.py                 — Individual agent (bot) representation
linear_threshold_model.py    — Information spread model across the bot social network
initialize_csv_file.py       — Data pipeline: structured storage of simulation results
Braess_detector_based_on_data.py — GNN training and Braess Paradox prediction
analyzing_results.py         — Post-simulation statistical analysis and visualization
starkville_graph.py          — Real-world MSU campus road network test case
main.py                      — Entry point: runs simulation trials
```

---

## Technologies

| Component | Technology |
|---|---|
| Language | Python 3 |
| Graph modeling & algorithms | NetworkX |
| Agent simulation | Custom-built multi-agent engine |
| Social influence model | Linear Threshold Model (custom implementation) |
| Data pipeline | pandas, CSV |
| Machine learning | PyTorch, Graph Neural Networks (GNN) |
| Graph topology | Scale-free networks (Barabási–Albert model) |
| Real-world data | Mississippi State University campus road network |

---

## How to Run

```bash
# Run simulation trials
python main.py

# Analyze results
python analyzing_results.py

# Train GNN on generated data
python Braess_detector_based_on_data.py
```

Simulation output is stored as CSV and used as input for the GNN training pipeline.

---

## Research Significance

This project makes the following contributions:

1. **Empirical methodology**: Unlike most Braess Paradox research which uses fixed analytical networks, this system generates and tests thousands of diverse network configurations programmatically
2. **Scale-free focus**: Real-world infrastructure networks (roads, internet, power grids) follow scale-free topology — this work specifically studies the paradox within that context
3. **Dual-model simulation**: The combination of selfish routing with a social influence layer (Linear Threshold Model) adds a layer of behavioral realism not present in classical Braess analyses
4. **ML-driven prediction**: The GNN provides a practical tool for identifying at-risk network designs *before* infrastructure is built, with direct implications for urban planning and network engineering
5. **Real-world validation**: Findings were validated on an actual road network, not just synthetic graphs

---

## Applications

This framework and its findings have direct relevance to:

- **Transportation planning** — identify which road additions will worsen congestion before breaking ground
- **Internet routing** — detect configurations where added bandwidth paradoxically reduces throughput
- **Power grid design** — avoid infrastructure expansions that increase system-wide energy loss
- **Multi-agent systems** — understand emergent inefficiency in any system where agents make independent, selfish decisions

---

## Future Work

- Scaling experiments to larger graph sizes (15+ nodes) via parallelization
- Integration with real-time traffic data feeds
- Reinforcement learning for cooperative (non-selfish) routing strategies that avoid paradox conditions
- Extension to dynamic graphs where edge weights change over time

---

## Citation

Prabhakar, Samuel Giftson. *Exploring the Relationship Between Network Topology and Braess' Paradox*. M.S. Thesis, Mississippi State University, 2024. Mississippi State University Theses and Dissertations, No. 6160.

---

## Author

**Samuel Giftson Prabhakar**
M.S. Computer Science — Mississippi State University
Major Professor: Dr. Zhiqian Chen
Committee: Dr. Jingdao Chen, Dr. Vaidyanathan Sivaraman, Dr. Snehalatha Ballamoole
