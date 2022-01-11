let delInput = document.getElementById('remove-input');
let delBtn = document.getElementById('del-btn')

delInput.addEventListener('input', checkInput);

//Checks whether the User typed in the word 'DELETE' correctly
//on a good read it will enable the 'Delete account' button to be able to be clicked. 
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

//Adds event listener to form, prevent the 'enter' key from submiting form
$('form').on('keyup keypress', function(e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) { 
      e.preventDefault();
      return false;
    }
  });