/* ============================================================
   SITE SETTINGS: the only file that needs editing to switch on
   the booking calendar and the mailing list.
   ============================================================ */
window.SITE_CONFIG = {
  // Where form submissions go until MailerLite is connected
  // (opens a pre-filled email to this address).
  contactEmail: 'drkarendhamilton@gmail.com',

  // Calendly scheduling link, e.g. 'https://calendly.com/your-name/discovery-call'
  // Leave '' until the Calendly account exists.
  calendlyUrl: '',

  // MailerLite. Fill these in once the account exists.
  // accountId: the number in your MailerLite embed code (.../jsonp/<accountId>/forms/...)
  // forms: one MailerLite form ID per website form (data-group on each form).
  mailerlite: {
    accountId: '',
    forms: {
      'Early Readers': '',
      'Book Clubs': '',
      'Speaking Inquiries': '',
      'Workshop Inquiries': '',
      'Coaching Inquiries': '',
      'Booking Requests': ''
    }
  }
};
