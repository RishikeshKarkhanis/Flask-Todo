var panel = document.getElementById('popup-panel');

var button = document.getElementById('add-btn-click');

button.addEventListener('click', event => { panel.style.display = "flex"; });

var close_button = document.getElementById('close-btn');

close_button.addEventListener('click', event => { panel.style.display = 'none'; });

fetch('https://flask-todo-ts81.onrender.com/api')
  .then(response => response.json())

  .then(data => {
    for (i in data) {
      if (data[i].is_done == 1) {
        document.getElementById(i).style.backgroundColor = "#c7b436";
        document.getElementById(i).innerHTML = "Undo"
        document.getElementById('P-' + i).innerHTML = '<strike>' + data[i].title + '</strike>'
      }
    }
  })

  .catch(error => console.error(error));