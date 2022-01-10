const navList = ['home', '/games', 'forum', 'support', 'users'];
for(let item of navList){
    if(item === 'users'){
        continue
    };
    if(window.location.href.indexOf(`${item}`) !== -1){
        activeNavFlag(`${item}`);
    } else if(window.location.href === `http://${window.location.host}/`){
        activeNavFlag(`home`);
    };
};

function activeNavFlag(section){
    $(`#${section}-nav`).children().children().first().addClass('nav-button-active-flag');
    $(`#${section}-nav`).children().children().last().removeClass('text-dark');
    $(`#${section}-nav`).children().children().last().addClass('text-light');
}

let mobileNavMenu = document.getElementById('navbarToggleExternalContent');
let mobileNavButton = document.getElementById('mobileNavButton');
let mainNav = document.querySelector('nav');
let navSticky = mainNav.offsetTop;

window.addEventListener('resize', () => {
    if(mobileNavMenu.className.indexOf('show') != -1){
        if ($(window).width() >= 768){
            mobileNavMenu.classList.remove('show');
            document.querySelector('html').style.overflow = '';
        };
    };
});

mobileNavButton.addEventListener('click', () => {
    if(document.querySelector('html').style.overflow != 'hidden'){
        document.querySelector('html').style.overflow = 'hidden';
    } else {
        document.querySelector('html').style.overflow = '';
    };
});

window.onscroll = function() {stickyNav()};
function stickyNav() {
    if (window.pageYOffset >= navSticky) {
    mainNav.classList.add("sticky");
    mobileNavMenu.style.top = navSticky -15 + 'px';
    } else {
      mainNav.classList.remove("sticky");
      mobileNavMenu.style.top = 'auto';
    };
  };


addEventListenersToNavBar(navList);

function addEventListenersToNavBar(list){
    for(let item of list){
        if (!($(`#${item}-nav`).children().children().first().hasClass('nav-button-active-flag'))){
            $(`#${item}-nav`).mouseenter(() => {
                navLinkMouseEnter(`${item}`);
            }).mouseleave(() => {
                navLinkMouseLeave(`${item}`);
            });
        };
    };
};


function navLinkMouseEnter(section){
    $(`#${section}-nav`).children().children().last().removeClass('text-dark');
    $(`#${section}-nav`).children().children().last().addClass('text-light');
    $(`#${section}-nav`).children().children().first().addClass('nav-button-flag');
};

function navLinkMouseLeave(section){
    $(`#${section}-nav`).children().children().first().removeClass('nav-button-flag');
    $(`#${section}-nav`).children().children().last().removeClass('text-light');
    $(`#${section}-nav`).children().children().last().addClass('text-dark');
};
