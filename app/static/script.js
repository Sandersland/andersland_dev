const IMAGE_PLACEHOLDER = "https://plchldr.co/i/200";
const MESSAGE_ENDPOINT = "api/message";

const FormElement = {
  ALL: "form > *[name]",
  NAME_FIELD: "input[name=name]",
  EMAIL_FIELD: "input[name=email]",
  SUBJECT_FIELD: "input[name=subject]",
  MESSAGE_FIELD: "textarea[name=message]",
  SUBMIT_BUTTON: "input[type=submit]",
  LOADER: ".loader",
  VALIDATION_MESSAGE: ".validation-message",
};

const FormValidityMessage = {
  valueMissing: (fieldName) =>
    `Please enter a value for the ${fieldName} field.`,
  typeMismatch: (fieldName) =>
    `Please enter a correct value for the ${fieldName} field.`,
};

const getLeftOffset = (selectorText) => {
  const ruleArr = Array.from(document.styleSheets[0].rules);
  const container = ruleArr.find((rule) => rule.selectorText === selectorText);
  const containerWidth = (100 - parseInt(container.style.width)) / 100;
  const multiplier = containerWidth / 2;
  return window.innerWidth * multiplier;
};

const moveSelector = (selector, { top, left, height, width }) => {
  const leftOffset = getLeftOffset(".container");
  selector.style.setProperty("left", `${left - leftOffset}px`);
  selector.style.setProperty("top", `${top}px`);
  selector.style.setProperty("height", `${height}px`);
  selector.style.setProperty("width", `${width}px`);
};

const select = (selector) =>
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const className = entry.target.className;
        const active = document.querySelector(`[data-page=${className}]`);
        const coords = active.getBoundingClientRect();
        moveSelector(selector, coords);
      }
    });
  };

const observe = (observables, callback, options) => {
  const observer = new IntersectionObserver(callback, options);
  observables.forEach((el) => observer.observe(el));
  return observer;
};

const sendMessage = (formData) => {
  const url = `${window.location.origin}/${MESSAGE_ENDPOINT}`;
  const response = fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  return new Promise((resolve, reject) => {
    response.then((res) => res.json())
      .then(resolve)
      .catch(reject);
  });
};

const flashMessage = (message) => {
  const validationMessageField = document.querySelector(
    FormElement.VALIDATION_MESSAGE,
  );
  validationMessageField.classList.add("visible");
  validationMessageField.textContent = message;
};

const flashValidationMessage = (field) => {
  for (let key in field.validity) {
    const result = field.validity[key];
    if (result && key !== "valid") {
      const message = FormValidityMessage[key](field.name);
      flashMessage(message);
    }
  }
};

const handleMessageSuccess = (data) => {
  const submitButton = document.querySelector(FormElement.SUBMIT_BUTTON);
  document.querySelector(FormElement.LOADER).classList.remove("visible");
  document.querySelector(FormElement.NAME_FIELD).value = "";
  document.querySelector(FormElement.EMAIL_FIELD).value = "";
  document.querySelector(FormElement.SUBJECT_FIELD).value = "";
  document.querySelector(FormElement.MESSAGE_FIELD).value = "";
  submitButton.disabled = false;
  submitButton.style.cursor = "pointer";

  flashMessage(data.message);
};

const handleMessageError = (data) => {
  const submitButton = document.querySelector(FormElement.SUBMIT_BUTTON);
  document.querySelector(FormElement.LOADER).classList.remove("visible");
  submitButton.disabled = false;
  submitButton.style.cursor = "pointer";

  console.log(data);
  flashMessage("Something unexpected happened while sending your message.");
};

const debounce = (func, wait, immediate) => {
  var timeout;
  return function () {
    var context = this, args = arguments;
    var later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

const clearValidationMessage = debounce((_) => {
  const validationMessageField = document.querySelector(
    FormElement.VALIDATION_MESSAGE,
  );
  validationMessageField.classList.remove("visible");
}, 5000);

const validateField = (e) => {
  const field = e.target;
  const fieldIsValid = field.checkValidity();

  if (!fieldIsValid) {
    field.setAttribute("data-invalid", "");
    flashValidationMessage(field);
  }
};

const validateForm = () => {
  const form = document.querySelector("form");
  return form.checkValidity();
};

const clearError = (e) => {
  e.target.removeAttribute("data-invalid");
};

const submitForm = (e) => {
  e.preventDefault();

  const submitButton = document.querySelector(FormElement.SUBMIT_BUTTON);
  const loader = document.querySelector(FormElement.LOADER);
  const formIsValid = validateForm();

  if (formIsValid) {
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";

    loader.classList.add("visible");
    sendMessage({
      name: document.querySelector(FormElement.NAME_FIELD).value,
      email: document.querySelector(FormElement.EMAIL_FIELD).value,
      subject: document.querySelector(FormElement.SUBJECT_FIELD).value,
      message: document.querySelector(FormElement.MESSAGE_FIELD).value,
    }).then(handleMessageSuccess).catch(handleMessageSuccess);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("section");

  const selector = document.querySelector(".select");

  const options = {
    threshold: .7,
  };

  const selectorFn = select(selector);

  observe(sections, selectorFn, options);

  const submitButton = document.querySelector(FormElement.SUBMIT_BUTTON);
  submitButton.onclick = submitForm;

  Array.from(document.querySelectorAll(".card-image")).forEach((el) => {
    el.onerror = ({ target }) => {
      target.src = IMAGE_PLACEHOLDER;
      target.style.padding = ".5em";
    };
  });

  const inputFields = Array.from(document.querySelectorAll(FormElement.ALL));
  inputFields.forEach((el) => {
    el.addEventListener("input", clearError);
    el.addEventListener("focusout", validateField);
    el.addEventListener("focusout", clearValidationMessage);
  });

  window.onresize = observe(sections, selectorFn, options);
});
