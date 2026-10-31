"""Strings added or overridden for the simplified site (free first second opinion, one-step form, blog teaser).
Each value is a tuple (EN, FR, AR, RU); merged over web_strings.S by build_site.py."""

S2 = {
 # nav / calls to action
 "nav_blog": ("Blog", "Blog", "المدونة", "Блог"),
 "nav_apply": ("Get an opinion", "Obtenir un avis", "احصل على رأي", "Получить мнение"),
 "m_apply": ("Request an opinion", "Demander un avis", "اطلب رأيًا طبيًا", "Запросить мнение"),
 "cta_second": ("Request a second opinion", "Demander un second avis", "اطلب رأيًا طبيًا ثانيًا", "Запросить второе мнение"),

 # hero
 "h_eb": ("Second opinions from $30", "Seconds avis dès 30 USD", "رأي طبي ثانٍ ابتداءً من 30 دولارًا", "Второе мнение от 30 $"),
 "h_h1": ("A physician’s second opinion, <em>from $30</em>", "Le second avis d’un médecin, <em>dès 30 USD</em>", "رأي طبيب ثانٍ، <em>ابتداءً من 30 دولارًا</em>", "Второе мнение врача — <em>от 30 $</em>"),
 "h_p": ("Tell us about your case and send your records. A specialist physician reviews them and writes you a clear report.", "Décrivez-nous votre cas et envoyez vos documents. Un médecin spécialiste les examine et vous rédige un rapport clair.", "أخبرنا بحالتك وأرسل سجلاتك، ويراجعها طبيب أخصائي ويكتب لك تقريرًا واضحًا.", "Расскажите о вашем случае и пришлите документы. Врач-специалист изучит их и напишет понятное заключение."),
 "h_c1": ("Written physician report", "Rapport écrit d’un médecin", "تقرير مكتوب من طبيب", "Письменное заключение врача"),
 "h_c2": ("Request in 2 minutes", "Demande en 2 minutes", "اطلب في دقيقتين", "Заявка за 2 минуты"),
 "h_c3": ("From $30", "Dès 30 USD", "ابتداءً من 30 دولارًا", "От 30 $"),
 "free_note": ("Second opinions from $30.", "Seconds avis dès 30 USD.", "رأي طبي ثانٍ ابتداءً من 30 دولارًا.", "Второе мнение от 30 $."),

 # one-step form
 "f_title": ("Request your second opinion", "Demandez votre second avis", "اطلب رأيك الطبي الثاني", "Запросите второе мнение"),
 "f_need": ("What do you need?", "De quoi avez-vous besoin ?", "ماذا تحتاج؟", "Что вам нужно?"),
 "f_name": ("Your name", "Votre nom", "اسمك", "Ваше имя"),
 "f_contact": ("E-mail or WhatsApp number", "E-mail ou numéro WhatsApp", "البريد الإلكتروني أو رقم واتساب", "E-mail или номер WhatsApp"),
 "f_msg": ("What would you like a doctor to look at?", "Sur quoi souhaitez-vous l’avis d’un médecin ?", "ما الذي تودّ أن يراجعه الطبيب؟", "Что должен оценить врач?"),
 "f_msg_h": ("A few lines are enough. You can send documents after we reply.",
             "Quelques lignes suffisent. Vous pourrez envoyer vos documents après notre réponse.",
             "يكفي بضعة أسطر. يمكنك إرسال المستندات بعد ردّنا.",
             "Достаточно нескольких строк. Документы можно отправить после нашего ответа."),
 "f_more": ("Add more details (optional)", "Ajouter des détails (facultatif)", "أضف تفاصيل أخرى (اختياري)", "Добавить подробности (необязательно)"),
 "f_photo": ("Please do not send photos that show your face.", "Merci de ne pas envoyer de photos montrant votre visage.", "يُرجى عدم إرسال صور يظهر فيها وجهك.", "Пожалуйста, не присылайте фото, на которых видно лицо."),
 "f_consent": ("I explicitly consent to Easy Clinic Center using the information I send, including any health information, to deal with my request, and to it being sent to Türkiye and handled by the service providers described in the privacy policy. I can withdraw my consent at any time. I am 18 or older (or a parent/guardian).", "Je consens expressément à ce qu’Easy Clinic Center utilise les informations que j’envoie, y compris mes données de santé, pour traiter ma demande, et à leur transfert vers la Türkiye et leur traitement par les prestataires décrits dans la politique de confidentialité. Je peux retirer mon consentement à tout moment. J’ai 18 ans ou plus (ou je suis parent/tuteur).", "أوافق صراحةً على أن يستخدم Easy Clinic Center المعلومات التي أرسلها، بما فيها أي معلومات صحية، لمعالجة طلبي، وعلى إرسالها إلى تركيا ومعالجتها لدى مزوّدي الخدمات الموضّحين في سياسة الخصوصية. يمكنني سحب موافقتي في أي وقت. عمري 18 عامًا أو أكثر (أو أنا أحد الوالدين/الوصي).", "Я прямо соглашаюсь, чтобы Easy Clinic Center использовал присланные мной сведения, включая данные о здоровье, для рассмотрения моей заявки, а также на их передачу в Турцию и обработку поставщиками услуг, указанными в политике конфиденциальности. Я могу отозвать согласие в любой момент. Мне 18 лет или больше (либо я родитель/опекун)."),
 "f_submit": ("Send my request", "Envoyer ma demande", "أرسل طلبي", "Отправить заявку"),
 "f_mail": ("Send by e-mail", "Envoyer par e-mail", "إرسال بالبريد الإلكتروني", "Отправить по e-mail"),
 "err_contact": ("Enter an e-mail address or a phone number with country code (+...).",
                 "Saisissez une adresse e-mail ou un numéro avec indicatif (+...).",
                 "أدخل بريدًا إلكترونيًا أو رقم هاتف مع رمز الدولة (+...).",
                 "Введите e-mail или номер телефона с кодом страны (+...)."),

 # trust strip
 "tr1": ("Second opinions from $30", "Seconds avis dès 30 USD", "رأي ثانٍ ابتداءً من 30 دولارًا", "Второе мнение от 30 $"),
 "tr3": ("Your data is used only for your request", "Vos données ne servent qu’à votre demande", "تُستخدم بياناتك لطلبك فقط", "Данные используются только для вашей заявки"),

 # blog teaser
 "blog_eb": ("Guides", "Guides", "أدلة", "Руководства"),
 "blog_h2": ("Clear answers before you decide", "Des réponses claires avant de décider", "إجابات واضحة قبل أن تقرر", "Понятные ответы до принятия решения"),
 "blog_all": ("All articles (English)", "Tous les articles (en anglais)", "كل المقالات (بالإنجليزية)", "Все статьи (на английском)"),
 "blog_read": ("Read article", "Lire l’article", "اقرأ المقال", "Читать статью"),

 # closing call to action
 "cta2_h": ("Ready? Send your request in two minutes.", "Prêt ? Envoyez votre demande en deux minutes.", "جاهز؟ أرسل طلبك في دقيقتين.", "Готовы? Отправьте заявку за две минуты."),

 # FAQ
 "q8": ("How much does a second opinion cost?", "Combien coûte un second avis ?", "كم تبلغ تكلفة الرأي الطبي الثاني؟", "Сколько стоит второе мнение?"),
 "a8": ("Second opinions start from $30. We confirm the price for your case when we reply to you.", "Les seconds avis commencent à 30 USD. Nous vous confirmons le prix pour votre cas dans notre réponse.", "تبدأ تكلفة الرأي الطبي الثاني من 30 دولارًا، ونؤكد لك السعر الخاص بحالتك عند ردّنا عليك.", "Второе мнение стоит от 30 $. Цену для вашего случая мы подтвердим в ответе."),
 # request sent by e-mail (mailbox is live)
 "res_p": ("Your request is ready. Press “Send by e-mail” to open your mail app with it, or copy or save the summary and send it with your documents and photos (without your face). This website does not store your information.",
           "Votre demande est prête. Cliquez sur « Envoyer par e-mail » pour ouvrir votre messagerie, ou copiez ou enregistrez le résumé et envoyez-le avec vos documents et photos (sans visage). Ce site ne conserve pas vos informations.",
           "طلبك جاهز. اضغط «إرسال بالبريد الإلكتروني» لفتح تطبيق البريد لديك، أو انسخ الملخص أو احفظه وأرسله مع مستنداتك وصورك (دون إظهار الوجه). هذا الموقع لا يحتفظ بمعلوماتك.",
           "Заявка готова. Нажмите «Отправить по e-mail», чтобы открыть почтовое приложение, или скопируйте либо сохраните сводку и отправьте её с документами и фото (без лица). Сайт не хранит ваши данные."),
 "ft_contact_v": ('<a href="mailto:info@easycliniccenter.com">info@easycliniccenter.com</a>',) * 4,
 "mail_note": ("Attachments (reports, scans) can be added in your mail app before sending.",
               "Vous pouvez joindre vos documents (rapports, imageries) dans votre messagerie avant l’envoi.",
               "يمكنك إضافة المرفقات (التقارير والصور الطبية) في تطبيق البريد قبل الإرسال.",
               "Вложения (заключения, снимки) можно добавить в почтовом приложении перед отправкой."),
 # automatic delivery through the form service
 "form_reassure": ("No payment is taken. When you press the button, your request is e-mailed to our team through a form service.",
                   "Aucun paiement n’est demandé. En cliquant sur le bouton, votre demande est envoyée par e-mail à notre équipe via un service de formulaire.",
                   "لا يتم أي دفع. عند الضغط على الزر يُرسل طلبك بالبريد الإلكتروني إلى فريقنا عبر خدمة نماذج.",
                   "Оплата не взимается. При нажатии кнопки заявка отправляется нашей команде по e-mail через сервис форм."),
 "sending": ("Sending…", "Envoi en cours…", "جارٍ الإرسال…", "Отправка…"),
 "sent_h": ("Your request has been sent", "Votre demande a été envoyée", "تم إرسال طلبك", "Ваша заявка отправлена"),
 "sent_p": ("We have received your request and will reply to the e-mail address or number you gave. Please keep your reference. Send your documents and photos (without your face) by replying to our e-mail.",
            "Nous avons reçu votre demande et répondrons à l’e-mail ou au numéro indiqué. Conservez votre référence. Envoyez vos documents et photos (sans visage) en répondant à notre e-mail.",
            "استلمنا طلبك وسنردّ على البريد الإلكتروني أو الرقم الذي زوّدتنا به. احتفظ برقم المرجع. أرسل مستنداتك وصورك (دون إظهار الوجه) بالرد على بريدنا.",
            "Мы получили вашу заявку и ответим на указанный e-mail или номер. Сохраните номер заявки. Документы и фото (без лица) отправьте ответом на наше письмо."),
 "sent_fail": ("We could not send it automatically. Please press “Send by e-mail” below or copy the summary and send it to us.",
               "L’envoi automatique a échoué. Cliquez sur « Envoyer par e-mail » ci-dessous ou copiez le résumé et envoyez-le-nous.",
               "تعذّر الإرسال التلقائي. اضغط «إرسال بالبريد الإلكتروني» أدناه أو انسخ الملخص وأرسله إلينا.",
               "Не удалось отправить автоматически. Нажмите «Отправить по e-mail» ниже или скопируйте сводку и отправьте нам."),
 # attachments + privacy link
 "f_files": ("Photos or documents (optional)", "Photos ou documents (facultatif)", "صور أو مستندات (اختياري)", "Фото или документы (необязательно)"),
 "f_files_h": ("JPG, PNG or PDF. Up to 5 files, 8 MB in total. No photos showing your face.",
               "JPG, PNG ou PDF. 5 fichiers maximum, 8 Mo au total. Pas de photos montrant votre visage.",
               "JPG أو PNG أو PDF. حتى 5 ملفات و8 ميغابايت إجمالًا. بدون صور يظهر فيها وجهك.",
               "JPG, PNG или PDF. До 5 файлов, всего до 8 МБ. Без фото, на которых видно лицо."),
 "f_files_type": ("Only JPG, PNG or PDF files can be attached.", "Seuls les fichiers JPG, PNG ou PDF sont acceptés.", "يمكن إرفاق ملفات JPG وPNG وPDF فقط.", "Можно прикреплять только файлы JPG, PNG или PDF."),
 "f_files_size": ("These files are too large (8 MB in total). Photos are reduced automatically; for large PDFs send them by e-mail after we reply.",
                  "Ces fichiers sont trop volumineux (8 Mo au total). Les photos sont réduites automatiquement ; envoyez les gros PDF par e-mail après notre réponse.",
                  "هذه الملفات كبيرة جدًا (8 ميغابايت إجمالًا). تُصغَّر الصور تلقائيًا؛ أرسل ملفات PDF الكبيرة بالبريد بعد ردّنا.",
                  "Файлы слишком большие (всего 8 МБ). Фото уменьшаются автоматически; большие PDF отправьте по e-mail после нашего ответа."),
 "f_files_max": ("You can attach up to 5 files.", "Vous pouvez joindre 5 fichiers au maximum.", "يمكنك إرفاق 5 ملفات كحد أقصى.", "Можно прикрепить не более 5 файлов."),
 "f_files_remove": ("Remove", "Retirer", "إزالة", "Удалить"),
 "privacy_link": ("Privacy policy", "Politique de confidentialité", "سياسة الخصوصية", "Политика конфиденциальности"),
 "privacy_read": ("Read our privacy policy", "Lire notre politique de confidentialité", "اقرأ سياسة الخصوصية", "Прочитать политику конфиденциальности"),
 # legal review overrides
 "cons2": ("I explicitly consent to Easy Clinic Center processing my personal and health data, transferring it to Türkiye and to the service providers named in the privacy policy, and sharing it with partner hospitals and physicians only to assess my case and prepare a quote (UK GDPR / KVKK). I can withdraw this consent at any time.", "Je consens expressément à ce qu’Easy Clinic Center traite mes données personnelles et de santé, les transfère vers la Türkiye et vers les prestataires cités dans la politique de confidentialité, et les partage avec les hôpitaux et médecins partenaires uniquement pour évaluer mon dossier et établir un devis (RGPD britannique / KVKK). Je peux retirer ce consentement à tout moment.", "أوافق صراحةً على أن يعالج Easy Clinic Center بياناتي الشخصية والصحية، وأن ينقلها إلى تركيا وإلى مزوّدي الخدمات المذكورين في سياسة الخصوصية، وأن يشاركها مع المستشفيات والأطباء الشركاء فقط لتقييم حالتي وإعداد العرض (GDPR البريطانية / KVKK). ويمكنني سحب هذه الموافقة في أي وقت.", "Я прямо соглашаюсь на обработку Easy Clinic Center моих персональных и медицинских данных, их передачу в Турцию и поставщикам услуг, указанным в политике конфиденциальности, и передачу больницам и врачам-партнёрам только для оценки моего случая и подготовки предложения (UK GDPR / KVKK). Я могу отозвать согласие в любой момент."),
 "a1": ("Yes. Reviewing your request and explaining your options costs nothing. A physician’s written second opinion is priced separately and starts from $30.", "Oui. L’étude de votre demande et l’explication de vos options sont gratuites. Le second avis écrit d’un médecin est facturé à part, dès 30 USD.", "نعم، مراجعة طلبك وشرح خياراتك مجانًا. أما الرأي الطبي المكتوب من الطبيب فيُسعَّر بشكل منفصل ويبدأ من 30 دولارًا.", "Да. Рассмотрение заявки и объяснение вариантов бесплатны. Письменное второе мнение врача оплачивается отдельно и стоит от 30 $."),
 # cookie banner (Google Analytics only after consent)
 "cc_text": ("We would like to use Google Analytics cookies to count visits and see which pages are useful. Nothing is loaded unless you accept.",
             "Nous aimerions utiliser les cookies de Google Analytics pour compter les visites et savoir quelles pages sont utiles. Rien n’est chargé sans votre accord.",
             "نودّ استخدام ملفات تعريف الارتباط الخاصة بـ Google Analytics لإحصاء الزيارات ومعرفة الصفحات المفيدة. لا يُحمَّل شيء ما لم توافق.",
             "Мы хотели бы использовать cookie Google Analytics, чтобы считать посещения и понимать, какие страницы полезны. Без вашего согласия ничего не загружается."),
 "cc_yes": ("Accept", "Accepter", "أوافق", "Принять"),
 "cc_no": ("Decline", "Refuser", "أرفض", "Отклонить"),
 "cc_open": ("Cookie settings", "Paramètres des cookies", "إعدادات ملفات تعريف الارتباط", "Настройки cookie"),
 "cc_label": ("Cookie consent", "Consentement aux cookies", "الموافقة على ملفات تعريف الارتباط", "Согласие на cookie"),
 # localized legal pages
 "pg_home": ("Home", "Accueil", "الرئيسية", "Главная"),
 "pg_updated": ("Last updated", "Dernière mise à jour", "آخر تحديث", "Обновлено"),
}

META2 = {
 "en": ("Second Medical Opinion Online from $30 | Easy Clinic Center",
        "Get a second medical opinion from a specialist physician online from $30, or arrange treatment at partner hospitals in Türkiye. UK patients welcome."),
 "fr": ("Second avis médical en ligne dès 30 USD | Easy Clinic Center",
        "Obtenez en ligne le second avis médical d’un médecin spécialiste dès 30 USD, ou organisez un traitement dans des hôpitaux partenaires en Türkiye."),
 "ar": ("رأي طبي ثانٍ ابتداءً من 30 دولارًا | Easy Clinic Center",
        "احصل على رأي طبي ثانٍ من طبيب أخصائي عبر الإنترنت ابتداءً من 30 دولارًا، أو رتّب علاجك في مستشفيات شريكة في تركيا."),
 "ru": ("Второе мнение врача онлайн от 30 $ | Easy Clinic Center",
        "Получите второе мнение врача-специалиста онлайн от 30 $ или организуйте лечение в клиниках-партнёрах в Турции."),
}
