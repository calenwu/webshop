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
function showCart() {
	cartOverlay.classList.remove('-right-full');
	cartOverlay.classList.remove('sm:-right-96');
	cartOverlay.classList.remove('2xl:-right-1/3');
	cartOverlayBackground.classList.remove('-z-1');
	cartOverlayBackground.classList.add('z-30');
	cartOverlayBackground.classList.add('opacity-100');
}
function hideCart() {
	cartOverlay.classList.add('-right-full');
	cartOverlay.classList.add('sm:-right-96');
	cartOverlay.classList.add('2xl:-right-1/3');
	cartOverlayBackground.classList.remove('opacity-100');
	cartOverlayBackground.classList.remove('z-30');
	cartOverlayBackground.classList.add('-z-1');
}
const delay = ms => new Promise(res => setTimeout(res, ms));
let firstGetCart = true;
async function getCart() {
	if (!firstGetCart) {
		if (window.location.pathname.includes('payment')) {
			location.reload();
			return;
		}
	}
	loadContent('cartOverlayContent' , cartOverlayContentUrl, 'bg-primary-400');
	if (document.getElementById('cartCheckoutTop')) {
		loadContent('cartCheckoutTop' , cartCheckoutTopUrl, 'bg-primary-400');
		loadContent('cartCheckoutRight' , cartCheckoutRightUrl, 'bg-primary-400');
	}
	firstGetCart = false;
}
function updateQuantity(form, productColorsQuantityId, qty=-1) {
	const quantity = qty == -1 ? form.getElementsByClassName('text-sm')[0].value : qty;
	if (quantity < 0) {
		createFancyAlert('error', invalidQuantityTitle, invalidQuantityText);
		return false;
	}
	const refreshBtn = form.getElementsByClassName('rounded-r')[0];
	url = cartUpdateUrl.replace(/12345/, productColorsQuantityId);
	url = url.replace(/12345/, quantity);
	refreshBtn.disabled = true;
	const prevIcon = refreshBtn.innerHTML;
	refreshBtn.firstElementChild.classList.add('spinning');
	fetch(url)
		.then(response => response.json())
		.then((data) => {
			refreshBtn.firstElementChild.classList.remove('spinning');
			data = data['data'];
			if (data['success']){
				refreshBtn.innerHTML = '<i class="fas fa-check"></i>';
				setTimeout(function() {
					refreshBtn.innerHTML = prevIcon;
				}, 1000);
				if (data['message']) {
					createFancyAlert(data['message']['tag'], data['message']['title'], data['message']['innerHtml'], 5000);
				}
				location.reload();
			} else {
				createFancyAlert(data['message']['tag'], data['message']['title'], data['message']['innerHtml']);
				getCart();
			}
		})
		.catch((error) => {
			refreshBtn.firstElementChild.classList.remove('spinning');
			createFancyAlert('error', errorString, error.toString());
			getCart();
		});
	refreshBtn.innerHTML = '<i class="fas fa-sync"></i>';
	refreshBtn.disabled = false;
	return false;
}
function updateOverlayQuantity(form, productColorsQuantityId, qty=-1) {
	const quantity = qty == -1 ? form.getElementsByClassName('text-sm')[0].value : qty;
	if (quantity < 0) {
		createFancyAlert('error', invalidQuantityTitle, invalidQuantityText);
		return false;
	}
	const refreshBtn = form.getElementsByClassName('rounded-r')[0];
	url = cartUpdateUrl.replace(/12345/, productColorsQuantityId);
	url = url.replace(/12345/, quantity);
	refreshBtn.disabled = true;
	const prevIcon = refreshBtn.innerHTML;
	refreshBtn.firstElementChild.classList.add('spinning');
	fetch(url)
		.then(response => response.json())
		.then((data) => {
			refreshBtn.firstElementChild.classList.remove('spinning');
			data = data['data'];
			if (data['success']){
				refreshBtn.innerHTML = '<i class="fas fa-check"></i>';
				setTimeout(function() {
					refreshBtn.innerHTML = prevIcon;
				}, 1000);
				if (data['message']) {
					createFancyAlert(data['message']['tag'], data['message']['title'], data['message']['innerHtml'], 5000);
				}
				getCart();
			} else {
				createFancyAlert(data['message']['tag'], data['message']['title'], data['message']['innerHtml']);
			}
		})
		.catch((error) => {
			createFancyAlert('error', errorString, error.toString());
		});
	refreshBtn.disabled = false;
	return false;
}
