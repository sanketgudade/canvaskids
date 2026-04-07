import os
import glob
import re

html_files = glob.glob('*.html')

for filepath in html_files:
    if filepath == 'Fruits.html':
        continue # Skipped because it has custom setup
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for exactly this generic block:
    #     if (btnTheme) {
    #         btnTheme.addEventListener('click', () => {
    #             playClickSound(); 
    #             AppState.isDarkMode = !AppState.isDarkMode;
    #             document.body.classList.toggle('dark-theme', AppState.isDarkMode);
    #             btnTheme.innerHTML = AppState.isDarkMode ? '<i class=\"fa-solid fa-sun\"></i>' : '<i class=\"fa-solid fa-moon\"></i>';
    #         });
    #     }
    
    old_btn_theme = """    if (btnTheme) {
        btnTheme.addEventListener('click', () => {
            playClickSound(); 
            AppState.isDarkMode = !AppState.isDarkMode;
            document.body.classList.toggle('dark-theme', AppState.isDarkMode);
            btnTheme.innerHTML = AppState.isDarkMode ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
        });
    }"""

    new_btn_theme = """    if (btnTheme) {
        // init theme on load
        if (localStorage.getItem('canvasKidsTheme') === 'dark') {
            AppState.isDarkMode = true;
            document.body.classList.add('dark-theme');
            btnTheme.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
        
        btnTheme.addEventListener('click', () => {
            playClickSound(); 
            AppState.isDarkMode = !AppState.isDarkMode;
            document.body.classList.toggle('dark-theme', AppState.isDarkMode);
            btnTheme.innerHTML = AppState.isDarkMode ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
            localStorage.setItem('canvasKidsTheme', AppState.isDarkMode ? 'dark' : 'light');
        });
    }"""

    # If the file hasn't been updated yet, update it
    if old_btn_theme in content:
        content = content.replace(old_btn_theme, new_btn_theme)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated theme persistence in {filepath}")
    elif new_btn_theme in content:
        print(f"Already updated {filepath}")
    else:
        print(f"WARNING: Could not find theme target in {filepath}")
