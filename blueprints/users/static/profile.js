let postNav = document.querySelector('#post-nav');
let followingNav = document.querySelector('#following-nav');
let followerNav = document.querySelector('#follower-nav');

let postDiv = document.querySelector('#post-div');
let followingDiv = document.querySelector('#following-div');
let followerDiv = document.querySelector('#follower-div');

//adds event listeners to the profile nav buttons
postNav.addEventListener('click', () => {
    changeProfileDom(postNav);
    
});


followingNav.addEventListener('click', () => {
    changeProfileDom(followingNav);
});


followerNav.addEventListener('click', () => {
    changeProfileDom(followerNav);
});

//changes the DOM to show the selected info and hide the unselected
function changeProfileDom(profileNav){
    let navs = [postNav, followingNav, followerNav];
    let divs = [postDiv, followingDiv, followerDiv];
    let index = navs.indexOf(profileNav);

    navs.splice(index, 1);
    let removedDiv = divs.splice(index, 1);

    for(let nav of navs){
        nav.classList.remove('gray');
    };

    for(let div of divs){
        div.classList.add('d-none');
    };
    
    profileNav.classList.add('gray');
    if(removedDiv[0].className.indexOf('d-none') !== -1){
        removedDiv[0].classList.remove('d-none');
    } else {
        removedDiv[0].classList.add('d-none');
        profileNav.classList.remove('gray');
    };
};


