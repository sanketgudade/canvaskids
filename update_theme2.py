import os
import glob
import re

html_files = glob.glob('*.html')

for filepath in html_files:
    if filepath == 'Fruits.html':
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = re.compile(
        r'(if\s*\(\s*btnTheme\s*\)\s*\{\s*)(btnTheme\.addEventListener\(.*?\n\s*\}\);)(\s*\})',
        re.DOTALL
    )
    
    def replacer(match):
        prefix = match.group(1)
        new_prefix = prefix + """
        if (localStorage.getItem('canvasKidsTheme') === 'dark') {
            AppState.isDarkMode = true;
            document.body.classList.add('dark-theme');
            btnTheme.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
        """
        
        listener = match.group(2)
        if "localStorage.setItem" not in listener:
            listener = listener.replace(
                "btnTheme.innerHTML = AppState.isDarkMode ? '<i class=\"fa-solid fa-sun\"></i>' : '<i class=\"fa-solid fa-moon\"></i>';",
                "btnTheme.innerHTML = AppState.isDarkMode ? '<i class=\"fa-solid fa-sun\"></i>' : '<i class=\"fa-solid fa-moon\"></i>';\n                    localStorage.setItem('canvasKidsTheme', AppState.isDarkMode ? 'dark' : 'light');"
            )
        
        suffix = match.group(3)
        return new_prefix + listener + suffix

    if 'canvasKidsTheme' not in content:
        new_content = pattern.sub(replacer, content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
        else:
            print(f"Regex didn't match in {filepath}")
    else:
        print(f"Already updated {filepath}")
