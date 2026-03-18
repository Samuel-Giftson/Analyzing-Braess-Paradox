# Network Optimization & Braess Paradox Analysis

A simulation-driven system that analyzes network performance and predicts when increasing connectivity can reduce overall efficiency.

---

## Overview

In many real-world systems, adding more capacity does not always improve performance.  
In certain conditions, it can lead to worse outcomes due to decentralized decision-making.

This phenomenon, known as the **Braess Paradox**, appears in:
- Transportation systems
- Network routing
- Power grids
- Distributed and multi-agent systems

This project addresses the problem by combining simulation and machine learning to identify inefficient network configurations.

---

## What This System Does

- Simulates network behavior using autonomous agents (selfish routing)
- Evaluates performance as edges are added to the network
- Detects when additional connections reduce efficiency
- Generates structured data from simulations
- Trains a Graph Neural Network (GNN) to predict inefficient network designs

---

## Architecture

### Components

- **Graph Generator**
  - Produces directed, weighted, scale-free networks
  - Reflects real-world topology patterns

- **Simulation Engine**
  - Agents independently choose optimal paths
  - Measures system-wide performance under changing conditions

- **Data Pipeline**
  - Captures graph states and outcomes
  - Builds datasets for training

- **GNN Model**
  - Learns structural patterns in graphs
  - Predicts likelihood of Braess Paradox occurrence

---

## Key Contribution

This project introduces a **simulation-driven data generation framework** for studying the Braess Paradox.

While most existing approaches focus on analytical or fixed-network scenarios, this system:
- Programmatically generates diverse network conditions  
- Simulates agent behavior at scale  
- Produces data suitable for machine learning models  

---

## Key Outcomes

- Identified conditions where increasing connectivity leads to reduced efficiency  
- Built a scalable simulation framework for network analysis  
- Generated datasets for training graph-based models  
- Developed a predictive model for identifying high-risk network structures  

---

## Business Value

This approach can support decision-making in:

- Traffic system design — avoid infrastructure changes that worsen congestion  
- Network routing — improve efficiency in distributed systems  
- Power grid expansion — reduce risk in infrastructure scaling  
- Multi-agent systems — understand behavior under decentralized control  

---

## Technologies

- Python  
- Network simulation (custom-built engine)  
- Graph modeling  
- Machine Learning (Graph Neural Networks)  
- Data processing and analysis  

---

## Future Enhancements

- Real-time simulation with dynamic inputs  
- Integration with real-world datasets  
- Reinforcement learning for adaptive routing strategies  
- Scaling experiments to larger graph sizes  

---

## Research Basis

This project is based on a research study exploring the relationship between network topology and the occurrence of the Braess Paradox, with a focus on simulation-driven analysis and predictive modeling.

---

## Author

Samuel Prabhakar  
M.S. Computer Science  

---

## Summary

This project demonstrates how simulation and machine learning can be combined to detect non-intuitive inefficiencies in complex networks, enabling better design decisions in real-world systems.

# Analyzing-Braess-Paradox
This program was developed to support the research presented in the thesis "Exploring the Relationship Between Network Topology and Braess' Paradox" (2024), available via Mississippi State University Theses and Dissertations, No. 6160.
