# 🔮 DERIEN — AI-Powered Social Media Intelligence System

**DERIEN** is an AI-driven cyber-intelligence system that detects, analyzes, and maps
drug trafficking activity on social media platforms by identifying suspicious
content, behavioural patterns, and hidden user networks—without
requiring access to private data. This program uses an open-source
intelligence (OSINT) + AI + cybersecurity analytics software system

---

## Important Links

### Project Documentation : https://drive.google.com/file/d/10AzbItR8efoaPOXTDutlfo-xH1M64j6E/view?usp=sharing
### Explanatory Video : https://drive.google.com/file/d/1xMvFS1wtvztRoVzkH3KXITYcqvm1J498/view?usp=drive_link
### Demonstration Video : https://drive.google.com/file/d/12tJgK_okhVvyiP5FwK9CNbfk4V2cByLL/view?usp=drive_link

---

## ✨ Key Capabilities

### 🔍 Multi-Signal Intelligence
* **Content analysis:** Keywords, slang, and risk indicators.
* **Behavioral analysis:** Posting frequency and anomalies.
* **Network analysis:** Interaction graphs, hubs, and clusters.

### 📊 Explainable Risk Scoring
* **Normalized signals:** Using z-score and sigmoid functions.
* **Weighted aggregation:** Confidence scoring to reflect signal completeness.
* **Percentile-based risk levels:** Adaptive and low-noise.
* **Transparency:** Detailed explainability at both the post and user level.

### 🌐 Network Intelligence
* **Interactive user network graph:** Powered by `vis-network`.
* **Risk-based node sizing & coloring:** Visual priority for high-risk entities.
* **Cluster highlighting:** 1-hop neighborhood analysis.
* **Deep-dive investigations:** Click-through functionality for detailed user views.

### 🧠 Analyst-Grade Dashboard
* **Live system health:** Boot sequence monitoring.
* **High-risk overview:** Tables and cards for users and posts.
* **Full investigation view:** Multi-tab interface (Overview, Posts, Network, Explainability).

---

## 🏗️ System Architecture

DERIEN utilizes a modular intelligence pipeline to process and visualize risk data.

│ PostgreSQL |  ───▶ | Backend |  ───▶ │ FastAPI | ───▶ | Frontend │ 

### **Frontend**
* **React (Vite):** Fast, modern development.
* **Dark UI:** Motion-polished interface designed for long investigation sessions.
* **Visualizations:** `vis-network` for interactive graph intelligence.

### **Backend**
* **FastAPI:** High-performance asynchronous processing.
* **PostgreSQL:** Relational database for intelligence storage.
* **Modular Pipeline:** Clean separation of intelligence logic.

---

## 🧠 Intelligence Scoring Pipeline

The platform utilizes a three-stage scoring model to ensure accuracy and context.

### **H1 — Signal Normalization**
Each signal is normalized to prevent scale dominance:
$$z\text{-score} \to \text{sigmoid} \to [0, 1]$$

### **H2 — Weighted Aggregation + Confidence**
Scores are combined based on thematic importance:
$$\text{Total Score} = (0.4 \times \text{Content}) + (0.3 \times \text{Behaviour}) + (0.3 \times \text{Network})$$

### **H3 — Percentile-Based Risk Levels**
Risk is determined relative to the total population to ensure adaptive classification:

| Population Percentile | Risk Level |
| :--- | :--- |
| Top 5% | **High** |
| Next 15% | **Medium** |
| Remaining 80% | **Low** |

---

## 🚀 API Highlights

| Endpoint | Description |
| :--- | :--- |
| `GET /health` | System health check |
| `GET /users/high-risk` | High-risk user list |
| `GET /posts/high-risk` | High-risk posts overview |
| `GET /posts/{id}/explain` | Post-level explainability |
| `GET /network/graph` | Network graph data |
| `GET /users/{id}/detail` | Full user investigation data |

---

## 📌 Design Philosophy

* **Explainability > Raw Scores:** Insights must be actionable and understandable.
* **Relative Risk > Static Thresholds:** Risk is defined by the environment, not arbitrary numbers.
* **Context > Isolated Signals:** Relationships matter as much as individual actions.
* **Analyst Workflow > Flashy UI:** Focused on efficiency and reducing cognitive load.

---

## 🗺️ Roadmap

* [ ] **Dockerized deployment:** Simplified environment setup.
* [ ] **Temporal network analysis:** Tracking changes in risk over time.
* [ ] **Community detection:** Louvain/Leiden algorithm integration.
* [ ] **Timeline-based investigations:** Visual history of user activity.
* [ ] **Analyst notes:** Integrated case tracking system.

---
**Author:** Built as an individual systems project focused on applied intelligence engineering, full-stack architecture, and explainable risk systems.
