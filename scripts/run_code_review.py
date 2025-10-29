import os
import requests
import subprocess
from openai import OpenAI

# Environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

if not GITHUB_TOKEN or not REPO or not PR_NUMBER:
    raise ValueError("Missing environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, or PR_NUMBER.")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    pr_info = requests.get(url, headers=headers).json()
    diff_url = pr_info["diff_url"]
    diff = requests.get(diff_url, headers=headers).text
    return diff

def generate_review(diff):
    prompt = f"""
You are an experienced software reviewer.
Analyze this GitHub Pull Request diff for:
1. Bugs or incorrect logic
2. Security vulnerabilities
3. Code style violations
4. Suggestions for improvement
Be concise and structured.

Diff:
{diff[:12000]}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an AI code reviewer."},
                  {"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content

def post_comment(review_text):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {"body": f"### 🤖 AI Code Review Feedback\n\n{review_text}"}
    r = requests.post(url, headers=headers, json=data)
    return r.status_code

if __name__ == "__main__":
    diff = get_pr_diff()
    review = generate_review(diff)
    status = post_comment(review)
    print(f"Posted review to PR #{PR_NUMBER} (status: {status})")
