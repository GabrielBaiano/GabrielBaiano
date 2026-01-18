const fs = require('fs');
fetch('https://raw.githubusercontent.com/GabrielBaiano/personal-library/main/README.md')
  .then(r => r.text())
  .then(text => {
    fs.writeFileSync('temp_library_readme.md', text);
    console.log('File written: temp_library_readme.md');
  });
