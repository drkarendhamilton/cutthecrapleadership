/* Handles every .lead-form on the site and the Calendly embed.
   Settings come from site-config.js. */
(function () {
  var cfg = window.SITE_CONFIG || {};
  var ml = cfg.mailerlite || {};

  // ---------- Calendly ----------
  var slot = document.getElementById('booking');
  if (slot && cfg.bookingEmbedUrl) {
    slot.innerHTML = '<iframe src="' + cfg.bookingEmbedUrl + '" title="Schedule a call with Karen" loading="lazy"></iframe>';
    slot.style.padding = '0';
  } else if (slot && cfg.bookingUrl) {
    slot.innerHTML = '<p class="note">Choose a time for a free 30-minute discovery call with Dr. Karen Hamilton. Your confirmation email will include a Google Meet link.</p>' +
      '<a class="btn" href="' + cfg.bookingUrl + '" target="_blank" rel="noopener">See Available Times</a>' +
      '<p class="note" style="font-size:13px">After you book, add your details in the request form below so Karen can prepare.</p>';
  } else if (slot && cfg.calendlyUrl) {
    var u = cfg.calendlyUrl + (cfg.calendlyUrl.indexOf('?') > -1 ? '&' : '?') +
      'hide_gdpr_banner=1&background_color=ffffff&text_color=3b302a&primary_color=a8703f';
    slot.innerHTML = '<iframe src="' + u + '" title="Schedule a call with Karen" loading="lazy"></iframe>';
    slot.style.padding = '0';
  }

  // ---------- Forms ----------
  function label(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    var lab = el && form.querySelector('label[for="' + el.id + '"]');
    return lab ? lab.textContent.replace(/\s*\*$/, '') : name;
  }

  function sendMailerLite(form, data) {
    var formId = ml.forms && ml.forms[form.dataset.group];
    if (!ml.accountId || !formId) return false;
    var body = new URLSearchParams();
    Object.keys(data).forEach(function (k) {
      if (k === 'newsletter') return;
      var key = k === 'first_name' ? 'name' : k;
      body.append('fields[' + key + ']', data[k]);
    });
    body.append('fields[inquiry_type]', form.dataset.kind);
    body.append('ml-submit', '1');
    body.append('anticsrf', 'true');
    fetch('https://assets.mailerlite.com/jsonp/' + ml.accountId + '/forms/' + formId + '/subscribe',
      { method: 'POST', body: body, mode: 'no-cors' });
    return true;
  }

  function sendEmail(form, data) {
    var lines = ['New ' + form.dataset.kind + ' from the website', ''];
    Object.keys(data).forEach(function (k) {
      if (data[k]) lines.push(label(form, k) + ': ' + data[k]);
    });
    var subject = form.dataset.kind + ' - ' + (data.name || data.first_name || '') + (data.organization ? ' (' + data.organization + ')' : '');
    window.location.href = 'mailto:' + (cfg.contactEmail || '') +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
  }

  document.querySelectorAll('form.lead-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = null;
      form.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.value.trim() && (el.type !== 'email' || /\S+@\S+\.\S+/.test(el.value));
        el.style.borderColor = ok ? '' : '#b23224';
        if (!ok && !bad) bad = el;
      });
      if (bad) { bad.focus(); return; }
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = String(v).trim(); });
      if (!data.newsletter) data.newsletter = 'no';
      if (!sendMailerLite(form, data)) sendEmail(form, data);
      form.classList.add('sent');
      form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
})();
