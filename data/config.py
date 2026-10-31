"""Site settings. Set CONTACT_EMAIL once the mailbox exists: the request form then shows a 'Send by e-mail' button."""
SITE = "https://www.easycliniccenter.com"   # final domain (canonical URLs, sitemap, social cards)
CONTACT_EMAIL = "info@easycliniccenter.com"
# Form service: the request is POSTed here and delivered to the mailbox. Empty = local summary + mailto only.
# FormSubmit needs no account; the first submission sends an activation e-mail to the address in the URL.
FORM_ENDPOINT = "https://formsubmit.co/ajax/info@easycliniccenter.com"
# Attachments are NOT delivered by the free FormSubmit AJAX endpoint (tested 2026-10-31: mail arrived without files).
# Turn on only after a backend that really forwards files exists (e.g. a PHP script on the mail hosting).
ATTACHMENTS_ENABLED = False
# Google Search Console ownership file (URL-prefix property, HTML file method). Keep it: Google re-checks it.
GOOGLE_VERIFICATION_FILE = "googlefd2fd1dc4d730845.html"
# Google Analytics 4 measurement ID. Loaded ONLY after the visitor accepts the cookie banner.
GA_ID = "G-23CYTMPX81"
# IndexNow (Bing and others): the key file is served at /<key>.txt; the key is public by design.
INDEXNOW_KEY = "1a8d8f73a9e234ae7e05328293e9f45d"
