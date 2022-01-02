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