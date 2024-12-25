config = document.getElementById('tableConfig')
if(config) {
    rows = config.querySelectorAll('tr')
    for(let i = 1; i < rows.length; i++) {
        rows[i].querySelectorAll('td')[3].querySelector('p').textContent = rows[i].querySelectorAll('td')[3].querySelector('p').textContent.split(' ').slice(0, 1).join('');
    }
}
