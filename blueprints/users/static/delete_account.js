let delInput = document.getElementById('remove-input');
let delBtn = document.getElementById('del-btn')

delInput.addEventListener('input', checkInput);

function checkInput(){
    console.log('hello')
    if(delInput.value === 'DELETE'){
        delBtn.classList.remove('disabled')
        delBtn.classList.add('nav-user-btn')
    } else {
        delBtn.classList.remove('nav-user-btn')
        delBtn.classList.add('disabled')
    };
};

$('form').on('keyup keypress', function(e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) { 
      e.preventDefault();
      return false;
    }
  });