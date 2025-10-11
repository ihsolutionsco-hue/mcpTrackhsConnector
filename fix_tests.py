#!/usr/bin/env python3
"""
Script para corregir tests que fallan
"""

import re
from pathlib import Path

def fix_async_tests(file_path):
    """Corregir tests para que sean async"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Patrón para encontrar tests que llaman a search_tool sin await
    pattern = r'def (test_\w+)\(self, search_tool\):\s*\n(\s+)"""([^"]*)"""\s*\n(\s+)with pytest\.raises\(ValidationError\) as exc_info:\s*\n(\s+)search_tool\('
    
    def replace_test(match):
        test_name = match.group(1)
        indent = match.group(2)
        docstring = match.group(3)
        indent2 = match.group(4)
        indent3 = match.group(5)
        
        return f'@pytest.mark.asyncio\n{indent}async def {test_name}(self, search_tool):\n{indent}    """{docstring}"""\n{indent2}with pytest.raises(ValidationError) as exc_info:\n{indent3}await search_tool('
    
    content = re.sub(pattern, replace_test, content, flags=re.MULTILINE)
    
    # Patrón para encontrar tests que llaman a search_tool sin await (sin pytest.raises)
    pattern2 = r'def (test_\w+)\(self, search_tool\):\s*\n(\s+)"""([^"]*)"""\n(\s+)search_tool\('
    
    def replace_test2(match):
        test_name = match.group(1)
        indent = match.group(2)
        docstring = match.group(3)
        indent2 = match.group(4)
        
        return f'@pytest.mark.asyncio\n{indent}async def {test_name}(self, search_tool):\n{indent}    """{docstring}"""\n{indent2}await search_tool('
    
    content = re.sub(pattern2, replace_test2, content, flags=re.MULTILINE)
    
    # Reemplazar search_tool( por await search_tool( en líneas que no tienen await
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'search_tool(' in line and 'await' not in line and 'def ' not in line:
            # Reemplazar search_tool( por await search_tool(
            line = line.replace('search_tool(', 'await search_tool(')
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed async tests in {file_path}")
        return True
    return False

def main():
    """Función principal para corregir tests"""
    test_files = [
        "tests/unit/test_search_reservations_validation.py",
        "tests/unit/test_types.py"
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            print(f"Processing {file_path}...")
            fix_async_tests(file_path)
        else:
            print(f"File {file_path} not found")

if __name__ == "__main__":
    main()
