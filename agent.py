import json
import time
import requests
from openai import OpenAI

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1"

# Connect to local LM Studio instance
client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")


# -------------------------------------------------------------------
# 1. FETCH LATEST ACTIVE JOBS
# -------------------------------------------------------------------
def fetch_latest_projects(limit=15):
    """Fetches active public projects from Freelancer."""
    url = "https://www.freelancer.com/api/projects/0.1/projects/active/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    params = {
        "limit": limit,
        "full_description": "true"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("result", {}).get("projects", [])
        return []
    except Exception as e:
        print(f"[!] Error fetching projects: {e}")
        return []


# -------------------------------------------------------------------
# 2. EVALUATE & GENERATE DELIVERABLE
# -------------------------------------------------------------------
def evaluate_and_generate_deliverable(project):
    title = project.get("title", "")
    description = project.get("description", "")

    prompt = f"""
    You are an automated freelance worker. Analyze this project:

    Title: {title}
    Description: {description}

    Task:
    1. Is this job a simple text, copywriting, basic script, or data formatting task that can be 100% completed immediately by an AI with NO human work? (is_doable: true/false)
    2. Provide a 1-sentence reason.
    3. If doable, write a pitch proposal (under 80 words) AND the complete finished deliverable.

    Respond ONLY in raw JSON matching this format:
    {{
      "is_doable": false,
      "reason": "Brief reason why",
      "proposal": "",
      "deliverable": ""
    }}
    """

    try:
        response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        raw_text = response.choices[0].message.content.strip()

        # Clean JSON markdown backticks if present
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        # strict=False handles raw newlines inside generated code strings
        return json.loads(raw_text, strict=False)
    except Exception as e:
        print(f"[!] LLM parsing error: {e}")
        return None


# -------------------------------------------------------------------
# MAIN EXECUTION (CONTINUOUS SCANNER)
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("[*] Starting Continuous AI Freelance Scanner...")
    print("[*] Monitoring Freelancer.com for instant AI-completable jobs...\n")

    seen_projects = set()

    while True:
        print("[*] Checking for new project listings...")
        projects = fetch_latest_projects(limit=15)

        for proj in projects:
            proj_id = proj.get("id")
            
            # Skip projects already evaluated in previous loops
            if proj_id in seen_projects:
                continue
            seen_projects.add(proj_id)

            title = proj.get("title")
            seo_url = proj.get("seo_url", "")
            link = f"https://www.freelancer.com/projects/{seo_url}" if seo_url else f"https://www.freelancer.com/projects/{proj_id}"

            print(f"\nEvaluating: {title}")

            eval_result = evaluate_and_generate_deliverable(proj)
            if not eval_result:
                continue

            if eval_result.get("is_doable"):
                print(f"\n==================================================")
                print(f"[MATCH FOUND] {title}")
                print(f"Reason: {eval_result.get('reason')}")
                print(f"Direct Link: {link}")
                print("\n--- PROPOSAL PITCH ---")
                print(eval_result.get("proposal"))
                print("\n--- FINISHED DELIVERABLE ---")
                print(eval_result.get("deliverable"))
                print("==================================================\n")
            else:
                reason = eval_result.get('reason') or "Not an instant AI task"
                print(f"[SKIP] -> {reason}")

            time.sleep(1)

        print("\n[*] Batch complete. Waiting 60 seconds before next scan...\n")
        time.sleep(60)