fancyAlertCounter = 0;

function createFancyAlert(tag, title, innerHTML, mSecVisible) {
  let firstDiv = setAttributes(document.createElement('div'), {
		'id': 'fancy-alert-' + fancyAlertCounter.toString(),
		'class': 'flex justify-between bg-white w-full md:w-3/4 p-3 transition-opacity relative rounded mb-4 shadow border-l-4 opacity-0'
	});
  let icon = setAttributes(document.createElement('i'), {
		'class': 'fancy-alert-icon fas',
	});
  let secondDiv = setAttributes(document.createElement('div'), {
    'class': 'flex',
  });
  let thirdDiv = setAttributes(document.createElement('div'), {
    'class': '',
  });
  if (tag == 'success') {
		firstDiv.classList.add('border-green-400');
		icon.classList.add('text-green-400');
		icon.classList.add('fa-check-circle');
  } else if (tag =='warning') {
		firstDiv.classList.add('border-yellow-400');
		icon.classList.add('text-yellow-400');
		icon.classList.add('fa-exclamation-circle');
  } else {
		firstDiv.classList.add('border-red-400');
		icon.classList.add('text-red-400');
		icon.classList.add('fa-times-circle');
	}
  thirdDiv.appendChild(icon);
  let fourthDiv = setAttributes(document.createElement('div'), {
    'class': 'pl-2',
  });
  let titleDiv = setAttributes(document.createElement('div'), {
    'class': 'font-bold font-weight-bold mb-1'
  });
  let text = setAttributes(document.createElement('div'), {
    'class': 'mb-1',
  });
  titleDiv.innerText = title;
  text.innerHTML = innerHTML;
  fourthDiv.appendChild(titleDiv);
  fourthDiv.appendChild(text);
  secondDiv.appendChild(thirdDiv);
  secondDiv.appendChild(fourthDiv);
  let closeContainer = setAttributes(document.createElement('div'), {
    'class': 'flex justify-center items-center',
  });
  let closeIconContainer = setAttributes(document.createElement('span'), {
    'class': 'p-2',
    'onClick': 'closeFancyAlert(' + fancyAlertCounter.toString() + ')'
  });
  let closeIcon = setAttributes(document.createElement('i'), {
    'class': 'cursor-pointer fal fa-times',
  });
  closeIconContainer.appendChild(closeIcon);
  closeContainer.appendChild(closeIconContainer);
  firstDiv.appendChild(secondDiv);
  firstDiv.appendChild(closeContainer);
  let snackbar = document.getElementById('snackbar');
  snackbar.appendChild(firstDiv);
	firstDiv.classList.add('opacity-100');
  fancyAlertCounter = fancyAlertCounter + 1;
  if (mSecVisible) {
    setTimeout(function () {
      closeIconContainer.click();
    }, mSecVisible);
  } else {
    setTimeout(function () {
      closeIconContainer.click();
    }, 5000);
  }
}

function closeFancyAlert(alert_id) {
  let alert = document.getElementById('fancy-alert-' + alert_id.toString());
  alert.classList.remove('opacity-100');
  setTimeout(function () {
    alert.style.height = 0;
  }, 250);
  setTimeout(function () {
    removeElement('fancy-alert-' + alert_id.toString());
  }, 500);
}

function transformButtonToLoad(btn, bgColor) {
  btn.innerText = '';
  btn.appendChild(getSpinnerDots(bgColor));
  btn.disabled = true;
}

function transformButtonToNormal(btn, text) {
  removeAllChilds(btn);
  btn.disabled = false;
  btn.innerText = text;
}

function getSpinnerDotsContainerMedium(bgColor) {
  let firstDiv = setAttributes(document.createElement('div'), {
    'class': 'spinner-dots-container',
  });
  firstDiv.appendChild(getSpinnerDotsMedium(bgColor));
  return firstDiv
}

function getSpinnerDotsContainer(bgColor) {
  let firstDiv = setAttributes(document.createElement('div'), {
    'class': 'spinner-dots-container',
  });
  firstDiv.appendChild(getSpinnerDots(bgColor));
  return firstDiv
}

function getSpinnerDotsMedium(bgColor) {
  let megaDiv = setAttributes(document.createElement('div'), {
    'class': 'flex w-full justify-center items-center',
  });
  let firstDiv = setAttributes(document.createElement('div'), {
    'class': 'spinner-dots spinner-dots-medium',
  });
  let bounce1 = setAttributes(document.createElement('div'), {
    'class': 'bounce1 ' + bgColor,
  });
  let bounce2 = setAttributes(document.createElement('div'), {
    'class': 'bounce2 ' + bgColor,
  });
  let bounce3 = setAttributes(document.createElement('div'), {
    'class': 'bounce3 ' + bgColor,
  });
  let invis1 = setAttributes(document.createElement('div'), {
    'class': 'invisible',
  });
  let invis2 = setAttributes(document.createElement('div'), {
    'class': 'invisible',
  });
  invis1.innerHTML = 'h';
  invis2.innerHTML = 'h';
  firstDiv.appendChild(bounce1);
  firstDiv.appendChild(bounce2);
  firstDiv.appendChild(bounce3);
  megaDiv.appendChild(invis1);
  megaDiv.appendChild(firstDiv);
  megaDiv.appendChild(invis2);
  return megaDiv;
}

function getSpinnerDots(bgColor) {
  let megaDiv = setAttributes(document.createElement('div'), {
    'class': 'flex w-full justify-center items-center',
  });
  let firstDiv = setAttributes(document.createElement('div'), {
    'class': 'spinner-dots',
  });
  let bounce1 = setAttributes(document.createElement('div'), {
    'class': 'bounce1 ' + bgColor,
  });
  let bounce2 = setAttributes(document.createElement('div'), {
    'class': 'bounce2 ' + bgColor,
  });
  let bounce3 = setAttributes(document.createElement('div'), {
    'class': 'bounce3 ' + bgColor,
  });
  let invis1 = setAttributes(document.createElement('div'), {
    'class': 'invisible',
  });
  let invis2 = setAttributes(document.createElement('div'), {
    'class': 'invisible',
  });
  invis1.innerHTML = 'h';
  invis2.innerHTML = 'h';
  firstDiv.appendChild(bounce1);
  firstDiv.appendChild(bounce2);
  firstDiv.appendChild(bounce3);
  megaDiv.appendChild(invis1);
  megaDiv.appendChild(firstDiv);
  megaDiv.appendChild(invis2);
  return megaDiv;
}

function setAttributes(el, attrs) {
  for (let key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
  return el;
}

function removeElement(id) {
  document.getElementById(id).outerHTML = "";
}

async function loadContent(container_id, url, color) {
	let container = document.getElementById(container_id);
	const oldChildren = container.children;
	container.classList.add('flex', 'justify-center', 'items-center');
	while(container.firstChild) {container.firstChild.remove()};
	let spinnerContainer = document.createElement('div');
	spinnerContainer.classList.add('h-72', 'w-full', 'flex', 'justify-center', 'items-center');
	let spinnerDots = getSpinnerDotsContainerMedium(color);
	spinnerContainer.appendChild(spinnerDots);
	container.appendChild(spinnerContainer);
	const startTime = Date.now();
	await fetch(url)
		.then(response => {
			return response.text()
		})
		.then(html => {
			const elapsedTime = ((Date.now() - startTime));
			if (elapsedTime > 400){
				while(container.firstChild) {container.firstChild.remove()};
				container.appendChild(new DOMParser().parseFromString(html, 'text/html').querySelector('div'));
				container.classList.remove('justify-center', 'items-center');
			} else {
				setTimeout(() => {
					while(container.firstChild) {container.firstChild.remove()};
					container.appendChild(new DOMParser().parseFromString(html, 'text/html').querySelector('div'));
					container.classList.remove('justify-center', 'items-center');
				},  400 - elapsedTime);
			}
		})
		.catch(error => {
			while(container.firstChild) {container.firstChild.remove()};
			for(let i = 0; i < oldChildren.length; i++){
				container.appendChild(oldChildren[i]);
			}
			createFancyAlert('error', 'Loading error', 'There was an error trying to load the content');
			container.classList.remove('justify-center', 'items-center');
			throw error;
		})
	return true;
}

function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+ d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

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
	aspectRatio,
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
		primaryCarousel.appendChild(createCarouselZoomImageLi(images[i]));
		secondaryCarousel.appendChild(createCarouselImageLi(images[i]['src']));
	}
	var primarySlider = new Splide('#' + primaryCarouselId, {
		type       : 'fade',
		heightRatio: aspectRatio,
		pagination : false,
		arrows     : false,
		cover      : true,
		rewind     : true,
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
		rewind     : true,
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
	return primarySlider;
}

function createCarouselZoomImageLi(img) {
	let image = document.createElement('img');
	image.classList.add('w-auto');
	image.classList.add('h-auto');
	image.classList.add('max-w-full');
	image.classList.add('max-h-full');
	image.classList.add('object-contain');
	image.setAttribute('src', img['src']);
	image.setAttribute('alt', 'carousel image');
	let a = document.createElement('a');
	a.setAttribute('href', 'javascript:void(0);');
	a.setAttribute('data-pswp-src', img['src']);
	a.setAttribute('data-pswp-width', img['width']);
	a.setAttribute('data-pswp-height', img['height']);
	a.classList.add('m-auto');
	a.classList.add('max-w-full');
	a.classList.add('h-full');
	a.appendChild(image);
	let slide = document.createElement('li');
	slide.classList.add('splide__slide');
	slide.classList.add('flex');
	slide.appendChild(a);
	return slide;
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

function changeToSpinner(el) {
	el.style.width = nextButton.offsetWidth + 'px';
	el.style.height = nextButton.offsetHeight + 'px';
	el.innerHTML = '';
	let spinner = document.createElement('i');
	spinner.classList.add('fad');
	spinner.classList.add('fa-spinner-third');
	spinner.classList.add('spinning');
	el.appendChild(spinner);
}
