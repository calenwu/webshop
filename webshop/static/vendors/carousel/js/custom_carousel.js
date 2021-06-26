function initCarousel(images) {
	const productImagesCarousel = document.getElementById('productImagesCarousel');
	const productImagesCarouselPicker = document.getElementById('productImagesCarouselPicker');
	while (productImagesCarousel.firstChild) {
		productImagesCarousel.firstChild.remove()
	}
	while (productImagesCarouselPicker.firstChild) {
		productImagesCarouselPicker.firstChild.remove()
	}
	for (let i = 0; i < images.length; i++) {
		productImagesCarousel.appendChild(createCarouselImageDiv(images[i]));
		productImagesCarouselPicker.appendChild(createCarouselImagePicker(i + 1));
	}
	showSlides(1);
}

function createCarouselImageDiv(img) {
	let image = document.createElement('img');
	image.classList.add('w-full');
	image.setAttribute('src', img);
	image.setAttribute('alt', 'carousel image');
	let slide = document.createElement('div');
	slide.classList.add('mySlides');
	slide.classList.add('fade');
	slide.appendChild(image);
	return slide;
}

function createCarouselImagePicker(index) {
	let picker = document.createElement('span');
	picker.classList.add('dot');
	picker.addEventListener('click', function() {currentSlide(index)});
	return picker;
}

let slideIndex = 1;
// Next/previous controls
function plusSlides(n) {
	showSlides(slideIndex += n);
}
// Thumbnail image controls
function currentSlide(n) {
	showSlides(slideIndex = n);
}
function showSlides(n) {
	let i;
	let slides = document.getElementsByClassName("mySlides");
	let dots = document.getElementsByClassName("dot");
	if (n > slides.length) {slideIndex = 1}
	if (n < 1) {slideIndex = slides.length}
	for (i = 0; i < slides.length; i++) {
		slides[i].style.display = 'none';
	}
	for (i = 0; i < dots.length; i++) {
		dots[i].className = dots[i].className.replace(' active', '');
	}
	slides[slideIndex-1].style.display = 'block';
	dots[slideIndex-1].className += ' active';
}