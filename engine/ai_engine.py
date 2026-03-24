import json
import requests
from config import OLLAMA_URL, MODEL

def ask_v5_ai(prompt, as_json=False):
    payload = {
        "model": MODEL, 
        "prompt": prompt, 
        "stream": False,
        "options": {
            "num_ctx": 16384, 
            "temperature": 0.0,    # MUST BE ZERO to stop hallucinations
            "top_p": 0.1           # Extremely strict token selection 
        }
    }
    if as_json:
        payload["format"] = "json"

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=600)
        res.raise_for_status()
        response_text = res.json().get("response", "")
        if as_json:
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {} 
        return response_text
    except Exception as e:
        print(f"[!] AI Connection Error: {e}")
        return {} if as_json else None

def ai_graph_triage(files_graph):
    """
    Horizontally scales across massive codebases by chunking the AST dict into sizes of 50
    to prevent AI context overflow. Returns all viable logic targets across the entire repo.
    """
    summary_map = {}
    for f_path, graph in files_graph.items():
        if graph and "functions" in graph:
            summary_map[f_path] = list(graph["functions"].keys())
            
    items = list(summary_map.items())
    chunk_size = 50
    chunks = [dict(items[i:i + chunk_size]) for i in range(0, len(items), chunk_size)]
    
    all_priority_targets = []
    
    for idx, chunk in enumerate(chunks):
        print(f"    --> AI triaging codebase chunk {idx+1}/{len(chunks)}...")
        prompt = f"""
You are an elite Bug Bounty Hunter and Security Architect.
I am providing you a JSON map of a codebase architecture showing file paths and the functions/routes defined in them.
{json.dumps(chunk)}

Identify ONLY the specific files that are MOST likely to contain business logic vulnerabilities, IDORs, SSRF, RCE, or Injection flaws based on their name. 
If the chunk contains irrelevant files (e.g., config files, parsers, generic UI components), DO NOT INCLUDE THEM. 
Be extremely strict. It is better to return 0 targets than to return irrelevant files.

Return ONLY a valid JSON object with a key "targets" mapping to an array of file path strings representing the highest priority targets for deep analysis in this specific chunk.
"""
        response = ask_v5_ai(prompt, as_json=True)
        if isinstance(response, dict) and "targets" in response:
            valid = [t for t in response["targets"] if t in chunk]
            all_priority_targets.extend(valid)
            
    if not all_priority_targets and len(files_graph) < 20:
        return list(files_graph.keys())
        
    return list(set(all_priority_targets))

def analyze_bounty_target(context_payload):
    """
    Deep semantic bug bounty analysis on the cohesive context with extreme anti-hallucination.
    """
    prompt = f"""
You are an elite Application Security Engineer conducting a Bug Bounty on this application.
CRITICAL RULE: DO NOT HALLUCINATE. DO NOT MAKE UP VULNERABILITIES THAT DO NOT EXIST. 
IF YOU ARE NOT 100% CERTAIN A VULNERABILITY EXISTS AND IS EXPLOITABLE, YOU MUST RETURN EXACTLY: "No Critical Vulnerabilities Found."

I have extracted an execution path (the main file and its relevant dependencies):

{context_payload}

Analyze this execution path deeply for real, critical vulnerabilities (OWASP Top 10, IDOR, Injection, Bypasses, SSRF). 
You must pinpoint the exact line of code that is vulnerable. 

If you find an EXPLOITABLE bug, output exactly this format:
**VULNERABILITY ID**: [Type]
**DESCRIPTION**: [How it works]
**PROOF OF CONCEPT (POC)**: [Must include exact code snippet from context confirming the flaw]
**REMEDIATION**: [How to fix it]

If no critical vulnerabilities are found, return exactly: "No Critical Vulnerabilities Found."
"""
    return ask_v5_ai(prompt, as_json=False)

