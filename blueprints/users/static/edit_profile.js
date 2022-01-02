

let loadFile = function(event) {
    let output = document.getElementById('img');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src);
    };
  };

let editProfileDiv = document.getElementById('profile-settings');
let editProfileBtns = document.querySelectorAll('[data-ep]');
let accountSettingsDiv = document.getElementById('account-settings');
let accountSettingsBtns = document.querySelectorAll('[data-as]');


for(let node of accountSettingsBtns){
    node.addEventListener('click', editAccount);
};

for(let node of editProfileBtns){
    node.addEventListener('click', editProfile);
};


function editProfile(){
    accountSettingsDiv.classList.add('d-none');
    editProfileDiv.classList.remove('d-none');

    for(let btn of editProfileBtns){
        btn.classList.remove('text-white-50')
        btn.classList.add('text-decoration-underline', 'link-light', 'fw-bolder');
    };
    for(let btn of accountSettingsBtns){
        btn.classList.remove('text-decoration-underline', 'link-light', 'fw-bolder');
        btn.classList.add('text-white-50')
    };
    $("textarea").each(function () {
        this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
        }).on("input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    });
    let textArea = document.querySelector('textarea')
    textArea.style.resize = 'vertical';
    textArea.style.maxHeight = '275px';
};

function editAccount(){
    editProfileDiv.classList.add('d-none');
    accountSettingsDiv.classList.remove('d-none');

    for(let btn of editProfileBtns){
        btn.classList.remove('text-decoration-underline', 'link-light', 'fw-bolder');
        btn.classList.add('text-white-50');
    };
    for(let btn of accountSettingsBtns){
        btn.classList.remove('text-white-50')
        btn.classList.add('text-decoration-underline', 'link-light', 'fw-bolder');
    };
};

let topNav = document.getElementById('top-nav');
let sideNav = document.getElementById('side-nav');

if(topNav && sideNav){
    if($(window).width() > 768){
        sideNav.classList.remove('d-none');
    } else {
        topNav.classList.remove('d-none');
    };

};

window.addEventListener('resize', () => {
    if(topNav && sideNav){
        if($(window).width() > 768){
            sideNav.classList.remove('d-none');
            topNav.classList.add('d-none');
        } else {
            topNav.classList.remove('d-none');
            sideNav.classList.add('d-none');
        };
    };
});