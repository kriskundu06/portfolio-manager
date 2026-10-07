# RL-based Portfolio Manager

An end-to-end RL-powered portfolio management system that uses **Reinforcement Learning (PPO)** to dynamically allocate capital across multiple asset classes.

The project was inspired by the research paper:

> **HARLF: Hierarchical Reinforcement Learning and Lightweight LLM-Driven Sentiment Integration for Financial Portfolio Optimization**

[Research Paper](https://arxiv.org/pdf/2507.18560)

The paper inspired the overall direction of this project, but the implementation, data pipeline, experiments, environment, backend and frontend were developed independently.

---

## 🚀 Live Demo

**[Open the Live Application](https://portfolio-manager-eight-nu.vercel.app/)**

---

## 📌 Project Overview

Traditional portfolio allocation strategies often rely on fixed rules such as equal weighting or manually optimized weights.

This project explores whether a **reinforcement learning agent can learn portfolio allocation decisions from historical market data**.

The system:

1. Collects historical market data
2. Engineers financial features
3. Builds a custom Gymnasium portfolio environment
4. Trains a PPO agent
5. Generates portfolio allocations
6. Backtests the learned strategy
7. Calculates risk and performance metrics
8. Compares different model variants
9. Exposes the results through a FastAPI backend
10. Visualizes the results through a React dashboard

### Architecture

```text
                    Historical Market Data
                              │
                              ▼
                    ┌──────────────────┐
                    │ Feature Engineering │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Gymnasium        │
                    │ Portfolio Env    │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ PPO Agent        │
                    │ Stable-Baselines3│
                    └─────────┬────────┘
                              │
                              ▼
                    Portfolio Weights
                              │
                              ▼
                    ┌──────────────────┐
                    │ Backtesting      │
                    └─────────┬────────┘
                              │
                              ▼
              ┌────────────────────────────┐
              │ Performance & Risk Metrics│
              └─────────────┬──────────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │ FastAPI Backend  │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ React Dashboard  │
                    └──────────────────┘
