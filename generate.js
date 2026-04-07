const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
// regex to capture `<section id="sec-xxx" ... </section>`
const sections = [...html.matchAll(/<section id="sec-([^"]+)"[\s\S]*?<\/section>/g)];

let baseHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canvas Kids - {Title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav id="top-nav">
        <div class="nav-left">
            <button id="btn-home" class="nav-btn" onclick="window.location.href='index.html'" aria-label="Home" title="Home">
                <i class="fa-solid fa-house"></i>
            </button>
            <h1 class="nav-logo">Canvas Kids</h1>
        </div>
        <div class="nav-right">
            <button id="btn-bgm" class="nav-btn"><i class="fa-solid fa-music"></i></button>
            <button id="btn-sound" class="nav-btn"><i class="fa-solid fa-volume-high"></i></button>
            <button id="btn-theme" class="nav-btn"><i class="fa-solid fa-moon"></i></button>
        </div>
    </nav>
    <main id="app-content">
        {Content}
    </main>
    <audio id="bgm-player" loop><source src="https://assets.mixkit.co/music/preview/mixkit-funny-puppy-music-loop-2746.mp3" type="audio/mpeg"></audio>
    <script src="script.js"></script>
</body>
</html>`;

sections.forEach(sec => {
    let name = sec[1];
    if(name === 'home') return;
    let title = name.charAt(0).toUpperCase() + name.slice(1);
    
    // Ignore the ones we already successfully wrote manually correctly with formatting
    if(title === 'Alphabets' || title === 'Numbers') return;

    let content = sec[0].replace('class="view-section"', 'class="view-section active"');
    fs.writeFileSync(title + '.html', baseHtml.replace('{Content}', content).replace('{Title}', title));
    console.log('Created ' + title + '.html');
});
