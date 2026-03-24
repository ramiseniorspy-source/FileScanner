import ast
import re

def parse_python_imports_and_funcs(filepath, content):
    """
    Parses a python file to extract function definitions and imports 
    to build an execution context map.
    """
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError:
        return {"imports": [], "functions": {}, "classes": {}}
        
    data = {"imports": [], "functions": {}, "classes": {}}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                data["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                data["imports"].append(node.module)
        elif isinstance(node, ast.FunctionDef):
            # Capture the start and end line of the function
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            func_lines = content.split('\n')[start-1:end]
            data["functions"][node.name] = '\n'.join(func_lines)
            
    return data

def generic_regex_parser(content):
    """
    Fallback for Javascript/Typescript/Go/etc to find basic function names.
    Uses regex to extract function blocks or top-level declarations.
    """
    data = {"functions": {}}
    
    # Simple regex to catch `function foo()` or `const bar = () =>` or `func Query()`
    pattern = re.compile(r'(?:function|func|const|let)\s+([\w\d_]+)\s*(?:=\s*(?:async\s*)?\([^)]*\)\s*=>|\([^)]*\))', re.IGNORECASE)
    
    for match in pattern.finditer(content):
        func_name = match.group(1)
        # Just grab the next ~15 lines as the block for the graph (very rough fallback)
        start_pos = content.count('\n', 0, match.start())
        lines = content.split('\n')[start_pos:start_pos+15]
        data["functions"][func_name] = '\n'.join(lines)
        
    return data

def analyze_file_ast(filepath):
    """
    Reads the file and parses its syntax tree (AST) to extract functions 
    and identify dependencies. Returns a dictionary graph.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return None
        
    if filepath.endswith('.py'):
        return parse_python_imports_and_funcs(filepath, content)
    else:
        return generic_regex_parser(content)
