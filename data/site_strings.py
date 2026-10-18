"""Strings added or overridden for the simplified site (free first second opinion, one-step form, blog teaser).
Each value is a tuple (EN, FR, AR, RU); merged over web_strings.S by build_site.py."""

S2 = {
 # nav / calls to action
 "nav_blog": ("Blog", "Blog", "المدونة", "Блог"),
 "nav_apply": ("Free opinion", "Avis gratuit", "رأي مجاني", "Бесплатно"),
 "m_apply": ("Get your free opinion", "Mon avis gratuit", "احصل على رأيك المجاني", "Бесплатное мнение"),
 "cta_second": ("Request your free opinion", "Demander mon avis gratuit", "اطلب رأيك المجاني", "Запросить бесплатное мнение"),

 # hero
 "h_eb": ("Free for your first request", "Gratuit pour votre première demande", "مجاني لطلبك الأول", "Бесплатно при первом обращении"),
 "h_h1": ("Your first physician second opinion is <em>free</em>",
          "Votre premier second avis médical est <em>gratuit</em>",
          "رأيك الطبي الثاني الأول <em>مجاني</em>",
          "Первое второе мнение врача — <em>бесплатно</em>"),
 "h_p": ("Tell us about your case and send your records. A specialist physician reviews them and writes you a clear report. No payment, no obligation.",
         "Décrivez-nous votre cas et envoyez vos documents. Un médecin spécialiste les examine et vous rédige un rapport clair. Sans paiement, sans engagement.",
         "أخبرنا بحالتك وأرسل سجلاتك، ويراجعها طبيب أخصائي ويكتب لك تقريرًا واضحًا. دون دفع ودون التزام.",
         "Расскажите о вашем случае и пришлите документы. Врач-специалист изучит их и напишет понятное заключение. Без оплаты и обязательств."),
 "h_c1": ("Written physician report", "Rapport écrit d’un médecin", "تقرير مكتوب من طبيب", "Письменное заключение врача"),
 "h_c2": ("Request in 2 minutes", "Demande en 2 minutes", "اطلب في دقيقتين", "Заявка за 2 минуты"),
 "h_c3": ("No payment", "Aucun paiement", "دون دفع", "Без оплаты"),
 "free_note": ("Free for first-time requests.", "Gratuit pour toute première demande.", "مجاني للطلب الأول.", "Бесплатно при первом обращении."),

 # one-step form
 "f_title": ("Request your free opinion", "Demandez votre avis gratuit", "اطلب رأيك المجاني", "Запросите бесплатное мнение"),
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
 "f_consent": ("I agree that Easy Clinic Center may use the information I send to prepare my request, and I am 18 or older (or a parent/guardian).",
               "J’accepte qu’Easy Clinic Center utilise les informations envoyées pour préparer ma demande, et j’ai 18 ans ou plus (ou je suis parent/tuteur).",
               "أوافق على استخدام Easy Clinic Center للمعلومات التي أرسلها لإعداد طلبي، وعمري 18 عامًا أو أكثر (أو أنا أحد الوالدين/الوصي).",
               "Я согласен(на), что Easy Clinic Center использует присланные сведения для подготовки моей заявки, и мне 18 лет или больше (либо я родитель/опекун)."),
 "f_submit": ("Request my free opinion", "Demander mon avis gratuit", "اطلب رأيي المجاني", "Запросить бесплатно"),
 "f_mail": ("Send by e-mail", "Envoyer par e-mail", "إرسال بالبريد الإلكتروني", "Отправить по e-mail"),
 "err_contact": ("Enter an e-mail address or a phone number with country code (+...).",
                 "Saisissez une adresse e-mail ou un numéro avec indicatif (+...).",
                 "أدخل بريدًا إلكترونيًا أو رقم هاتف مع رمز الدولة (+...).",
                 "Введите e-mail или номер телефона с кодом страны (+...)."),

 # trust strip
 "tr1": ("First second opinion free", "Premier second avis gratuit", "أول رأي طبي ثانٍ مجاني", "Первое второе мнение бесплатно"),
 "tr3": ("Your data is used only for your request", "Vos données ne servent qu’à votre demande", "تُستخدم بياناتك لطلبك فقط", "Данные используются только для вашей заявки"),

 # blog teaser
 "blog_eb": ("Guides", "Guides", "أدلة", "Руководства"),
 "blog_h2": ("Clear answers before you decide", "Des réponses claires avant de décider", "إجابات واضحة قبل أن تقرر", "Понятные ответы до принятия решения"),
 "blog_all": ("All articles (English)", "Tous les articles (en anglais)", "كل المقالات (بالإنجليزية)", "Все статьи (на английском)"),
 "blog_read": ("Read article", "Lire l’article", "اقرأ المقال", "Читать статью"),

 # closing call to action
 "cta2_h": ("Ready? Request your free opinion in two minutes.", "Prêt ? Demandez votre avis gratuit en deux minutes.", "جاهز؟ اطلب رأيك المجاني في دقيقتين.", "Готовы? Запросите бесплатное мнение за две минуты."),

 # FAQ
 "q8": ("Is the first second opinion really free?", "Le premier second avis est-il vraiment gratuit ?", "هل الرأي الطبي الثاني الأول مجاني فعلًا؟", "Первое второе мнение действительно бесплатно?"),
 "a8": ("Yes. Your first second-opinion request is free. We confirm what is included when we reply to you.",
        "Oui. Votre première demande de second avis est gratuite. Nous vous confirmons ce qui est inclus dans notre réponse.",
        "نعم، طلب الرأي الطبي الثاني الأول مجاني. نوضّح لك ما يشمله عند ردّنا عليك.",
        "Да. Ваш первый запрос на второе мнение бесплатный. Что в него входит, мы подтвердим в ответе."),
}

META2 = {
 "en": ("Free Second Medical Opinion Online | Easy Clinic Center",
        "Get a free second medical opinion from a specialist physician online, or arrange treatment at partner hospitals in Türkiye. UK patients welcome."),
 "fr": ("Second avis médical gratuit en ligne | Easy Clinic Center",
        "Obtenez gratuitement un second avis médical en ligne d’un médecin spécialiste, ou organisez un traitement dans des hôpitaux partenaires en Türkiye."),
 "ar": ("رأي طبي ثانٍ مجاني عبر الإنترنت | Easy Clinic Center",
        "احصل مجانًا على رأي طبي ثانٍ عبر الإنترنت من طبيب أخصائي، أو رتّب علاجك في مستشفيات شريكة في تركيا."),
 "ru": ("Бесплатное второе мнение врача онлайн | Easy Clinic Center",
        "Получите бесплатное второе мнение врача-специалиста онлайн или организуйте лечение в клиниках-партнёрах в Турции."),
}
