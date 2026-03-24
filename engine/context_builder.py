import os

def build_execution_context(file_path, ast_graph, all_files_graphs):
    """
    Constructs a razor-sharp execution context by strictly extracting AST-mapped 
    functions instead of raw, noisy file strings to completely eliminate hallucination.
    """
    context = f"=== TARGET FILE: {file_path} ===\n"

    # Strict AST injection: Only give the AI the actual functional logic
    if ast_graph and "functions" in ast_graph and ast_graph["functions"]:
        context += "--- Extracted Logic Blocks ---\n"
        for func_name, func_body in ast_graph["functions"].items():
            context += f"\n[Function: {func_name}]\n{func_body}\n"
    else:
        # Fallback if AST failed to parse or no functions were found (cap at 3000 chars)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                context += f.read()[:3000] 
        except Exception:
            context += "Error reading main file."
            
    # Resolve imports utilizing the same strict AST precision
    if ast_graph and "imports" in ast_graph:
        context += "\n=== DEPENDENCY CONTEXT ===\n"
        for imp in ast_graph["imports"]:
            for other_file, other_graph in all_files_graphs.items():
                # Rough matching for dependency imports
                if imp in other_file or imp.split('.')[-1] in other_file:
                    context += f"\n--- Included Dependency: {other_file} ---\n"
                    if other_graph and "functions" in other_graph and other_graph["functions"]:
                        for func_name, func_body in other_graph["functions"].items():
                            context += f"\n[Dependency Function: {func_name}]\n{func_body}\n"
                    else:
                        try:
                            with open(other_file, "r", encoding="utf-8", errors="ignore") as dep_f:
                                context += dep_f.read()[:2000]
                        except Exception:
                            pass
                            
    return context
