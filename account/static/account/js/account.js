function showLoginOverlay() {
	loginOverlay.classList.add('opacity-100');
	loginOverlay.classList.remove('-z-1');
}
function hideLoginOverlay() {
	loginOverlay.classList.remove('opacity-100');
	setTimeout(function(){
		loginOverlay.classList.add('-z-1');
	}, 500);
}
function showLogin() {
	loginContent.classList.remove('hidden');
}
function hideLogin() {
	loginContent.classList.add('hidden');
}
function showRegister() {
	registerContent.classList.remove('hidden');
}
function hideRegister() {
	registerContent.classList.add('hidden');
}
function showReset() {
	resetContent.classList.remove('hidden');
}
function hideReset() {
	resetContent.classList.add('hidden');
}
async function submitLoginForm(form) {
	const prev = loginBtn.innerHTML;
	loginBtn.innerHTML = '';
	loginBtn.disabled = true;
	loginBtn.classList.add('btn-loading');
	loginBtn.appendChild(getSpinnerDots('bg-white'));
	const dataForm = new FormData();
	dataForm.append('email', loginEmail.value);
	dataForm.append('password', loginPassword.value);
	dataForm.append('csrfmiddlewaretoken', form.firstElementChild.value);
	await fetch(loginUrl, {
		method: 'POST',
		body: dataForm,
	})
		.then(response => response.json())
		.then((data) => {
			data = data['data'];
			if (data['success']){
				location.reload();
			} else {
				if (data['error']) {
					loginError.innerHTML = data['error'];
					loginError.classList.remove('hidden');
				}
			}
		})
		.catch((error) => {
			createFancyAlert('error', errorString, error.toString());
		});
	loginBtn.disabled = false;
	loginBtn.innerHTML = prev;
	return false;
}
async function submitRegisterForm(form) {
	const prev = registerBtn.innerHTML;
	registerBtn.innerHTML = '';
	registerBtn.disabled = true;
	registerBtn.classList.add('btn-loading');
	registerBtn.appendChild(getSpinnerDots('bg-white'));
	const dataForm = new FormData();
	dataForm.append('email', registerEmail.value);
	dataForm.append('password', registerPassword.value);
	dataForm.append('password2', registerPassword2.value);
	dataForm.append('csrfmiddlewaretoken', form.firstElementChild.value);
	if (registerPassword.value != registerPassword2.value) {
		registerPassword.style.border = '1px solid red';
		registerPasswordError.innerHTML = passwordsDontMatchError;
		registerPassword2.style.border = '1px solid red';
		registerPassword2Error.innerHTML = passwordsDontMatchError;
		return false;
	}
	await fetch(registerUrl, {
		method: 'POST',
		body: dataForm,
	})
		.then(response => response.json())
		.then((data) => {
			data = data['data'];
			if (data['success']){
				location.reload();
			} else {
				if (data['errors']['email']) {
					registerEmail.style.border = '1px solid red';
					registerEmailError.innerHTML = data['errors']['email'];
				}
				if (data['errors']['password']) {
					registerPassword.style.border = '1px solid red';
					registerPasswordError.innerHTML = data['errors']['password'];
				}
				if (data['errors']['password2']) {
					registerPassword2.style.border = '1px solid red';
					registerPassword2Error.innerHTML = data['errors']['password2'];
				}
			}
		})
		.catch((error) => {
			createFancyAlert('error', errorString, error.toString());
		});
	registerBtn.disabled = false;
	registerBtn.innerHTML = prev;
	return false;
}
async function submitResetForm(form) {
	const prev = resetBtn.innerHTML;
	resetBtn.innerHTML = '';
	resetBtn.disabled = true;
	resetBtn.classList.add('btn-loading');
	resetBtn.appendChild(getSpinnerDots('bg-white'));
	const dataForm = new FormData();
	dataForm.append('email', resetEmail.value);
	dataForm.append('csrfmiddlewaretoken', form.firstElementChild.value);
	await fetch(resetUrl, {
		method: 'POST',
		body: dataForm,
	})
		.then(() => {
			resetEmail.classList.remove('input-error');
			resetSuccess.innerHTML = resetSuccessText;
			resetEmailError.innerHTML = '';
			resetSuccess.classList.remove('hidden');
		})
		.catch((error) => {
			console.log(error);
			resetEmail.classList.remove('input-error');
			resetEmailError.innerHTML = error;
			resetSuccess.classList.add('hidden');
		});
	resetBtn.disabled = false;
	resetBtn.innerHTML = prev;
	return false;
}