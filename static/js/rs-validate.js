/**
 * Royal Smoke — клієнтська валідація форм.
 * Підключення: <form data-rs-validate novalidate>
 * Поля: data-rs-rule="name|email|password|phone|url|required"
 * Опційні: data-rs-optional="1"
 * Чекбокс: data-rs-checkbox="1"
 *
 * UX: onBlur одразу; onChange після першого submit; submit завжди клікабельний,
 * при помилках — показ усіх помилок і блокування відправки.
 */
(function (global) {
  'use strict';

  var MSG = {
    required: 'Це поле обовʼязкове',
    requiredCheckbox: 'Підтвердіть цю опцію',
    whitespace: 'Поле не може складатися лише з пробілів',
    nameMin: 'Імʼя має містити мінімум 2 символи',
    nameChars: 'Імʼя може містити лише літери, пробіли, дефіс і апостроф',
    email: 'Введіть коректну електронну пошту',
    passwordMin: 'Пароль має містити мінімум 8 символів',
    passwordUpper: 'Пароль має містити хоча б одну велику літеру',
    passwordLower: 'Пароль має містити хоча б одну малу літеру',
    passwordDigit: 'Пароль має містити хоча б одну цифру',
    passwordSpecial: 'Пароль має містити хоча б один спеціальний символ',
    phone: 'Введіть коректний номер телефону',
    url: 'Введіть коректну URL-адресу'
  };

  (function loadI18n() {
    var el = document.getElementById('rs-i18n-validate');
    if (!el) return;
    try {
      var data = JSON.parse(el.textContent || '{}');
      Object.keys(data).forEach(function (k) {
        if (data[k]) MSG[k] = data[k];
      });
    } catch (e) { /* keep defaults */ }
  })();

  var NAME_RE = /^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'ʼ\- ]+$/;
  var EMAIL_RE = /^(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|\[(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?|[a-zA-Z\-0-9]*[a-zA-Z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/;
  var PHONE_RE = /^\+?[\d\s\-()./]{7,25}$/;
  var SPECIAL_RE = /[^A-Za-z0-9]/;

  function isBlank(el) {
    if (!el) return true;
    if (el.type === 'checkbox' || el.type === 'radio') return !el.checked;
    return String(el.value || '').trim() === '';
  }

  function isOptional(el) {
    return el.getAttribute('data-rs-optional') === '1' || el.getAttribute('data-rs-optional') === 'true';
  }

  function isCheckboxRule(el) {
    return el.getAttribute('data-rs-checkbox') === '1' || el.type === 'checkbox';
  }

  function validateValue(rule, el) {
    var optional = isOptional(el);
    var raw = el.type === 'checkbox' ? el.checked : String(el.value || '');

    if (rule === 'required' || (el.required && !rule)) {
      if (isCheckboxRule(el)) {
        return el.checked ? '' : MSG.requiredCheckbox;
      }
      if (String(el.value || '') !== '' && String(el.value).trim() === '') {
        return MSG.whitespace;
      }
      return isBlank(el) ? MSG.required : '';
    }

    if (optional && isBlank(el)) return '';

    if (!optional && isBlank(el)) {
      return isCheckboxRule(el) ? MSG.requiredCheckbox : MSG.required;
    }

    var text = String(el.value || '').trim();
    var pass = String(el.value || '');

    switch (rule) {
      case 'name':
        if (text.length < 2) return MSG.nameMin;
        if (!NAME_RE.test(text)) return MSG.nameChars;
        return '';
      case 'email':
        if (text.length > 254 || !EMAIL_RE.test(text)) return MSG.email;
        return '';
      case 'password':
        if (pass.length < 8) return MSG.passwordMin;
        if (!/[A-Z]/.test(pass)) return MSG.passwordUpper;
        if (!/[a-z]/.test(pass)) return MSG.passwordLower;
        if (!/\d/.test(pass)) return MSG.passwordDigit;
        if (!SPECIAL_RE.test(pass)) return MSG.passwordSpecial;
        return '';
      case 'phone': {
        if (!PHONE_RE.test(text)) return MSG.phone;
        var digits = text.match(/\d/g) || [];
        if (digits.length < 7 || digits.length > 15) return MSG.phone;
        return '';
      }
      case 'url':
        if (text.charAt(0) === '/' && text.indexOf('//') !== 0) return '';
        try {
          // iOS Safari: URL ctor підтримує абсолютні URL
          // eslint-disable-next-line no-new
          new URL(text);
          return '';
        } catch (e) {
          return MSG.url;
        }
      default:
        return '';
    }
  }

  function fieldWrap(el) {
    return el.closest('.rs-field')
      || el.closest('.rs-svc-card__field')
      || el.closest('.rs-check')
      || el.parentElement;
  }

  function ensureErrorEl(wrap) {
    var err = wrap.querySelector('[data-rs-error], .rs-field__error');
    if (!err) {
      err = document.createElement('p');
      err.className = 'rs-field__error';
      err.setAttribute('data-rs-error', '');
      err.setAttribute('hidden', '');
      wrap.appendChild(err);
    }
    return err;
  }

  function setInvalid(el, message) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    var err = ensureErrorEl(wrap);
    if (message) {
      wrap.classList.add('is-invalid');
      el.setAttribute('aria-invalid', 'true');
      err.textContent = message;
      err.removeAttribute('hidden');
    } else {
      wrap.classList.remove('is-invalid');
      el.removeAttribute('aria-invalid');
      err.textContent = '';
      err.setAttribute('hidden', '');
    }
  }

  function clearServerErrorFlag(el) {
    if (el && el.getAttribute('data-rs-server-error') === '1') {
      el.removeAttribute('data-rs-server-error');
    }
  }

  function controllable(el) {
    return el && el.matches && el.matches('input, select, textarea');
  }

  function fieldsOf(form) {
    return Array.prototype.slice.call(
      form.querySelectorAll('[data-rs-rule], input[required], select[required], textarea[required]')
    ).filter(function (el) {
      return controllable(el) && !el.disabled;
    });
  }

  function validateField(el) {
    var rule = el.getAttribute('data-rs-rule') || (el.required ? 'required' : '');
    if (!rule) {
      setInvalid(el, '');
      return true;
    }
    var message = validateValue(rule, el);
    setInvalid(el, message);
    return !message;
  }

  function validateForm(form) {
    var ok = true;
    var firstBad = null;
    fieldsOf(form).forEach(function (el) {
      if (!validateField(el)) {
        ok = false;
        if (!firstBad) firstBad = el;
      }
    });
    return { ok: ok, firstBad: firstBad };
  }

  function bindForm(form) {
    if (form.getAttribute('data-rs-bound') === '1') return;
    form.setAttribute('data-rs-bound', '1');
    form.setAttribute('novalidate', '');

    var submitted = false;

    fieldsOf(form).forEach(function (el) {
      var wrap = fieldWrap(el);
      if (wrap && wrap.classList.contains('is-invalid')) {
        el.setAttribute('data-rs-server-error', '1');
      }
    });

    form.addEventListener('focusout', function (e) {
      var el = e.target;
      if (!controllable(el) || !form.contains(el)) return;
      if (!el.getAttribute('data-rs-rule') && !el.required) return;
      if (el.getAttribute('data-rs-server-error') === '1') return;
      validateField(el);
    }, true);

    form.addEventListener('input', function (e) {
      var el = e.target;
      if (!controllable(el) || !form.contains(el)) return;
      clearServerErrorFlag(el);
      if (!submitted) return;
      if (!el.getAttribute('data-rs-rule') && !el.required) return;
      validateField(el);
    });

    form.addEventListener('change', function (e) {
      var el = e.target;
      if (!controllable(el) || !form.contains(el)) return;
      clearServerErrorFlag(el);
      if (!submitted) return;
      if (!el.getAttribute('data-rs-rule') && !el.required) return;
      validateField(el);
    });

    form.addEventListener('submit', function (e) {
      submitted = true;
      fieldsOf(form).forEach(clearServerErrorFlag);
      var result = validateForm(form);
      if (!result.ok) {
        e.preventDefault();
        e.stopPropagation();
        if (result.firstBad && typeof result.firstBad.focus === 'function') {
          try {
            result.firstBad.focus({ preventScroll: false });
          } catch (err) {
            result.firstBad.focus();
          }
        }
      }
    });
  }

  function init(root) {
    var scope = root || document;
    Array.prototype.slice.call(scope.querySelectorAll('form[data-rs-validate]')).forEach(bindForm);
  }

  global.RsValidate = {
    init: init,
    bindForm: bindForm,
    validateForm: validateForm,
    validateField: validateField,
    messages: MSG
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { init(); });
  } else {
    init();
  }
})(window);
