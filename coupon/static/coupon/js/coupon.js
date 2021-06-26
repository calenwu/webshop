async function applyCoupon(form, refresh = false) {
	const code = form.getElementsByClassName('rounded-l')[0].value;
	const csrf = form.getElementsByClassName('rounded-l')[0].previousElementSibling.value;
	const warning = form.getElementsByClassName('rounded-l')[0].parentElement.previousElementSibling;
	const dataForm = new FormData();
	const forms = document.getElementsByClassName('couponForm');
	Array.from(forms).forEach((element) => {
		const refreshBtn = element.getElementsByClassName('rounded-r')[0];
		refreshBtn.disabled = true;
		refreshBtn.innerHTML = '<i class="fal fa-sync"></i>';
		refreshBtn.firstElementChild.classList.add('spinning'); 
	});
	dataForm.append('csrfmiddlewaretoken', csrf);
	dataForm.append('code', code);
	await fetch(couponApplyUrl, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
		body: dataForm // body data type must match "Content-Type" header
	})
		.then(response => response.json())
		.then((data) => {
			Array.from(forms).forEach((element) => {
				const refreshBtn = element.getElementsByClassName('rounded-r')[0];
				refreshBtn.firstElementChild.classList.remove('spinning');
			});
			data = data['data'];
			if (data['success']){
				if (refresh) {
					location.reload();
				}
				Array.from(forms).forEach((element) => {
					element.getElementsByClassName('rounded-l')[0].value = "";
				});
				getCart();
			} else {
				warning.classList.remove('hidden');
				var coll = document.getElementsByClassName("collapsible");
				for (let i = 0; i < coll.length; i++) {
					coll[i].click();
					coll[i].click();
				}
			}
		})
		.catch((error) => {
			createFancyAlert('error', errorString, error.toString());
			getCart();
		});
		Array.from(forms).forEach((element) => {
		const refreshBtn = element.getElementsByClassName('rounded-r')[0];
		refreshBtn.innerHTML = '<i class="fal fa-check"></i>';
		refreshBtn.disabled = false;
	});
	return false;
}

async function removeCoupon(refresh = false) {
	await fetch(couponRemoveUrl, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
	})
		.then(response => response.json())
		.then((data) => {
			data = data['data'];
			if (data['success']){
				if (refresh) {
					location.reload();
				}
				getCart();
			} else {
				warning.classList.remove('hidden');
				var coll = document.getElementsByClassName("collapsible");
				for (let i = 0; i < coll.length; i++) {
					coll[i].click();
					coll[i].click();
				}
			}
		})
		.catch((error) => {
			createFancyAlert('error', errorString, error.toString());
			getCart();
		});
	return false;
}