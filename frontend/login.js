(() => {
  const tabs = document.querySelectorAll('.auth-tab');
  const form = document.querySelector('#authForm');
  const title = document.querySelector('#formTitle');
  const eyebrow = document.querySelector('#formEyebrow');
  const subtitle = document.querySelector('#formSubtitle');
  const submit = document.querySelector('#submitButton');
  const terms = document.querySelector('#termsRow');
  const message = document.querySelector('#authMessage');
  const password = document.querySelector('#password');
  const forgot = document.querySelector('#forgotLink');
  let mode = 'login';

  function setMode(nextMode) {
    mode = nextMode;
    const registering = mode === 'register';
    tabs.forEach((tab) => {
      const active = tab.dataset.mode === mode;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', String(active));
    });
    eyebrow.textContent = registering ? 'A NEW FIELD NOTEBOOK' : 'WELCOME BACK';
    title.innerHTML = registering ? 'Let curiosity <em>in.</em>' : 'Come on <em>in.</em>';
    subtitle.textContent = registering ? 'Create an account to save your discoveries.' : 'Your field notes are waiting.';
    submit.innerHTML = registering ? 'Create account <span aria-hidden="true">↗</span>' : 'Log in <span aria-hidden="true">↗</span>';
    terms.hidden = !registering;
    forgot.hidden = registering;
    password.autocomplete = registering ? 'new-password' : 'current-password';
    message.textContent = '';
    message.classList.remove('is-error');
  }

  tabs.forEach((tab) => tab.addEventListener('click', () => setMode(tab.dataset.mode)));
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    message.classList.remove('is-error');
    message.textContent = 'Account access is a frontend demo. Continue to the plant guide.';
    window.setTimeout(() => { window.location.href = 'identify.html'; }, 700);
  });
  forgot.addEventListener('click', (event) => {
    event.preventDefault();
    message.classList.remove('is-error');
    message.textContent = 'Password recovery will be available when account services are connected.';
  });
})();
