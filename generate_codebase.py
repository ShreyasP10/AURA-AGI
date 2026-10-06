import os
import pathspec

def generate_codebase():
    ignore_patterns = [
        '.git/', '__pycache__/', '*.pyc', 'node_modules/', '.env', '.env.*',
        'ASSETS/', 'codebase.md', '*.wav', '*.mp3', '*.png', '*.jpg', '*.exe'
    ]
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, ignore_patterns)
    
    with open('codebase.md', 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk('.'):
            # Prune hidden dirs and ignored dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and not spec.match_file(os.path.relpath(os.path.join(root, d), '.'))]
            
            for file in files:
                if file.startswith('.'): continue
                filepath = os.path.relpath(os.path.join(root, file), '.')
                if spec.match_file(filepath):
                    continue
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                    outfile.write(f"\\n\\n### File: {filepath}\\n")
                    outfile.write("```\\n")
                    outfile.write(content)
                    outfile.write("\\n```\\n")
                except Exception as e:
                    print(f"Skipping {filepath}: {e}")

if __name__ == '__main__':
    generate_codebase()
    print("codebase.md generated successfully.")
