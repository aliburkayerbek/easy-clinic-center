"""Site settings. Set CONTACT_EMAIL once the mailbox exists: the request form then shows a 'Send by e-mail' button."""
SITE = "https://www.easycliniccenter.com"   # final domain (canonical URLs, sitemap, social cards)
CONTACT_EMAIL = "info@easycliniccenter.com"
# Form service: the request is POSTed here and delivered to the mailbox. Empty = local summary + mailto only.
# FormSubmit needs no account; the first submission sends an activation e-mail to the address in the URL.
FORM_ENDPOINT = "https://formsubmit.co/ajax/info@easycliniccenter.com"
