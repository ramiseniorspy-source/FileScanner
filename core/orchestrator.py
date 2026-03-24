import os
from engine.ingestion import clone_or_setup_repo
from engine.ast_parser import analyze_file_ast
from engine.context_builder import build_execution_context
from engine.ai_engine import ai_graph_triage, analyze_bounty_target
from config import MAX_THREADS

def _collect_all(base_path):
    # Fast collector targeting only code files for bug bounty context
    collected = []
    
    # Extensions that actually contain logic, routes, and business flow
    CODE_EXT = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.php', '.go', 
        '.rb', '.java', '.cs', '.c', '.cpp', '.h', '.hpp'
    }
    
    for root, _, files in os.walk(base_path):
        if any(ignored in root for ignored in ['.git', 'node_modules', 'venv', 'build', 'dist', 'vendor']):
            continue
        for f in files:
            # We only want to AST map files that act as logic nodes
            if any(f.endswith(ext) for ext in CODE_EXT):
                collected.append(os.path.join(root, f))
    return collected

def run_v5_scan(target_path, mode="bounty"):
    print(f"\n[🚀] Starting Scanner V5 (AST Bug Bounty Engine) | Target: {target_path}")
    
    repo_path = clone_or_setup_repo(target_path)
    if not repo_path:
        return
        
    files = _collect_all(repo_path)
    print(f"[+] Repository Indexed: {len(files)} source files.")
    
    print("[+] 🌲 Building Abstract Syntax Trees and Dependency Graphs...")
    # Map file path -> AST Dictionary (Imports, Functions)
    files_graph = {}
    for f in files:
        graph = analyze_file_ast(f)
        if graph and (graph.get("imports") or graph.get("functions")):
            files_graph[f] = graph
            
    print(f"[+] Graph built containing {len(files_graph)} active logic nodes.")
    
    print("[+] 🤖 Asking Qwen to structurally triage the codebase chunks for Bug Bounty Targets...")
    priority_targets = ai_graph_triage(files_graph)
    print(f"[!] Target Acquired: {len(priority_targets)} critical execution paths mapped for deep scan.")
    
    report_file = "bounty_report.md"
    with open(report_file, "w", encoding="utf-8") as rf:
        rf.write("# 🏴‍☠️ Scanner V5 Bug Bounty Report\n\n")
        
        for target in priority_targets:
            print(f"    -> Assembling execution context for {target}...")
            context = build_execution_context(target, files_graph.get(target), files_graph)
            
            print(f"    -> Running Deep Semantic AI Analysis...")
            analysis_result = analyze_bounty_target(context)
            
            if analysis_result and "No Critical Vulnerabilities Found" not in analysis_result:
                print(f"    [🔥] VULNERABILITY FOUND in {target}!")
                rf.write(f"## Target Vector: `{target}`\n\n")
                rf.write(f"{analysis_result}\n\n---\n\n")
            else:
                print(f"    [-] Target {target} is clean.")
                
    print(f"\n[+] Scan Complete. Detailed findings written to {report_file}")
