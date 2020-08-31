document.addEventListener("DOMContentLoaded", main);

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

const handleMessageSuccess = (data) => console.log(data);

const handleMessageError = (data) => console.log(data);

const sendMessage = (formData) => {
  const url = `${window.location.origin}/message`;
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

const submitForm = (e) => {
  e.preventDefault();
  const nameField = document.querySelector("input[name=name]");
  const emailField = document.querySelector("input[name=email]");
  const messageField = document.querySelector("textarea[name=message]");

  const isValidEmail = emailField && emailField.checkValidity();
  const nameAndMessageFieldsHaveData = (
    nameField && nameField.checkValidity() &&
    messageField && messageField.checkValidity()
  );

  if (isValidEmail && nameAndMessageFieldsHaveData) {
    // make form button unclickable
    sendMessage({
      name: nameField.value,
      email: emailField.value,
      message: messageField.value,
    }).then((resp) => {
      // flash message success
      // clear form
      // make button clickable
      // send confirmation email to form submitter???
      console.log(resp);
    }).catch((resp) => {
      // flash error message
      // make button clickable
      console.log(resp);
    });
  } else {
    if (!isValidEmail) {
      // flash message that email is invalid
    } else if (!nameAndMessageFieldsHaveData) {
      // flash message that both name and message fields must have values
    }
  }
};

function main() {
  const sections = document.querySelectorAll("section");

  const selector = document.querySelector(".select");

  const options = {
    threshold: .7,
  };

  const selectorFn = select(selector);

  observe(sections, selectorFn, options);

  const submitButton = document.querySelector("input[type=submit]");
  submitButton.onclick = submitForm;

  const projectImages = document.querySelectorAll(".card-image");

  Array.from(projectImages).forEach((el) => {
    el.onerror = ({ target }) => {
      target.src = `https://plchldr.co/i/200`;
      target.style.padding = ".5em";
    };
  });

  window.onresize = () => observe(sections, selectorFn, options);
}
