

function insertParam(key, value) {
	key = encodeURIComponent(key);
	value = encodeURIComponent(value);
	var kvp = document.location.search.substr(1).split('&');
	let i=0;
	for(; i<kvp.length; i++){
		if (kvp[i].startsWith(key + '=')) {
			let pair = kvp[i].split('=');
			pair[1] = value;
			kvp[i] = pair.join('=');
			break;
		}
	}
	if(i >= kvp.length){
		kvp[kvp.length] = [key,value].join('=');
	}
	let params = kvp.join('&');
	document.location.search = params;
}

function initProductDetailCarousel(
	primaryCarouselId,
	secondaryCarouselId,
	primaryCarouselListId,
	secondaryCarouselListId,
	productImagesOverlayId,
	overlaySliderPrimary,
	overlaySliderSecondary,
	images) {
	const primaryCarousel = document.getElementById(primaryCarouselListId);
	const secondaryCarousel = document.getElementById(secondaryCarouselListId);
	const productImagesOverlay = document.getElementById(productImagesOverlayId);
	while (primaryCarousel.firstChild) {
		primaryCarousel.firstChild.remove()
	}
	while (secondaryCarousel.firstChild) {
		secondaryCarousel.firstChild.remove()
	}
	for (let i = 0; i < images.length; i++) {
		primaryCarousel.appendChild(createCarouselImageLi(images[i]));
		secondaryCarousel.appendChild(createCarouselImageLi(images[i]));
	}
	var primarySlider = new Splide('#' + primaryCarouselId, {
		type       : 'fade',
		heightRatio: 0.8,
		pagination : false,
		arrows     : false,
		cover      : true,
	});
	var secondarySlider = new Splide('#' + secondaryCarouselId, {
		rewind      : true,
		fixedWidth  : 100,
		fixedHeight : 66,
		isNavigation: true,
		gap         : 10,
		focus       : 'center',
		pagination  : false,
		cover       : true,
		breakpoints : {
			'600': {
				fixedWidth  : 66,
				fixedHeight : 40,
			}
		}
	}).mount();
	primarySlider.sync(secondarySlider).mount();
	for (let i = 0; i < primaryCarousel.children.length; i++) {
		primaryCarousel.children[i].style.setProperty('background-size', 'contain', 'important');
		primaryCarousel.children[i].onclick = function() {
			overlaySliderPrimary.go(i);
			overlaySliderSecondary.go(i);
			productImagesOverlay.classList.remove('opacity-0');
			productImagesOverlay.classList.remove('-z-1');
			productImagesOverlay.classList.add('z-40');
		}
	}
}

function initProductDetailOverlayCarousel(
	primaryCarouselId,
	secondaryCarouselId,
	primaryCarouselListId,
	secondaryCarouselListId,
	images){
	const primaryCarousel = document.getElementById(primaryCarouselListId);
	const secondaryCarousel = document.getElementById(secondaryCarouselListId);
	while (primaryCarousel.firstChild) {
		primaryCarousel.firstChild.remove()
	}
	while (secondaryCarousel.firstChild) {
		secondaryCarousel.firstChild.remove()
	}
	for (let i = 0; i < images.length; i++) {
		primaryCarousel.appendChild(createCarouselImageLi(images[i]));
		secondaryCarousel.appendChild(createCarouselImageLi(images[i]));
	}
	var primarySlider = new Splide('#' + primaryCarouselId, {
		type       : 'fade',
		heightRatio: 1,
		pagination : false,
		arrows     : false,
		cover      : true,
	});
	var secondarySlider = new Splide('#' + secondaryCarouselId, {
		rewind      : true,
		fixedWidth  : 100,
		fixedHeight : 66,
		isNavigation: true,
		gap         : 10,
		focus       : 'center',
		pagination  : false,
		cover       : true,
		breakpoints : {
			'600': {
				fixedWidth  : 66,
				fixedHeight : 40,
			}
		}
	}).mount();
	primarySlider.sync(secondarySlider).mount();
	for (let i = 0; i < primaryCarousel.children.length; i++) {
		primaryCarousel.children[i].style.setProperty('background-size', 'contain', 'important');
		primaryCarousel.children[i].style.setProperty('max-height', 'calc(100vh - 240px)'); 
	}
	return [primarySlider, secondarySlider];
}

function initSimpleProductDetailCarousel(
	primaryCarouselId,
	secondaryCarouselId,
	primaryCarouselListId,
	secondaryCarouselListId,
	images) {
	const primaryCarousel = document.getElementById(primaryCarouselListId);
	const secondaryCarousel = document.getElementById(secondaryCarouselListId);
	while (primaryCarousel.firstChild) {
		primaryCarousel.firstChild.remove()
	}
	while (secondaryCarousel.firstChild) {
		secondaryCarousel.firstChild.remove()
	}
	for (let i = 0; i < images.length; i++) {
		primaryCarousel.appendChild(createCarouselImageLi(images[i]));
		secondaryCarousel.appendChild(createCarouselImageLi(images[i]));
	}
	var primarySlider = new Splide('#' + primaryCarouselId, {
		type       : 'fade',
		heightRatio: 0.8,
		pagination : false,
		arrows     : false,
		cover      : true,
	});
	var secondarySlider = new Splide('#' + secondaryCarouselId, {
		rewind      : true,
		fixedWidth  : 100,
		fixedHeight : 66,
		isNavigation: true,
		gap         : 10,
		focus       : 'center',
		pagination  : false,
		cover       : true,
		breakpoints : {
			'600': {
				fixedWidth  : 66,
				fixedHeight : 40,
			}
		}
	}).mount();
	primarySlider.sync(secondarySlider).mount();
	for (let i = 0; i < primaryCarousel.children.length; i++) {
		primaryCarousel.children[i].style.setProperty('background-size', 'contain', 'important');
	}
}

function createCarouselImageLi(img) {
	let image = document.createElement('img');
	image.classList.add('w-full');
	image.setAttribute('src', img);
	image.setAttribute('alt', 'carousel image');
	let slide = document.createElement('li');
	slide.classList.add('splide__slide');
	slide.appendChild(image);
	return slide;
}
