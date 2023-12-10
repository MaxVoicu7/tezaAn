let navbar = document.querySelector('.header .navbar');

document.querySelector('#menu-btn').onclick = () => {
  navbar.classList.toggle('active');
}



document.querySelectorAll('.about .video-container .video-controls .video__btn').forEach(btn => {
  btn.onclick = () => {
    let src = btn.getAttribute('data-src');
    document.querySelector('.about .video-container .video').src = src;

    let videoId = btn.getAttribute('id');
    document.querySelectorAll('.about__title, .about__description').forEach(el => {
      el.classList.add('display-description');
    });

    document.querySelector(`.about__title[id="${videoId}"]`).classList.remove('display-description');
    document.querySelector(`.about__description[id="${videoId}"]`).classList.remove('display-description');
  }
})