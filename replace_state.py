import os
import glob
import re

for filepath in glob.glob("**/*.py", recursive=True):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    
    def repl_get(m):
        key = m.group(1).strip("'\"")
        default = m.group(2)
        if default:
            return f"getattr(page, '{key}'{default})"
        else:
            return f"getattr(page, '{key}', None)"
            
    content, n = re.subn(r"page\.client_storage\.get\((['\"][^'\"]+['\"])([^)]*)\)", repl_get, content)
    
    def repl_set(m):
        key = m.group(1).strip("'\"")
        val = m.group(2).strip()
        if val.endswith(")"):
            # in case of nested parenthesis
            pass
        # simpler replace
        return f"setattr(page, '{key}', {val})"
        
    # We use a simpler regex for set:
    content, n = re.subn(r"page\.client_storage\.set\((['\"][^'\"]+['\"]),\s*(.+?)\)", repl_set, content)
    
    # Just in case some sets had nested parentheses that break regex
    content = content.replace("page.client_storage.set(\"eventos\", eventos_data)", "setattr(page, 'eventos', eventos_data)")
    content = content.replace("page.client_storage.set(\"eventos\", [])", "setattr(page, 'eventos', [])")
    content = content.replace("page.client_storage.set(\"usuario_logado\", None)", "setattr(page, 'usuario_logado', None)")
    content = content.replace("page.client_storage.set(\"carrinho\", [])", "setattr(page, 'carrinho', [])")
    content = content.replace("page.client_storage.set(\"cupons_resgatados\", [])", "setattr(page, 'cupons_resgatados', [])")
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")
