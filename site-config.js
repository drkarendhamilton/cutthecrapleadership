/* ============================================================
   SITE SETTINGS: the only file that needs editing to switch on
   the booking calendar and the mailing list.
   ============================================================ */
window.SITE_CONFIG = {
  // Where form submissions go until MailerLite is connected
  // (opens a pre-filled email to this address).
  contactEmail: 'drkarendhamilton@gmail.com',

  // Google Calendar booking page (opens in a new tab)
  bookingUrl: 'https://calendar.app.google/11XNmBU3vB7Axv6A8',
  // Optional: the src="..." URL from Google Calendar > Share > Website embed
  // (ends in ?gv=true). When filled in, the calendar shows right on the page.
  bookingEmbedUrl: 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ0138OZEF2qiYvdLpVYCwUinw49iTrsXyHHaBOZr4dAtjYShjx-8jumR-Te5F_VnP9uKpWR03VZ?gv=true',
  calendlyUrl: '',

  // Where to buy. Paste each store link as it goes live; empty = "Coming soon".
  buyLinks: {
    directEbook: '',      // Payhip product link for the e-book
    directSigned: '',     // Payhip product link for signed paperbacks
    amazonPaperback: '',
    kindle: '',
    appleBooks: '',
    kobo: '',
    nook: ''
  },

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
