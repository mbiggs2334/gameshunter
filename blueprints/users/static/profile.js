let postNav = document.querySelector('#post-nav');
let followingNav = document.querySelector('#following-nav');
let followerNav = document.querySelector('#follower-nav');

let postDiv = document.querySelector('#post-div');
let followingDiv = document.querySelector('#following-div');
let followerDiv = document.querySelector('#follower-div');



postNav.addEventListener('click', () => {
    followerNav.classList.remove('gray');
    followerNav.classList.add('profile-tab');
    followerDiv.classList.add('d-none');
    followingNav.classList.remove('gray');
    followingNav.classList.add('profile-tab');
    followingDiv.classList.add('d-none');

    postNav.classList.add('gray');
    if(postDiv.className.indexOf('d-none') !== -1){
        postDiv.classList.remove('d-none');
    } else {
        postDiv.classList.add('d-none');
        postNav.classList.remove('gray');
        
    };
});


followingNav.addEventListener('click', () => {
    followerNav.classList.remove('gray');
    followerDiv.classList.add('d-none');
    postNav.classList.remove('gray');
    postDiv.classList.add('d-none');

    followingNav.classList.add('gray');
    if(followingDiv.className.indexOf('d-none') !== -1){
        followingDiv.classList.remove('d-none');
    } else {
        followingDiv.classList.add('d-none');
        followingNav.classList.remove('gray');
    };
});


followerNav.addEventListener('click', () => {
    postNav.classList.remove('gray');
    postDiv.classList.add('d-none');
    followingNav.classList.remove('gray');
    followingDiv.classList.add('d-none');

    followerNav.classList.add('gray');
    if(followerDiv.className.indexOf('d-none') !== -1){
        followerDiv.classList.remove('d-none');
    } else {
        followerDiv.classList.add('d-none');
        followerNav.classList.remove('gray')
    };
});

