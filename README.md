# Autonomous Local AI Job Scouting Agent

An automated Python agent that continuously monitors active public project listings from Freelancer.com and leverages a local LLM via LM Studio to evaluate project requirements and draft custom bid proposals in real time.

## Features
- **Zero API Costs:** Connects to a local LLM server powered by LM Studio.
- **Continuous Polling:** Scans unauthenticated active public project endpoints on Freelancer.com.
- **Smart Evaluation:** Analyzes project requirements for feasibility and generates structured JSON outputs.
- **Deduplication:** Tracks previously evaluated job IDs to avoid duplicate processing.

## Tech Stack
- **Language:** Python 3.13+
- **Libraries:** `openai`, `requests`
- **Local Inference:** LM Studio (OpenAI API Compatible Endpoint)

## Setup & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Set up virtual environment and install dependencies:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```

3. **Ensure LM Studio is running:**
   Start your local server in LM Studio on `http://localhost:1234/v1`.

4. **Run the agent:**
   ```powershell
   python agent.py
   ```

NOTE: All of this was made out of curiosity and a drive to learn how AI Agents work and runnning them localy.