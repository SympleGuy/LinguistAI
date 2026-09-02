// ── DATA ─────────────────────────────────────────────────────
      let SCENARIOS = [
        {
          id: "restaurant",
          title: "At the Restaurant",
          desc: "Order food, ask about the menu, handle dietary requirements, and pay the bill.",
          category: "Daily Life",
          cefr: "Beginner",
          duration: "10–15 min",
          emoji: "🍽️",
          popular: true,
          lang: "French",
          msgs: [
            {
              r: "ai",
              t: "Bonjour! Bienvenue au restaurant Le Petit Paris. Avez-vous une réservation ce soir?",
            },
            {
              r: "user",
              t: "Oui, j'ai une réservation pour deux personnes sous le nom de Martin.",
            },
            {
              r: "ai",
              t: "Bien sûr, Monsieur Martin! Suivez-moi, s'il vous plaît.",
            },
            {
              r: "user",
              t: "Merci beaucoup. Est-ce que vous pouvez m'apporter la carte des vins?",
            },
          ],
          fb: [
            {
              i: "✏️",
              t: "Missing accent: <b>réservation</b> (not reservation)",
            },
            { i: "🔊", t: "Good rhythm — work on nasal vowels. Score: 87%" },
          ],
          vocab: [
            { w: "carte des vins", d: "wine menu" },
            { w: "s'il vous plaît", d: "please (formal)" },
          ],
        },
        {
          id: "airport",
          title: "At the Airport",
          desc: "Check in, ask for gate information, handle delays, and navigate security.",
          category: "Travel",
          cefr: "Intermediate",
          duration: "10–15 min",
          emoji: "✈️",
          popular: true,
          lang: "English",
          msgs: [
            {
              r: "ai",
              t: "Good morning! Welcome to London Heathrow. Can I see your passport and boarding pass, please?",
            },
            {
              r: "user",
              t: "Of course. I'm travelling to Paris on flight BA304.",
            },
            {
              r: "ai",
              t: "Thank you. Are you checking any bags today, or is this carry-on only?",
            },
            {
              r: "user",
              t: "I have one bag to check in and this carry-on backpack.",
            },
          ],
          fb: [
            { i: "🔊", t: "Excellent clarity and pace. Score: 92%" },
            {
              i: "✏️",
              t: "Perfect use of present continuous for future travel ✓",
            },
          ],
          vocab: [
            { w: "boarding pass", d: "document allowing you to board" },
            { w: "carry-on", d: "bag taken into the cabin" },
          ],
        },
        {
          id: "job-interview",
          title: "Job Interview",
          desc: "Answer competency questions, discuss your experience, and ask about the role.",
          category: "Business",
          cefr: "Advanced",
          duration: "20–25 min",
          emoji: "💼",
          popular: false,
          lang: "English",
          msgs: [
            {
              r: "ai",
              t: "Thank you for coming in. Could you start by telling me about yourself?",
            },
            {
              r: "user",
              t: "Certainly. I have five years of experience in software engineering, mainly React and Python.",
            },
            {
              r: "ai",
              t: "Can you describe a difficult technical problem you solved under pressure?",
            },
          ],
          fb: [
            {
              i: "🔊",
              t: "Slow down slightly — rushing some syllables. Score: 78%",
            },
            { i: "✏️", t: "'I have five years of experience' — Correct! ✓" },
          ],
          vocab: [
            {
              w: "under pressure",
              d: "in a stressful or time-sensitive situation",
            },
          ],
        },
        {
          id: "hotel",
          title: "Checking Into a Hotel",
          desc: "Reserve rooms, request amenities, report issues, and interact with staff.",
          category: "Travel",
          cefr: "Beginner",
          duration: "8–12 min",
          emoji: "🏨",
          popular: false,
          lang: "Spanish",
          msgs: [
            {
              r: "ai",
              t: "¡Buenos días! Bienvenido al Hotel Sol. ¿Tiene reserva con nosotros?",
            },
            {
              r: "user",
              t: "Sí, tengo una reserva a nombre de García para dos noches.",
            },
          ],
          fb: [
            { i: "🔊", t: "Good pacing. Work on rolling the 'r'. Score: 80%" },
          ],
          vocab: [
            { w: "reserva", d: "reservation" },
            { w: "a nombre de", d: "under the name of" },
          ],
        },
        {
          id: "directions",
          title: "Asking for Directions",
          desc: "Navigate streets, use public transport, and describe locations clearly.",
          category: "Daily Life",
          cefr: "Beginner",
          duration: "5–10 min",
          emoji: "🗺️",
          popular: false,
          lang: "French",
          msgs: [
            {
              r: "ai",
              t: "Excusez-moi, pouvez-vous m'aider? Je cherche la gare principale.",
            },
            {
              r: "user",
              t: "Oui! Continuez tout droit, puis tournez à gauche au feu.",
            },
          ],
          fb: [
            { i: "✏️", t: "Great imperative form: 'continuez', 'tournez' ✓" },
          ],
          vocab: [
            { w: "tout droit", d: "straight ahead" },
            { w: "tournez à gauche", d: "turn left" },
          ],
        },
        {
          id: "emergency",
          title: "Medical Emergency",
          desc: "Describe symptoms, talk to a doctor, and handle urgent situations.",
          category: "Emergency",
          cefr: "Intermediate",
          duration: "10–15 min",
          emoji: "🏥",
          popular: false,
          lang: "German",
          msgs: [
            { r: "ai", t: "Guten Tag! Was kann ich für Sie tun?" },
            {
              r: "user",
              t: "Ich habe starke Kopfschmerzen und Fieber seit gestern Abend.",
            },
          ],
          fb: [
            {
              i: "✏️",
              t: "Good use of 'seit' + present for ongoing condition ✓",
            },
          ],
          vocab: [
            { w: "Kopfschmerzen", d: "headache" },
            { w: "seit gestern", d: "since yesterday" },
          ],
        },
        {
          id: "shopping",
          title: "Shopping",
          desc: "Browse products, negotiate prices, and complete transactions.",
          category: "Daily Life",
          cefr: "Beginner",
          duration: "8–12 min",
          emoji: "🛍️",
          popular: false,
          lang: "Spanish",
          msgs: [
            { r: "ai", t: "¡Hola! ¿En qué le puedo ayudar hoy?" },
            {
              r: "user",
              t: "Estoy buscando una chaqueta de cuero en color negro.",
            },
          ],
          fb: [
            {
              i: "📚",
              t: "Great use of 'preferiblemente' — sounds very natural!",
            },
          ],
          vocab: [
            { w: "chaqueta de cuero", d: "leather jacket" },
            { w: "en qué le puedo ayudar", d: "how can I help you" },
          ],
        },
        {
          id: "coffee",
          title: "Coffee Shop Small Talk",
          desc: "Order drinks, make small talk, and practise casual conversation.",
          category: "Social",
          cefr: "Beginner",
          duration: "5–10 min",
          emoji: "☕",
          popular: false,
          lang: "Spanish",
          msgs: [
            { r: "ai", t: "¡Hola! ¿Qué le pongo?" },
            {
              r: "user",
              t: "Un café con leche, por favor. ¿Y tiene algún bollo?",
            },
          ],
          fb: [
            {
              i: "🔊",
              t: "Excellent intonation on the question ✓. Score: 85%",
            },
          ],
          vocab: [
            { w: "café con leche", d: "coffee with milk" },
            { w: "bollo", d: "pastry / bun" },
          ],
        },
      ];

      let activeFilter = "All";
      let micOn = false;

      // ── NAVIGATION & AUTH STATE ────────────────────────────────────
      let currentAuthMode = "login";
      let currentUser = JSON.parse(
        localStorage.getItem("linguist_user") || "null",
      );
      let currentUserId = currentUser
        ? currentUser.id
        : localStorage.getItem("linguist_user_id") ||
          "00000000-0000-0000-0000-000000000001";
      localStorage.setItem("linguist_user_id", currentUserId);

      /**
       * apiFetch – drop-in replacement for fetch() on /api/ routes.
       * Automatically adds:
       *   - credentials: 'include'  (sends session cookie)
       *   - X-User-ID header        (fallback auth from localStorage)
       */
      function apiFetch(url, options = {}) {
        const userId =
          (currentUser && currentUser.id) ||
          currentUserId ||
          localStorage.getItem("linguist_user_id") ||
          "";
        const headers = Object.assign({}, options.headers || {});
        if (userId && userId !== "00000000-0000-0000-0000-000000000001") {
          headers["X-User-ID"] = userId;
        }
        return fetch(
          url,
          Object.assign({}, options, {
            headers,
            credentials: "include",
          }),
        );
      }

      const PROTECTED_PAGES = [
        "scenarios",
        "freetalk",
        "conversation",
        "dashboard",
        "profile",
        "flashcards",
        "summary",
      ];

      function showPage(name, syncUrl = true) {
        let authRedirectMsg = null;
        // Auth Guard: Redirect unauthenticated guest to login
        if (PROTECTED_PAGES.includes(name) && !currentUser) {
          name = "login";
          authRedirectMsg =
            "Please sign in or create an account to start practicing!";
        }

        const pageEl = document.getElementById("page-" + name);
        if (!pageEl) return;

        document
          .querySelectorAll(".page")
          .forEach((p) => p.classList.remove("active"));
        pageEl.classList.add("active");
        const isLanding = name === "landing";
        const isAuthPage = name === "login";

        // toggle inner nav vs landing/auth nav
        document.getElementById("inner-nav").style.display =
          isLanding || isAuthPage ? "none" : "flex";

        // toggle sign in vs sign out
        updateUserNavUI(isLanding, isAuthPage);

        document.querySelectorAll(".to-login").forEach((el) => {
          el.style.display = isLanding || isAuthPage ? "" : "none";
        });

        // active nav link
        ["scenarios", "freetalk", "dashboard", "profile", "flashcards"].forEach((n) => {
          const el = document.getElementById("nl-" + n);
          if (el) el.classList.toggle("active", n === name);
        });
        window.scrollTo(0, 0);

        if (syncUrl && window.history && window.history.replaceState) {
          const url = new URL(window.location);
          url.searchParams.set("page", name);
          window.history.replaceState({}, "", url);
        }

        if (name === "scenarios") {
          renderScenarios();
          updateDailyTurnUI();
        }
        if (name === "freetalk") {
          initFreeTalkPage();
        }
        if (name === "conversation") {
          updateDailyTurnUI();
        }
        if (name === "dashboard") loadDashboardData();
        if (name === "profile") loadProfileData();
        if (name === "login") {
          resetAuthForm(true);
        }
        if (name === "flashcards") loadFlashcards();

        if (authRedirectMsg) {
          const errEl = document.getElementById("auth-error-msg");
          if (errEl) {
            errEl.textContent = authRedirectMsg;
            errEl.style.display = "block";
          }
        }
      }

      function handleBrandClick() {
        if (currentUser) {
          showPage("dashboard");
        } else {
          showPage("landing");
        }
      }

      function updateUserNavUI(isLanding, isAuthPage) {
        const signInBtn = document.getElementById("navbar-signin");
        const signOutBtn = document.getElementById("navbar-logout");
        const tryBtn = document.getElementById("navbar-try");
        const innerNav = document.getElementById("inner-nav");
        const adminPortalBtn = document.getElementById("nl-admin-portal");

        if (currentUser) {
          if (signInBtn) signInBtn.style.display = "none";
          if (signOutBtn)
            signOutBtn.style.display = isAuthPage ? "none" : "inline-flex";
          if (tryBtn) tryBtn.style.display = "none";
          if (innerNav) innerNav.style.display = isAuthPage ? "none" : "flex";
          if (adminPortalBtn) {
            adminPortalBtn.style.display = (!isAuthPage && (currentUser.role === "admin" || currentUser.is_admin)) ? "inline-flex" : "none";
          }
        } else {
          if (signInBtn)
            signInBtn.style.display =
              isLanding || isAuthPage ? "inline-flex" : "none";
          if (signOutBtn) signOutBtn.style.display = "none";
          if (tryBtn)
            tryBtn.style.display =
              isLanding || isAuthPage ? "inline-flex" : "inline-flex";
          if (innerNav)
            innerNav.style.display = isLanding || isAuthPage ? "none" : "flex";
          if (adminPortalBtn) adminPortalBtn.style.display = "none";
        }
      }

      // ── SCENARIOS & SESSION STATE ──────────────────────────────────
      let currentSessionId = null;

      let showAllLevelsForLanguage = false;

      function toggleShowAllLevels() {
        showAllLevelsForLanguage = !showAllLevelsForLanguage;
        renderScenarios();
      }

      async function loadScenariosFromAPI() {
        try {
          let url = "/api/scenarios/";
          if (currentUser) {
            const userLang = currentUser.target_language || "English";
            const userCefr = currentUser.proficiency_level || "Beginner";
            if (showAllLevelsForLanguage) {
              url = `/api/scenarios/?lang=${encodeURIComponent(userLang)}&all_levels=true&user_id=${currentUserId}`;
            } else {
              url = `/api/scenarios/?lang=${encodeURIComponent(userLang)}&cefr=${encodeURIComponent(userCefr)}&user_id=${currentUserId}`;
            }
          }

          const res = await apiFetch(url);
          if (res.ok) {
            const data = await res.json();
            if (Array.isArray(data)) {
              SCENARIOS = data.map((s) => ({
                id: String(s.id),
                title: s.title || "Untitled Scenario",
                desc: s.description || s.desc || "",
                category: s.category || "Daily Life",
                cefr: s.cefr || "Beginner",
                duration: s.duration || "10–15 min",
                emoji: s.emoji || "💬",
                popular: !!s.popular,
                lang: s.lang || "English",
                msgs: s.msgs || [{ r: "ai", t: getScenarioGreeting(s) }],
                fb: s.fb || [
                  { i: "ℹ️", t: "Start speaking to receive AI feedback." },
                ],
                vocab: s.vocab || [],
              }));
            }
          }
        } catch (e) {
          console.warn("Could not load scenarios from API, using fallback", e);
        }
      }

      // Dynamic Scenario Greeting Generator per Topic & Language
      function getScenarioGreeting(s) {
        if (!s) return "Hello! How can I help you today?";
        const titleLower = (s.title || "").toLowerCase();
        const lang = s.lang || "English";

        const greetings = {
          French: {
            free: "Bonjour ! 😊 Bienvenue dans la conversation libre ! De quoi aimerais-tu parler aujourd'hui ?",
            talk: "Bonjour ! 😊 Bienvenue dans la conversation libre ! De quoi aimerais-tu parler aujourd'hui ?",
            restaurant:
              "Bonjour ! Bienvenue au restaurant Le Petit Paris. Avez-vous une réservation pour ce soir ?",
            coffee:
              "Bonjour ! Que puis-je vous servir aujourd'hui à la brasserie ?",
            hotel:
              "Bonjour et bienvenue à l'hôtel ! Avez-vous une réservation chez nous ?",
            airport:
              "Bonjour ! Puis-je voir votre passeport et votre carte d'embarquement, s'il vous plaît ?",
            job: "Bonjour et bienvenue à cet entretien d'embauche. Pourriez-vous commencer par vous présenter ?",
            interview:
              "Bonjour et bienvenue à cet entretien d'embauche. Pourriez-vous commencer par vous présenter ?",
            shop: "Bonjour ! Puis-je vous aider à trouver quelque chose en magasin ?",
            direction:
              "Bonjour ! Je cherche la gare principale, pouvez-vous m'aider ?",
            emergency:
              "Bonjour, je suis le médecin de garde. Quels symptômes ressentez-vous ?",
            default: `Bonjour ! Bienvenue dans votre session "${s.title}". Comment puis-je vous aider aujourd'hui ?`,
          },
          Spanish: {
            free: "¡Hola! 😊 ¡Bienvenido a la conversación libre! ¿De qué te gustaría hablar hoy?",
            talk: "¡Hola! 😊 ¡Bienvenido a la conversación libre! ¿De qué te gustaría hablar hoy?",
            restaurant:
              "¡Hola! Bienvenido a nuestro restaurante. ¿Tiene una reserva para hoy?",
            coffee:
              "¡Hola! Bienvenido a la cafetería. ¿Qué le gustaría pedir hoy?",
            hotel:
              "¡Buenos días! Bienvenido al Hotel Sol. ¿Tiene una reserva con nosotros?",
            airport:
              "¡Buenos días! ¿Me permite su pasaporte y tarjeta de embarque, por favor?",
            job: "¡Hola y bienvenido a la entrevista! ¿Podría empezar contándome un poco sobre su experiencia?",
            interview:
              "¡Hola y bienvenido a la entrevista! ¿Podría empezar contándome un poco sobre su experiencia?",
            shop: "¡Hola! ¿En qué le puedo ayudar a buscar hoy?",
            direction:
              "¡Hola! Disculpe, ¿sabe cómo llegar al centro desde aquí?",
            emergency: "¡Hola! Soy el médico de guardia. ¿Qué síntomas tiene?",
            default: `¡Hola! Bienvenido a la práctica de "${s.title}". ¿En qué le puedo ayudar hoy?`,
          },
          German: {
            free: "Hallo! 😊 Willkommen zum freien Gespräch! Worüber möchtest du heute sprechen?",
            talk: "Hallo! 😊 Willkommen zum freien Gespräch! Worüber möchtest du heute sprechen?",
            restaurant:
              "Guten Tag! Willkommen im Restaurant. Haben Sie einen Tisch reserviert?",
            coffee:
              "Guten Tag! Willkommen im Café. Was darf ich Ihnen heute bringen?",
            hotel:
              "Guten Tag und herzlich willkommen! Haben Sie eine Zimmerreservierung bei uns?",
            airport:
              "Guten Tag! Kann ich bitte Ihren Reisepass und Ihre Bordkarte sehen?",
            job: "Guten Tag! Vielen Dank für Ihr Kommen. Könnten Sie sich bitte kurz vorstellen?",
            interview:
              "Guten Tag! Vielen Dank für Ihr Kommen. Könnten Sie sich bitte kurz vorstellen?",
            shop: "Hallo! Kann ich Ihnen heute beim Einkaufen behilflich sein?",
            direction:
              "Entschuldigung! Können Sie mir bitte sagen, wo der Bahnhof ist?",
            emergency:
              "Guten Tag, ich bin der diensthabende Arzt. Was für Beschwerden haben Sie?",
            default: `Guten Tag! Willkommen zu Ihrer "${s.title}" Übung. Wie kann ich Ihnen helfen?`,
          },
          Japanese: {
            free: "こんにちは！😊 フリートークへようこそ！今日はどんなことについて話したいですか？",
            talk: "こんにちは！😊 フリートークへようこそ！今日はどんなことについて話したいですか？",
            restaurant:
              "いらっしゃいませ！レストランへようこそ。ご予約はされていますでしょうか？",
            coffee:
              "いらっしゃいませ！カフェへようこそ。何をご注文されますか？",
            hotel:
              "いらっしゃいませ、当ホテルへようこそ！ご予約のお名前を伺えますでしょうか？",
            airport: "こんにちは！パスポートと搭乗券を拝見できますでしょうか？",
            job: "本日は面接にお越しいただきありがとうございます。簡単に自己紹介をお願いできますか？",
            interview:
              "本日は面接にお越しいただきありがとうございます。簡単に自己紹介をお願いできますか？",
            shop: "いらっしゃいませ！何かお探しの商品はございますか？",
            direction: "すみません、駅までの道を教えていただけますでしょうか？",
            emergency: "こんにちは、当直医です。どのような症状がありますか？",
            default: `こんにちは！「${s.title}」の練習へようこそ。どのようなご用件でしょうか？`,
          },
          Korean: {
            free: "안녕하세요! 😊 자유 대화에 오신 것을 환영합니다! 오늘 어떤 이야기를 나누고 싶으신가요?",
            talk: "안녕하세요! 😊 자유 대화에 오신 것을 환영합니다! 오늘 어떤 이야기를 나누고 싶으신가요?",
            restaurant:
              "안녕하세요! 식당에 오신 것을 환영합니다. 예약하셨나요?",
            coffee:
              "안녕하세요! 카페에 오신 것을 환영합니다. 어떤 음료를 드릴까요?",
            hotel:
              "어서오세요! 호텔에 오신 것을 환영합니다. 예약자 성함이 어떻게 되시나요?",
            airport: "안녕하세요! 여권과 탑승권을 보여주시겠습니까?",
            job: "면접에 와주셔서 감사합니다. 먼저 간단하게 자기소개 부탁드립니다.",
            interview:
              "면접에 와주셔서 감사합니다. 먼저 간단하게 자기소개 부탁드립니다.",
            shop: "어서오세요! 찾으시는 물건이 있으신가요?",
            direction: "실례합니다, 지하철역으로 가려면 어디로 가야 하나요?",
            emergency: "안녕하세요, 담당 의사입니다. 어디가 불편하신가요?",
            default: `안녕하세요! "${s.title}" 연습에 오신 것을 환영합니다. 무엇을 도와드릴까요?`,
          },
          Chinese: {
            free: "你好！😊 欢迎来到自由对话！今天你想聊些什么呢？",
            talk: "你好！😊 欢迎来到自由对话！今天你想聊些什么呢？",
            restaurant: "您好！欢迎光临餐厅。请问您今天有预订吗？",
            coffee: "您好！欢迎光临咖啡厅，今天想喝点什么？",
            hotel: "您好！欢迎入住酒店。请问预订的名字是什么？",
            airport: "您好！请出示您的护照和登机牌。",
            job: "您好，感谢您来参加面试。请先简单介绍一下您自己吧。",
            interview: "您好，感谢您来参加面试。请先简单介绍一下您自己吧。",
            shop: "您好！欢迎光临，请问有什么可以帮您的？",
            direction: "请问一下，去市中心应该怎么走？",
            emergency: "您好，我是值班医生。请问您哪里感觉不舒服？",
            default: `您好！欢迎来到“${s.title}”练习。请问有什么我可以协助您的？`,
          },
          Vietnamese: {
            free: "Chào bạn! 😊 Chào mừng bạn đến với chế độ Trò chuyện tự do! Hôm nay bạn muốn cùng mình tâm sự hay bàn luận về chủ đề gì nào?",
            talk: "Chào bạn! 😊 Chào mừng bạn đến với chế độ Trò chuyện tự do! Hôm nay bạn muốn cùng mình tâm sự hay bàn luận về chủ đề gì nào?",
            restaurant:
              "Xin chào! Chào mừng bạn đến với nhà hàng. Bạn đã đặt bàn trước chưa ạ?",
            coffee:
              "Xin chào! Chào mừng bạn đến quán cà phê. Bạn muốn dùng đồ uống gì hôm nay?",
            hotel:
              "Xin chào! Chào mừng quý khách đến khách sạn. Quý khách đã đặt phòng trước chưa ạ?",
            airport:
              "Xin chào! Vui lòng cho tôi xem hộ chiếu và thẻ lên máy bay của bạn.",
            job: "Chào bạn, cảm ơn bạn đã đến phỏng vấn. Bạn có thể giới thiệu đôi nét về bản thân không?",
            interview:
              "Chào bạn, cảm ơn bạn đã đến phỏng vấn. Bạn có thể giới thiệu đôi nét về bản thân không?",
            shop: "Xin chào! Bạn đang tìm kiếm sản phẩm nào để mình hỗ trợ nhé?",
            direction:
              "Xin lỗi, bạn có thể chỉ đường giúp tôi đến ga tàu gần nhất được không?",
            emergency:
              "Chào bạn, tôi là bác sĩ trực. Bạn đang cảm thấy khó chịu ở đâu?",
            default: `Xin chào! Chào mừng bạn đến với buổi luyện tập "${s.title}". Tôi có thể giúp gì cho bạn hôm nay?`,
          },
          English: {
            free: "Hey there! 😊 Welcome to Free Talk! We can chat about anything you like — your day, hobbies, travel, movies, or ideas. What's on your mind today?",
            talk: "Hey there! 😊 Welcome to Free Talk! We can chat about anything you like — your day, hobbies, travel, movies, or ideas. What's on your mind today?",
            restaurant:
              "Hello! Welcome to our restaurant. Do you have a table reservation with us today?",
            coffee:
              "Hi there! Welcome to the coffee shop. What can I get started for you today?",
            hotel:
              "Good day and welcome to the hotel! Do you have a reservation under your name?",
            airport:
              "Good morning! May I please see your passport and boarding pass?",
            job: "Hello, thank you for coming in today for the interview. Could you start by telling me a little about yourself?",
            interview:
              "Hello, thank you for coming in today for the interview. Could you start by telling me a little about yourself?",
            shop: "Hello! Welcome in. Are you looking for anything specific today?",
            direction:
              "Excuse me! Could you tell me how to get to the central station from here?",
            emergency:
              "Hello, I am the doctor on duty. Could you describe what symptoms you've been experiencing?",
            default: `Hello and welcome to your "${s.title}" practice! How can I help you today?`,
          },
        };

        const langMap = greetings[lang] || greetings["English"];
        let matchedGreeting = null;

        for (const [key, msg] of Object.entries(langMap)) {
          if (key !== "default" && titleLower.includes(key)) {
            matchedGreeting = msg;
            break;
          }
        }

        return (
          matchedGreeting ||
          langMap["default"] ||
          `Welcome to ${s.title}! How can I help you today?`
        );
      }

      async function renderScenarios() {
        // Update badge if user is logged in
        const badgeDiv = document.getElementById("scen-custom-badge");
        const badgeText = document.getElementById("scen-badge-text");
        const toggleBtn = document.getElementById("btn-toggle-all-scen");
        if (currentUser && badgeDiv && badgeText) {
          badgeDiv.style.display = "block";
          const langEmojis = {
            English: "🇬🇧",
            French: "🇫🇷",
            Spanish: "🇪🇸",
            German: "🇩🇪",
            Japanese: "🇯🇵",
            Chinese: "🇨🇳",
            Korean: "🇰🇷",
            Vietnamese: "🇻🇳",
          };
          const uLang = currentUser.target_language || "English";
          const uCefr = currentUser.proficiency_level || "Beginner";
          const flag = langEmojis[uLang] || "🌐";
          if (showAllLevelsForLanguage) {
            badgeText.textContent = `All Levels in ${flag} ${uLang}`;
            if (toggleBtn)
              toggleBtn.textContent = `Show only my level (${uCefr})`;
          } else {
            badgeText.textContent = `Personalized for: ${flag} ${uLang} • ${uCefr}`;
            if (toggleBtn)
              toggleBtn.textContent = `Explore all levels in ${uLang}`;
          }
        } else if (badgeDiv) {
          badgeDiv.style.display = "none";
        }

        await loadScenariosFromAPI();
        updateDailyTurnUI();
        const q = (
          document.getElementById("scen-search")?.value || ""
        ).toLowerCase();
        const grid = document.getElementById("scenarios-grid");
        const list = SCENARIOS.filter((s) => {
          const isFree = s.category === "Open Talk" || (s.title || "").toLowerCase().includes("free talk");
          if (isFree) return false; // Handled separately in dedicated Free Talk studio
          const mc = activeFilter === "All" || s.category === activeFilter;
          const mq =
            !q ||
            s.title.toLowerCase().includes(q) ||
            s.desc.toLowerCase().includes(q);
          return mc && mq;
        });

        if (list.length === 0) {
          grid.innerHTML = `
          <div style="grid-column:1/-1;text-align:center;padding:48px 20px;background:#fff;border-radius:16px;border:1px dashed var(--border)">
            <div style="font-size:2.5rem;margin-bottom:12px">📚</div>
            <div style="font-weight:700;font-size:1.1rem;margin-bottom:6px">No scenarios found for this filter</div>
            <p style="color:var(--muted-fg);font-size:.875rem;margin-bottom:16px">Try switching categories or view all available scenarios.</p>
            <button onclick="setFilter(document.querySelector('.filter-pill'), 'All')" class="btn-cta-outline" style="padding:7px 16px;font-size:.85rem">View All Categories</button>
          </div>`;
          return;
        }

        grid.innerHTML = list
          .map(
            (s) => `
        <div class="scen-card" onclick="startConv('${s.id}')">
          <div class="scen-emoji">${s.emoji}</div>
          <div class="scen-body">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px">
              <span class="cefr-badge cefr-${s.cefr}">${s.cefr}</span>
              ${s.popular ? '<span style="background:#fff7ed;color:#c2410c;font-size:.67rem;font-weight:700;border-radius:999px;padding:1px 7px">🔥 Popular</span>' : ""}
              <span style="margin-left:auto;font-size:.72rem;color:var(--muted-fg)">⏱ ${s.duration}</span>
            </div>
            <div style="font-weight:700;font-size:.9rem">${s.title}</div>
            <div style="font-size:.8rem;color:var(--muted-fg);margin-top:3px;line-height:1.45">${s.desc}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
              <span style="background:var(--secondary-bg);color:var(--primary);font-size:.7rem;font-weight:600;border-radius:8px;padding:2px 8px">${s.lang}</span>
              <span style="color:var(--primary);font-size:.8rem;font-weight:600">${s.category}</span>
            </div>
          </div>
        </div>`
          )
          .join("");
      }

      function setFilter(btn, cat) {
        activeFilter = cat;
        document
          .querySelectorAll(".filter-pill")
          .forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        renderScenarios();
      }

      // ── CONVERSATION & SESSION STATE ──────────────────────────────
      let currentScenarioId = 1;
      let currentSessionFeedbackList = [];
      let currentSessionVocabList = [];
      let currentSessionScores = {
        grammar: [],
        pronunciation: [],
        vocab: [],
        overall: [],
      };

      async function startConv(id) {
        currentScenarioId = id;
        currentSessionId = null;
        currentSessionFeedbackList = [];
        currentSessionVocabList = [];
        currentSessionScores = {
          grammar: [],
          pronunciation: [],
          vocab: [],
          overall: [],
        };

        const s =
          SCENARIOS.find((x) => String(x.id) === String(id)) || SCENARIOS[0];
        document.getElementById("conv-title").textContent = s.title;
        document.getElementById("conv-lang").textContent = s.lang;
        document.getElementById("conv-banner").textContent = s.emoji;

        // Show dynamic, natural initial AI greeting for this scenario and language
        const initialGreeting = getScenarioGreeting(s);
        const initVoiceId = "ai-voice-init-" + Date.now();
        const initVoicePill = createAiVoicePillHtml("", initVoiceId, initialGreeting, s.lang);
        const ml = document.getElementById("msg-list");
        ml.innerHTML = `
    <div class="msg-wrap">
      <div class="msg-lbl">🤖 LinguistAI</div>
      <div class="msg-bubble msg-ai">${initialGreeting}</div>
      <div>${initVoicePill}</div>
    </div>`;
        ml.scrollTop = ml.scrollHeight;

        // Preload audio URL for instant playback when user clicks or listens
        fetch(`/api/tts/?text=${encodeURIComponent(initialGreeting)}&lang=${encodeURIComponent(s.lang)}`)
          .then((r) => r.json())
          .then((d) => {
            if (d && d.audio_url) {
              const p = document.getElementById(`pill-${initVoiceId}`);
              if (p) p.setAttribute("data-url", d.audio_url);
            }
          })
          .catch(() => {});

        // Set fresh waiting state for Live Feedback
        const fbList = document.getElementById("fb-list");
        if (fbList) {
          fbList.innerHTML = `
      <div class="fb-item" style="color:var(--muted-fg)"><span style="flex-shrink:0">🎙️</span><span>Speak into the microphone or type below. Real-time feedback, corrections, and scores will appear here!</span></div>`;
        }

        document.getElementById("vocab-list").innerHTML = (s.vocab || [])
          .map(
            (v) => `
    <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border)">
      <span style="font-weight:600;color:var(--primary)">${v.w}</span>
      <span style="color:var(--muted-fg)">${v.d}</span>
    </div>`,
          )
          .join("");

        // Setup Free Talk Topic Starters
        const isOpenTalk = s.category === "Open Talk" || (s.title || "").toLowerCase().includes("free talk");
        const startersWrap = document.getElementById("conv-starters-wrap");
        const startersList = document.getElementById("starters-list");
        if (isOpenTalk && startersWrap && startersList) {
          const starterMap = {
            English: [
              { icon: "☕", text: "Tell me about your day so far!" },
              { icon: "✈️", text: "If you could travel anywhere right now, where would you go?" },
              { icon: "🎬", text: "What's a movie or book you recently enjoyed?" },
              { icon: "💡", text: "What do you think about AI and the future of technology?" },
              { icon: "🎲", text: "Ask me a thought-provoking, interesting question!" },
            ],
            French: [
              { icon: "☕", text: "Raconte-moi ta journée !" },
              { icon: "✈️", text: "Si tu pouvais voyager n'importe où, où irais-tu ?" },
              { icon: "🎬", text: "Quel est ton film ou livre préféré récemment ?" },
              { icon: "💡", text: "Que penses-tu de l'intelligence artificielle ?" },
              { icon: "🎲", text: "Pose-moi une question surprise et intéressante !" },
            ],
            Spanish: [
              { icon: "☕", text: "¡Cuéntame cómo ha ido tu día!" },
              { icon: "✈️", text: "¿Si pudieras viajar a cualquier lugar, a dónde irías?" },
              { icon: "🎬", text: "¿Cuál es tu película o libro favorito recientemente?" },
              { icon: "💡", text: "¿Qué opinas sobre el futuro de la inteligencia artificial?" },
              { icon: "🎲", text: "¡Hazme una pregunta interesante y aleatoria!" },
            ],
            German: [
              { icon: "☕", text: "Erzähl mir von deinem Tag!" },
              { icon: "✈️", text: "Wohin würdest du reisen, wenn du könntest?" },
              { icon: "🎬", text: "Was ist dein Lieblingsfilm oder Buch?" },
              { icon: "💡", text: "Was denkst du über Künstliche Intelligenz und Zukunft?" },
              { icon: "🎲", text: "Stell mir eine überraschende, spannende Frage!" },
            ],
            Japanese: [
              { icon: "☕", text: "今日の一日について教えて！" },
              { icon: "✈️", text: "今すぐどこへでも旅行できるなら、どこに行きたい？" },
              { icon: "🎬", text: "最近面白かった映画や本はある？" },
              { icon: "💡", text: "AIや未来のテクノロジーについてどう思う？" },
              { icon: "🎲", text: "何か面白い質問をしてみて！" },
            ],
            Chinese: [
              { icon: "☕", text: "跟我聊聊你今天过得怎么样吧！" },
              { icon: "✈️", text: "如果你能去任何地方旅行，你想去哪里？" },
              { icon: "🎬", text: "你最近看过什么好看的电影或书吗？" },
              { icon: "💡", text: "你对人工智能和未来科技有什么看法？" },
              { icon: "🎲", text: "问我一个随机有趣的问题吧！" },
            ],
            Korean: [
              { icon: "☕", text: "오늘 하루 어땠는지 이야기해 줘!" },
              { icon: "✈️", text: "어디로든 여행 갈 수 있다면 어디로 가고 싶어?" },
              { icon: "🎬", text: "최근에 재미있게 본 영화나 책 있어?" },
              { icon: "💡", text: "AI와 미래 기술에 대해 어떻게 생각해?" },
              { icon: "🎲", text: "나에게 재미있고 신선한 질문 하나 해줘!" },
            ],
            Vietnamese: [
              { icon: "☕", text: "Hôm nay của bạn thế nào rồi, kể mình nghe với!" },
              { icon: "✈️", text: "Nếu được đi du lịch bất cứ đâu ngay bây giờ, bạn sẽ đi đâu?" },
              { icon: "🎬", text: "Bộ phim hay cuốn sách bạn thích nhất gần đây là gì?" },
              { icon: "💡", text: "Bạn nghĩ gì về tương lai của công nghệ và AI?" },
              { icon: "🎲", text: "Hãy hỏi mình một câu hỏi ngẫu nhiên và thú vị nhé!" },
            ],
          };
          const curStarters = starterMap[s.lang] || starterMap["English"];
          startersList.innerHTML = curStarters
            .map(
              (st) =>
                `<button type="button" class="starter-chip" onclick="selectTopicStarter('${st.text.replace(/'/g, "\\'")}')"><span>${st.icon}</span> ${st.text}</button>`
            )
            .join("");
          startersWrap.style.display = "flex";
        } else if (startersWrap) {
          startersWrap.style.display = "none";
        }

        updateDailyTurnUI();
        showPage("conversation");

        // Start real backend session
        try {
          const activeUid = (currentUser && currentUser.id) || currentUserId || localStorage.getItem("linguist_user_id");
          const res = await apiFetch("/api/sessions/start/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ user_id: activeUid, scenario_id: id }),
          });
          if (res.ok) {
            const data = await res.json();
            currentSessionId = data.session_id;
            console.log("Started session:", currentSessionId);
          }
        } catch (e) {
          console.warn("Could not create backend session:", e);
        }
      }

      window.selectTopicStarter = function (text) {
        const input = document.getElementById("text-fallback-input");
        const container = document.getElementById("text-fallback-container");
        if (container) container.style.display = "flex";
        if (input) {
          input.value = text;
        }
        submitUserMessage(text);
      };

      let mediaRecorder = null;
      let audioChunks = [];

      function updateFeedbackUI(feedback) {
        if (!feedback) return;

        // Track session metrics for Summary page
        if (feedback.grammar_score !== undefined)
          currentSessionScores.grammar.push(feedback.grammar_score);
        if (feedback.pronunciation_score !== undefined)
          currentSessionScores.pronunciation.push(feedback.pronunciation_score);
        if (feedback.vocabulary_score !== undefined)
          currentSessionScores.vocab.push(feedback.vocabulary_score);
        const turnOverall = Math.round(
          ((feedback.grammar_score || 85) +
            (feedback.pronunciation_score || 80)) /
            2,
        );
        currentSessionScores.overall.push(turnOverall);
        currentSessionFeedbackList.push(feedback);

        const fbList = document.getElementById("fb-list");
        if (!fbList) return;

        let correctionsHTML = "";
        if (
          Array.isArray(feedback.corrections) &&
          feedback.corrections.length > 0
        ) {
          correctionsHTML = feedback.corrections
            .map(
              (c) =>
                `<div class="fb-item" style="font-size:0.8rem;color:#dc2626;"><span style="flex-shrink:0">❌</span><span><s>${c.original}</s> ➔ <b style="color:#16a34a">${c.corrected}</b> (${c.explanation})</span></div>`,
            )
            .join("");
        }

        let suggestionsHTML = "";
        if (
          Array.isArray(feedback.suggestions) &&
          feedback.suggestions.length > 0
        ) {
          suggestionsHTML = `<div class="fb-item" style="font-size:0.8rem;"><span style="flex-shrink:0">💡</span><span>Suggestions: ${feedback.suggestions.join("; ")}</span></div>`;
        }

        fbList.innerHTML = `
    <div class="fb-item"><span style="flex-shrink:0">📊</span><span>Grammar: <b>${feedback.grammar_score}%</b> | Pronunciation: <b>${feedback.pronunciation_score}%</b> | Vocab: <b>${feedback.vocabulary_score || 80}%</b></span></div>
    <div class="fb-item"><span style="flex-shrink:0">📝</span><span>${feedback.comments}</span></div>
    ${correctionsHTML}
    ${suggestionsHTML}
  `;

        // Update Vocabulary List in real-time
        if (
          Array.isArray(feedback.extracted_vocabulary) &&
          feedback.extracted_vocabulary.length > 0
        ) {
          const vocabList = document.getElementById("vocab-list");
          if (vocabList) {
            const existingHTML = vocabList.innerHTML;
            let newVocabHTML = "";
            feedback.extracted_vocabulary.forEach((v) => {
              // Track session vocabulary for Summary page
              if (
                !currentSessionVocabList.some(
                  (item) => item.word.toLowerCase() === v.word.toLowerCase(),
                )
              ) {
                currentSessionVocabList.push(v);
              }

              // Deduplicate in UI
              if (!existingHTML.includes(`🌟 ${v.word}`)) {
                newVocabHTML += `<div style="margin-bottom:8px;">
                 <div style="font-weight:bold;color:var(--primary);">🌟 ${v.word}</div>
                 <div style="color:var(--muted-fg);font-size:0.8rem;">${v.translation}</div>
               </div>`;
              }
            });

            if (vocabList.innerHTML.trim() === "") {
              vocabList.innerHTML = newVocabHTML;
            } else {
              vocabList.innerHTML += newVocabHTML;
            }
          }
        }
      }

      // End Lesson & Aggregate Summary Function
      function endLesson() {
        // 1. Calculate average scores
        const gScores = currentSessionScores.grammar;
        const pScores = currentSessionScores.pronunciation;
        const vScores = currentSessionScores.vocab;
        const oScores = currentSessionScores.overall;

        const avg = (arr) =>
          arr.length > 0
            ? Math.round(arr.reduce((a, b) => a + b, 0) / arr.length)
            : 85;

        const avgG = avg(gScores);
        const avgP = avg(pScores);
        const avgV = avg(vScores);
        const avgO =
          oScores.length > 0 ? avg(oScores) : Math.round((avgG + avgP) / 2);

        // 2. Set Score KPIs
        document.getElementById("sum-overall-score").textContent = `${avgO}%`;
        document.getElementById("sum-grammar-score").textContent = `${avgG}%`;
        document.getElementById("sum-pronun-score").textContent = `${avgP}%`;
        document.getElementById("sum-vocab-score").textContent = `${avgV}%`;

        // 3. Hero Subtitle & Emoji
        const currentScen = SCENARIOS.find(
          (x) => String(x.id) === String(currentScenarioId),
        ) || { title: "Practice Session", emoji: "🎉", lang: "English" };
        document.getElementById("sum-emoji").textContent =
          currentScen.emoji || "🎉";
        document.getElementById("sum-subtitle").textContent =
          `Completed ${currentScen.title} (${currentScen.lang}) with ${currentSessionFeedbackList.length} turns practiced.`;

        // 4. AI Feedback Recap
        const commentsDiv = document.getElementById("sum-ai-comments");
        const lastFb =
          currentSessionFeedbackList[currentSessionFeedbackList.length - 1];
        if (lastFb && lastFb.comments) {
          commentsDiv.textContent = lastFb.comments;
        } else if (currentSessionFeedbackList.length === 0) {
          commentsDiv.textContent =
            "You completed the lesson! Practice speaking into the microphone or typing responses to receive in-depth real-time grammar, pronunciation, and vocabulary ratings.";
        } else {
          commentsDiv.textContent =
            "Great conversational practice! Your fluency and expression are steadily improving. Keep exploring varied scenarios to strengthen your speaking reflexes.";
        }

        // 5. Corrections list
        const correctionsWrap = document.getElementById("sum-corrections-wrap");
        const correctionsList = document.getElementById("sum-corrections-list");
        const allCorrections = [];
        currentSessionFeedbackList.forEach((fb) => {
          if (Array.isArray(fb.corrections)) {
            fb.corrections.forEach((c) => allCorrections.push(c));
          }
        });

        if (allCorrections.length > 0) {
          correctionsWrap.style.display = "block";
          correctionsList.innerHTML = allCorrections
            .map(
              (c) => `
          <div style="background:#fef2f2;border:1px solid #fee2e2;border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:0.85rem;">
            <div style="color:#dc2626;text-decoration:line-through;margin-bottom:2px;">${c.original}</div>
            <div style="color:#16a34a;font-weight:700;">➔ ${c.corrected}</div>
            <div style="color:#6b7280;font-size:0.78rem;margin-top:4px;">${c.explanation}</div>
          </div>
        `,
            )
            .join("");
        } else {
          correctionsWrap.style.display = "none";
        }

        // 6. Suggestions list
        const suggestionsWrap = document.getElementById("sum-suggestions-wrap");
        const suggestionsList = document.getElementById("sum-suggestions-list");
        const allSuggestions = [];
        currentSessionFeedbackList.forEach((fb) => {
          if (Array.isArray(fb.suggestions)) {
            fb.suggestions.forEach((s) => {
              if (!allSuggestions.includes(s)) allSuggestions.push(s);
            });
          }
        });

        if (allSuggestions.length > 0) {
          suggestionsWrap.style.display = "block";
          suggestionsList.innerHTML = allSuggestions
            .map(
              (s) => `
          <div style="background:#fffbeb;border:1px solid #fef3c7;border-radius:10px;padding:8px 12px;margin-bottom:6px;font-size:0.85rem;color:#92400e;display:flex;align-items:center;gap:8px;">
            <span>💡</span><span>${s}</span>
          </div>
        `,
            )
            .join("");
        } else {
          suggestionsWrap.style.display = "none";
        }

        // 7. Vocabulary list
        const vocabListDiv = document.getElementById("sum-vocab-list");
        if (currentSessionVocabList.length > 0) {
          vocabListDiv.innerHTML = currentSessionVocabList
            .map(
              (v) => `
          <div class="summary-vocab-item">
            <div style="font-weight:700;color:var(--primary);font-size:0.95rem;">🌟 ${v.word}</div>
            <div style="color:#4b5563;font-size:0.82rem;margin-top:2px;">${v.translation || ""}</div>
            ${v.example ? `<div style="color:#9ca3af;font-size:0.75rem;font-style:italic;margin-top:4px;">"${v.example}"</div>` : ""}
          </div>
        `,
            )
            .join("");
        } else {
          vocabListDiv.innerHTML = `<div style="text-align:center;color:var(--muted-fg);font-size:0.85rem;padding:20px;">No new words were extracted in this session.</div>`;
        }

        // 8. Navigate to summary page
        showPage("summary");
      }

      async function ensureActiveSession() {
        if (currentSessionId) return currentSessionId;
        try {
          const res = await apiFetch("/api/sessions/start/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
              user_id: currentUserId,
              scenario_id: currentScenarioId || 1,
            }),
          });
          if (res.ok) {
            const data = await res.json();
            currentSessionId = data.session_id;
            return currentSessionId;
          }
        } catch (e) {
          console.warn("Error ensuring session:", e);
        }
        return null;
      }

      async function submitUserMessage(userText) {
        if (!userText) return;
        const ml = document.getElementById("msg-list");
        const d = document.createElement("div");
        d.className = "msg-wrap msg-user-wrap";
        d.innerHTML = `<div class="msg-lbl">🧑 You</div><div class="msg-bubble msg-user">${userText}</div>`;
        ml.appendChild(d);
        ml.scrollTop = ml.scrollHeight;

        const sessId = await ensureActiveSession();
        if (!sessId) return;

        const typing = document.createElement("div");
        typing.className = "typing-indicator";
        typing.id = "ai-typing";
        typing.innerHTML =
          '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

        const typingWrap = document.createElement("div");
        typingWrap.className = "msg-wrap";
        typingWrap.id = "ai-typing-wrap";
        typingWrap.innerHTML = '<div class="msg-lbl">🤖 LinguistAI</div>';
        typingWrap.appendChild(typing);

        ml.appendChild(typingWrap);
        ml.scrollTop = ml.scrollHeight;

        try {
          const res = await apiFetch(`/api/sessions/${sessId}/respond/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ user_transcript: userText }),
          });

          document.getElementById("ai-typing-wrap")?.remove();

          if (res.status === 403) {
            const errData = await res.json();
            if (errData.turns_today !== undefined) {
              updateDailyTurnUI(errData.turns_today, 5);
            }
            document.getElementById("upgradeModal").style.display = "flex";
            return;
          }

          if (res.ok) {
            const data = await res.json();
            if (data.turns_today !== undefined) {
              updateDailyTurnUI(data.turns_today, data.daily_limit);
            }
            const aiMsg = document.createElement("div");
            aiMsg.className = "msg-wrap";
            const curLang = document.getElementById("conv-lang")?.textContent || "English";
            const voiceId = "ai-voice-" + Date.now() + "-" + Math.floor(Math.random() * 1000);
            const voicePill = createAiVoicePillHtml(data.ai_audio_url || "", voiceId, data.ai_response, curLang);
            aiMsg.innerHTML = `<div class="msg-lbl">🤖 LinguistAI</div><div class="msg-bubble msg-ai">${data.ai_response}</div>`;
            ml.appendChild(aiMsg);
            const pillWrapper = document.createElement("div");
            pillWrapper.innerHTML = voicePill;
            ml.appendChild(pillWrapper);
            ml.scrollTop = ml.scrollHeight;

            // Play voice via ElevenLabs or Browser Speech Synthesis
            playAiVoicePill(voiceId, true);

            if (data.feedback) {
              updateFeedbackUI(data.feedback);
            }
          }
        } catch (e) {
          document.getElementById("ai-typing")?.remove();
          console.error("Error submitting response:", e);
        }
      }

      // ── AUDIO VISUALIZER ENGINE (Web Audio API) ───────────────────
      let audioCtx = null;
      let analyserNode = null;
      let visualizerAnimId = null;

      function initAudioVisualizer(stream) {
        try {
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          if (!AudioContextClass) return;

          if (!audioCtx || audioCtx.state === "closed") {
            audioCtx = new AudioContextClass();
          }
          if (audioCtx.state === "suspended") {
            audioCtx.resume();
          }

          const source = audioCtx.createMediaStreamSource(stream);
          analyserNode = audioCtx.createAnalyser();
          analyserNode.fftSize = 64;
          analyserNode.smoothingTimeConstant = 0.8;
          source.connect(analyserNode);

          const wrap = document.getElementById("audio-visualizer-wrap");
          const canvas = document.getElementById("audio-visualizer-canvas");
          if (wrap && canvas) {
            wrap.classList.add("active");
            const ctx = canvas.getContext("2d");
            const bufferLength = analyserNode.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            function renderFrame() {
              visualizerAnimId = requestAnimationFrame(renderFrame);
              analyserNode.getByteFrequencyData(dataArray);

              ctx.clearRect(0, 0, canvas.width, canvas.height);
              const barCount = 20;
              const step = Math.max(1, Math.floor(bufferLength / barCount));
              const barWidth = 6;
              const gap = (canvas.width - barCount * barWidth) / (barCount - 1);

              for (let i = 0; i < barCount; i++) {
                const val = dataArray[i * step] || 0;
                const barHeight = Math.max(3, (val / 255) * canvas.height * 0.95);
                const x = i * (barWidth + gap);
                const y = (canvas.height - barHeight) / 2;

                const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
                gradient.addColorStop(0, "#ec4899");
                gradient.addColorStop(0.5, "#8b5cf6");
                gradient.addColorStop(1, "#4f46e5");

                ctx.fillStyle = gradient;
                ctx.beginPath();
                if (ctx.roundRect) {
                  ctx.roundRect(x, y, barWidth, barHeight, 3);
                } else {
                  ctx.rect(x, y, barWidth, barHeight);
                }
                ctx.fill();
              }
            }
            renderFrame();
          }
        } catch (err) {
          console.warn("Visualizer init warning:", err);
        }
      }

      function stopAudioVisualizer() {
        if (visualizerAnimId) {
          cancelAnimationFrame(visualizerAnimId);
          visualizerAnimId = null;
        }
        const wrap = document.getElementById("audio-visualizer-wrap");
        const canvas = document.getElementById("audio-visualizer-canvas");
        if (wrap) wrap.classList.remove("active");
        if (canvas) {
          const ctx = canvas.getContext("2d");
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }

      // ── SLEEK AI VOICE NOTE PLAYER CONTROLLER ─────────────────────
      const activeVoiceAudioMap = {};
      let activeSpeakingVoiceId = null;

      function createAiVoicePillHtml(audioUrl, voiceId, text, lang) {
        const cleanText = (text || "").replace(/"/g, "&quot;");
        const cleanLang = lang || "English";
        return `
          <div class="ai-voice-pill" id="pill-${voiceId}" data-url="${audioUrl || ""}" data-text="${cleanText}" data-lang="${cleanLang}" data-speed="1.0">
            <button class="btn-voice-play" id="btn-play-${voiceId}" onclick="toggleAiVoicePlayback('${voiceId}')" title="Play / Replay Voice">
              <i class="bi bi-play-fill" id="ico-play-${voiceId}"></i>
            </button>
            <div class="voice-wave-anim" id="wave-${voiceId}">
              <span></span><span></span><span></span><span></span><span></span>
            </div>
            <span class="voice-label" id="lbl-${voiceId}">Replay Voice</span>
            <div class="voice-speed-picker">
              <button class="btn-speed active" id="spd-1-${voiceId}" onclick="setVoicePlaybackSpeed('${voiceId}', 1.0, event)">1x</button>
              <button class="btn-speed" id="spd-075-${voiceId}" onclick="setVoicePlaybackSpeed('${voiceId}', 0.75, event)">0.75x</button>
            </div>
          </div>
        `;
      }

      function stopAllAiVoicePlaybacks(exceptVoiceId = null) {
        // 1. Stop HTML5 Audio objects
        Object.keys(activeVoiceAudioMap).forEach((id) => {
          if (id !== exceptVoiceId) {
            const a = activeVoiceAudioMap[id];
            if (a) {
              a.pause();
              a.currentTime = 0;
            }
            updateVoicePillUIState(id, false);
          }
        });

        // 2. Stop Web Speech Synthesis
        if (window.speechSynthesis) {
          try {
            window.speechSynthesis.cancel();
          } catch (e) {}
        }
        if (activeSpeakingVoiceId && activeSpeakingVoiceId !== exceptVoiceId) {
          updateVoicePillUIState(activeSpeakingVoiceId, false);
          activeSpeakingVoiceId = null;
        }
      }

      function updateVoicePillUIState(voiceId, isPlaying) {
        const pill = document.getElementById(`pill-${voiceId}`);
        const ico = document.getElementById(`ico-play-${voiceId}`);
        const lbl = document.getElementById(`lbl-${voiceId}`);
        if (!pill) return;
        if (isPlaying) {
          pill.classList.add("is-playing");
          if (ico) ico.className = "bi bi-pause-fill";
          if (lbl) lbl.textContent = "AI Speaking...";
        } else {
          pill.classList.remove("is-playing");
          if (ico) ico.className = "bi bi-play-fill";
          if (lbl) lbl.textContent = "Replay Voice";
        }
      }

      async function playAiVoicePill(voiceId, auto = false) {
        const pill = document.getElementById(`pill-${voiceId}`);
        if (!pill) return;
        let audioUrl = pill.getAttribute("data-url");
        const rawText = pill.getAttribute("data-text") || "";
        const text = rawText.replace(/&quot;/g, '"');
        const lang = pill.getAttribute("data-lang") || "English";
        const speed = parseFloat(pill.getAttribute("data-speed") || "1.0");

        stopAllAiVoicePlaybacks(voiceId);

        // If audioUrl is missing, fetch from backend TTS API
        if (!audioUrl && text) {
          try {
            updateVoicePillUIState(voiceId, true);
            const res = await fetch(
              `/api/tts/?text=${encodeURIComponent(text)}&lang=${encodeURIComponent(lang)}`
            );
            if (res.ok) {
              const data = await res.json();
              if (data.audio_url) {
                audioUrl = data.audio_url;
                pill.setAttribute("data-url", audioUrl);
              }
            }
          } catch (e) {
            console.warn("TTS API fetch failed:", e);
          }
        }

        // Path A: Remote ElevenLabs / Backend MP3 Audio URL exists
        if (audioUrl) {
          let audio = activeVoiceAudioMap[voiceId];
          if (!audio || (audio.src && !audio.src.endsWith(audioUrl))) {
            audio = new Audio(audioUrl);
            activeVoiceAudioMap[voiceId] = audio;
            audio.onplay = () => updateVoicePillUIState(voiceId, true);
            audio.onended = () => updateVoicePillUIState(voiceId, false);
            audio.onerror = () => {
              playSpeechSynthesisFallback(voiceId, text, lang, speed);
            };
          }
          audio.playbackRate = speed;
          audio.currentTime = 0;
          updateVoicePillUIState(voiceId, true);
          audio.play().catch((err) => {
            console.warn("Audio play prevented, falling back to Web Speech:", err);
            playSpeechSynthesisFallback(voiceId, text, lang, speed);
          });
          return;
        }

        // Path B: Built-in Web Speech Synthesis or Direct Audio Stream
        playSpeechSynthesisFallback(voiceId, text, lang, speed);
      }

      function playSpeechSynthesisFallback(voiceId, text, lang, speed = 1.0) {
        const langCodeMap = {
          English: "en",
          French: "fr",
          Spanish: "es",
          German: "de",
          Japanese: "ja",
          Chinese: "zh-CN",
          Korean: "ko",
          Vietnamese: "vi",
        };
        const langCode = langCodeMap[lang] || "en";

        if (window.speechSynthesis && window.speechSynthesis.getVoices().length > 0) {
          try {
            window.speechSynthesis.cancel();
            window.speechSynthesis.resume();
            const utter = new SpeechSynthesisUtterance(text);
            const fullLangMap = {
              English: "en-US",
              French: "fr-FR",
              Spanish: "es-ES",
              German: "de-DE",
              Japanese: "ja-JP",
              Chinese: "zh-CN",
              Korean: "ko-KR",
              Vietnamese: "vi-VN",
            };
            utter.lang = fullLangMap[lang] || "en-US";
            utter.rate = speed === 0.75 ? 0.75 : 1.0;
            activeSpeakingVoiceId = voiceId;

            utter.onstart = () => updateVoicePillUIState(voiceId, true);
            utter.onend = () => {
              updateVoicePillUIState(voiceId, false);
              activeSpeakingVoiceId = null;
            };
            utter.onerror = () => {
              activeSpeakingVoiceId = null;
              playDirectStreamTTS(voiceId, text, langCode, speed);
            };

            updateVoicePillUIState(voiceId, true);
            window.speechSynthesis.speak(utter);
            return;
          } catch (e) {
            console.warn("Speech synthesis error, falling back to direct stream:", e);
          }
        }

        playDirectStreamTTS(voiceId, text, langCode, speed);
      }

      function playDirectStreamTTS(voiceId, text, langCode, speed = 1.0) {
        try {
          const streamUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${langCode}&client=tw-ob&q=${encodeURIComponent((text || "").substring(0, 200))}`;
          const audio = new Audio(streamUrl);
          activeVoiceAudioMap[voiceId] = audio;
          audio.playbackRate = speed;
          audio.onplay = () => updateVoicePillUIState(voiceId, true);
          audio.onended = () => updateVoicePillUIState(voiceId, false);
          audio.onerror = () => updateVoicePillUIState(voiceId, false);
          updateVoicePillUIState(voiceId, true);
          audio.play().catch(() => updateVoicePillUIState(voiceId, false));
        } catch (e) {
          updateVoicePillUIState(voiceId, false);
        }
      }

      window.toggleAiVoicePlayback = function (voiceId) {
        const pill = document.getElementById(`pill-${voiceId}`);
        if (!pill) return;

        const isPlaying = pill.classList.contains("is-playing");
        if (isPlaying) {
          stopAllAiVoicePlaybacks();
        } else {
          playAiVoicePill(voiceId, false);
        }
      };

      window.setVoicePlaybackSpeed = function (voiceId, speed, event) {
        if (event) event.stopPropagation();
        const pill = document.getElementById(`pill-${voiceId}`);
        if (pill) {
          pill.setAttribute("data-speed", String(speed));
        }
        const audio = activeVoiceAudioMap[voiceId];
        if (audio) {
          audio.playbackRate = speed;
        }
        const btn1 = document.getElementById(`spd-1-${voiceId}`);
        const btn075 = document.getElementById(`spd-075-${voiceId}`);
        if (speed === 1.0) {
          btn1?.classList.add("active");
          btn075?.classList.remove("active");
        } else {
          btn075?.classList.add("active");
          btn1?.classList.remove("active");
        }
        if (pill?.classList.contains("is-playing") && !audio) {
          playAiVoicePill(voiceId, false);
        }
      };

      let speechRecognizer = null;
      let liveSpeechTranscript = "";

      function speakAiResponse(text, langName) {
        if (!window.speechSynthesis) return;
        try {
          window.speechSynthesis.cancel();
          const utter = new SpeechSynthesisUtterance(text);
          const langCodeMap = {
            English: "en-US",
            French: "fr-FR",
            Spanish: "es-ES",
            German: "de-DE",
            Japanese: "ja-JP",
            Chinese: "zh-CN",
            Korean: "ko-KR",
            Vietnamese: "vi-VN",
          };
          utter.lang = langCodeMap[langName] || "en-US";
          utter.rate = 0.95;
          window.speechSynthesis.speak(utter);
        } catch (e) {
          console.warn("Speech synthesis error:", e);
        }
      }

      async function toggleMic() {
        const btn = document.getElementById("mic-btn");
        const ico = document.getElementById("mic-icon");
        const st = document.getElementById("mic-status");
        const curLang =
          document.getElementById("conv-lang")?.textContent || "English";

        if (!micOn) {
          try {
            const stream = await navigator.mediaDevices.getUserMedia({
              audio: true,
            });
            audioChunks = [];
            liveSpeechTranscript = "";
            mediaRecorder = new MediaRecorder(stream);

            // Initialize Live Real-time Audio Visualizer
            initAudioVisualizer(stream);

            // Start browser native SpeechRecognition alongside MediaRecorder
            const SpeechRecognition =
              window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
              try {
                speechRecognizer = new SpeechRecognition();
                speechRecognizer.continuous = true;
                speechRecognizer.interimResults = true;
                const langCodeMap = {
                  English: "en-US",
                  French: "fr-FR",
                  Spanish: "es-ES",
                  German: "de-DE",
                  Japanese: "ja-JP",
                  Chinese: "zh-CN",
                  Korean: "ko-KR",
                  Vietnamese: "vi-VN",
                };
                speechRecognizer.lang = langCodeMap[curLang] || "en-US";
                speechRecognizer.onresult = (event) => {
                  let finalStr = "";
                  let interimStr = "";
                  for (
                    let i = event.resultIndex;
                    i < event.results.length;
                    ++i
                  ) {
                    if (event.results[i].isFinal) {
                      finalStr += event.results[i][0].transcript + " ";
                    } else {
                      interimStr += event.results[i][0].transcript;
                    }
                  }
                  if (finalStr) liveSpeechTranscript += finalStr;
                  const liveDisplay = (
                    liveSpeechTranscript + interimStr
                  ).trim();
                  if (st && liveDisplay) {
                    st.textContent = `🎙️ "${liveDisplay}"`;
                  }
                };
                speechRecognizer.start();
              } catch (re) {
                console.warn("SpeechRecognition init warning:", re);
              }
            }

            mediaRecorder.ondataavailable = (e) => {
              if (e.data.size > 0) audioChunks.push(e.data);
            };

            mediaRecorder.onstop = async () => {
              stopAudioVisualizer();
              stream.getTracks().forEach((track) => track.stop());
              if (speechRecognizer) {
                try {
                  speechRecognizer.stop();
                } catch (e) {}
              }
              const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
              await sendAudioResponse(audioBlob, liveSpeechTranscript.trim());
            };

            mediaRecorder.start();
            micOn = true;
            btn.classList.add("recording");
            ico.className = "bi bi-mic-mute-fill";
            st.textContent =
              "🔴 Recording… Speak now (Click mic when finished)";
            st.style.color = "#dc2626";
          } catch (err) {
            stopAudioVisualizer();
            console.warn("Microphone access unavailable or denied:", err);
            st.textContent =
              "Microphone unavailable. Please type below or enter sample text.";
            const userText = prompt(
              "Microphone access unavailable. Enter your message to practice:",
            );
            if (userText) submitUserMessage(userText);
          }
        } else {
          micOn = false;
          btn.classList.remove("recording");
          ico.className = "bi bi-mic-fill";
          st.textContent = "Processing audio & generating real-time response…";
          st.style.color = "";
          stopAudioVisualizer();
          if (speechRecognizer) {
            try {
              speechRecognizer.stop();
            } catch (e) {}
          }
          if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
          }
        }
      }

      async function sendAudioResponse(audioBlob, liveTranscript) {
        const sessId = await ensureActiveSession();
        if (!sessId) return;

        const ml = document.getElementById("msg-list");
        const typing = document.createElement("div");
        typing.className = "typing-indicator";
        typing.id = "ai-typing";
        typing.innerHTML =
          '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

        const typingWrap = document.createElement("div");
        typingWrap.className = "msg-wrap";
        typingWrap.id = "ai-typing-wrap";
        typingWrap.innerHTML = '<div class="msg-lbl">🤖 LinguistAI</div>';
        typingWrap.appendChild(typing);

        ml.appendChild(typingWrap);
        ml.scrollTop = ml.scrollHeight;

        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");
        if (liveTranscript) {
          formData.append("user_transcript", liveTranscript);
        }

        try {
          const res = await apiFetch(`/api/sessions/${sessId}/respond-audio/`, {
            method: "POST",
            credentials: "include",
            body: formData,
          });

          document.getElementById("ai-typing-wrap")?.remove();

          if (res.status === 403) {
            const errData = await res.json();
            document.getElementById("upgradeModal").style.display = "flex";
            return;
          }

          if (res.ok) {
            const data = await res.json();

            // Show user transcribed message in real-time
            const userMsg = document.createElement("div");
            userMsg.className = "msg-wrap msg-user-wrap";
            userMsg.innerHTML = `<div class="msg-lbl">🧑 You (Voice)</div><div class="msg-bubble msg-user">${data.user_transcript || liveTranscript || "Spoken Audio"}</div>`;
            ml.appendChild(userMsg);

            // Show AI response & auto-play synthesized voice using sleek Voice Pill
            const aiMsg = document.createElement("div");
            aiMsg.className = "msg-wrap";
            const curLang = document.getElementById("conv-lang")?.textContent || "English";
            const voiceId = "ai-voice-" + Date.now() + "-" + Math.floor(Math.random() * 1000);
            aiMsg.innerHTML = `<div class="msg-lbl">🤖 LinguistAI</div><div class="msg-bubble msg-ai">${data.ai_response}</div>`;
            ml.appendChild(aiMsg);
            const pillWrap = document.createElement("div");
            pillWrap.innerHTML = voicePill;
            ml.appendChild(pillWrap);
            ml.scrollTop = ml.scrollHeight;

            // Auto-play AI voice seamlessly in background
            playAiVoicePill(voiceId, true);

            // Update Live Feedback Panel in Real-Time
            if (data.feedback) {
              updateFeedbackUI(data.feedback);
            }
            const st = document.getElementById("mic-status");
            if (st) st.textContent = "Press the mic to start speaking";
          }
        } catch (e) {
          document.getElementById("ai-typing")?.remove();
          console.error("Error submitting audio response:", e);
        }
      }

      // ── AUTHENTICATION & DASHBOARD SYNC ────────────────────────────
      function resetAuthForm(clearInputs = true) {
        const errEl = document.getElementById("auth-error-msg");
        if (errEl) {
          errEl.textContent = "";
          errEl.style.display = "none";
        }
        const authErr = document.getElementById("auth-error");
        if (authErr) {
          authErr.textContent = "";
          authErr.style.display = "none";
        }
        const pwEl = document.getElementById("pw-input");
        if (pwEl) pwEl.value = "";

        if (clearInputs) {
          const nameEl = document.getElementById("auth-name");
          if (nameEl) nameEl.value = "";
          const emailEl = document.getElementById("auth-email");
          if (emailEl) emailEl.value = "";
          const targetLangEl = document.getElementById("auth-target-lang");
          if (targetLangEl) targetLangEl.value = "French";
          const cefrEl = document.getElementById("auth-cefr-level");
          if (cefrEl) cefrEl.value = "Beginner";
        }
      }

      function setAuthMode(m) {
        currentAuthMode = m;
        const isReg = m === "register";
        document.getElementById("tab-login").classList.toggle("active", !isReg);
        document
          .getElementById("tab-register")
          .classList.toggle("active", isReg);
        document.getElementById("name-field").style.display = isReg
          ? "block"
          : "none";
        const targetLangField = document.getElementById("target-lang-field");
        if (targetLangField)
          targetLangField.style.display = isReg ? "block" : "none";
        const cefrField = document.getElementById("cefr-level-field");
        if (cefrField) cefrField.style.display = isReg ? "block" : "none";

        document.getElementById("auth-heading").textContent = isReg
          ? "Create your account"
          : "Welcome back";
        document.getElementById("auth-sub").textContent = isReg
          ? "Start your language journey today"
          : "Sign in to continue your language journey";
        document.getElementById("auth-btn-lbl").textContent = isReg
          ? "Create Account"
          : "Sign In";
        resetAuthForm(false);
      }

      function togglePw() {
        const i = document.getElementById("pw-input");
        const e = document.getElementById("eye-i");
        i.type = i.type === "password" ? "text" : "password";
        e.className = i.type === "password" ? "bi bi-eye" : "bi bi-eye-slash";
      }

      async function handleAuthSubmit() {
        const email = document.getElementById("auth-email").value.trim();
        const password = document.getElementById("pw-input").value;
        const nameEl = document.getElementById("auth-name");
        const username =
          nameEl && nameEl.value.trim() ? nameEl.value.trim() : email;
        const targetLangEl = document.getElementById("auth-target-lang");
        const target_language = targetLangEl ? targetLangEl.value : "French";
        const cefrEl = document.getElementById("auth-cefr-level");
        const proficiency_level = cefrEl ? cefrEl.value : "Beginner";
        const errEl = document.getElementById("auth-error-msg");

        if (errEl) errEl.style.display = "none";

        if (!email || !password) {
          if (errEl) {
            errEl.textContent = "Please enter email and password.";
            errEl.style.display = "block";
          }
          return;
        }

        const endpoint =
          currentAuthMode === "register"
            ? "/api/auth/register/"
            : "/api/auth/login/";
        const payload = {
          email,
          username,
          password,
          target_language,
          proficiency_level,
        };

        try {
          const res = await apiFetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(payload),
          });
          const data = await res.json();
          if (res.ok && data.status === "success") {
            currentUser = data.user;
            currentUserId = currentUser.id;
            localStorage.setItem("linguist_user", JSON.stringify(currentUser));
            localStorage.setItem("linguist_user_id", currentUserId);
            resetAuthForm(true);
            updateUserNavUI(false, false);
            showPage("dashboard");
          } else {
            if (errEl) {
              errEl.textContent = data.error || "Authentication failed.";
              errEl.style.display = "block";
            }
          }
        } catch (e) {
          if (errEl) {
            errEl.textContent = "Network or server error. Please try again.";
            errEl.style.display = "block";
          }
        }
      }

      async function handleLogout() {
        try {
          await apiFetch("/api/auth/logout/", { method: "POST" });
        } catch (e) {}
        currentUser = null;
        currentUserId = "00000000-0000-0000-0000-000000000001";
        localStorage.removeItem("linguist_user");
        localStorage.removeItem("linguist_user_id");
        resetAuthForm(true);
        updateUserNavUI(true, false);
        showPage("landing");
      }

      let analyticsChartInstance = null;

      function renderAnalyticsChart(data) {
        if (typeof Chart === "undefined") return;
        const canvas = document.getElementById("analytics-chart");
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        if (analyticsChartInstance) {
          analyticsChartInstance.destroy();
        }

        const days =
          data && data.days
            ? data.days
            : ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        const grammarScores =
          data && data.grammar_series
            ? data.grammar_series
            : [80, 82, 85, 84, 88, 86, 90];
        const pronScores =
          data && data.pronunciation_series
            ? data.pronunciation_series
            : [78, 80, 82, 85, 84, 88, 89];

        analyticsChartInstance = new Chart(ctx, {
          type: "line",
          data: {
            labels: days,
            datasets: [
              {
                label: "Grammar Score",
                data: grammarScores,
                borderColor: "#4f46e5",
                backgroundColor: "rgba(79, 70, 229, 0.12)",
                fill: true,
                tension: 0.35,
                pointRadius: 4,
                pointBackgroundColor: "#4f46e5",
                pointHoverRadius: 6,
                borderWidth: 2.5,
              },
              {
                label: "Pronunciation Score",
                data: pronScores,
                borderColor: "#7c3aed",
                backgroundColor: "rgba(124, 58, 237, 0.08)",
                fill: true,
                tension: 0.35,
                pointRadius: 4,
                pointBackgroundColor: "#7c3aed",
                pointHoverRadius: 6,
                borderWidth: 2.5,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
              mode: "index",
              intersect: false,
            },
            plugins: {
              legend: {
                position: "bottom",
                labels: {
                  boxWidth: 12,
                  font: {
                    family: "'DM Sans', sans-serif",
                    size: 11,
                    weight: "600",
                  },
                },
              },
              tooltip: {
                backgroundColor: "#0f0f23",
                padding: 10,
                titleFont: {
                  family: "'DM Sans', sans-serif",
                  size: 12,
                  weight: "700",
                },
                bodyFont: { family: "'DM Sans', sans-serif", size: 11 },
                callbacks: {
                  label: function (context) {
                    return ` ${context.dataset.label}: ${context.parsed.y}%`;
                  },
                },
              },
            },
            scales: {
              y: {
                min: 50,
                max: 100,
                ticks: {
                  stepSize: 10,
                  callback: (value) => value + "%",
                  font: { size: 10, family: "'DM Sans', sans-serif" },
                },
                grid: { color: "rgba(79, 70, 229, 0.06)" },
              },
              x: {
                grid: { display: false },
                ticks: { font: { size: 11, family: "'DM Sans', sans-serif" } },
              },
            },
          },
        });
      }

      async function loadDashboardData() {
        if (!currentUserId) return;
        try {
          const [dashRes, analyticsRes] = await Promise.allSettled([
            apiFetch(`/api/dashboard/${currentUserId}/`),
            apiFetch(`/api/user/${currentUserId}/analytics/`),
          ]);

          if (dashRes.status === "fulfilled" && dashRes.value.ok) {
            const data = await dashRes.value.json();
            const welcome = document.getElementById("dash-welcome");
            if (welcome)
              welcome.textContent = `Welcome back, ${data.username}! 🔥`;

            const sSess = document.getElementById("dash-stat-sessions");
            if (sSess) sSess.textContent = data.total_sessions;

            const sGram = document.getElementById("dash-stat-grammar");
            if (sGram) sGram.textContent = `${data.average_grammar_score}%`;

            const sPron = document.getElementById("dash-stat-pron");
            if (sPron)
              sPron.textContent = `${data.average_pronunciation_score}%`;

            const sStreak = document.getElementById("dash-stat-streak");
            if (sStreak) sStreak.textContent = `${data.streak_days} days`;

            const recList = document.getElementById("dash-recent-list");
            if (recList && Array.isArray(data.recent_sessions)) {
              if (data.recent_sessions.length === 0) {
                recList.innerHTML =
                  '<div style="color:var(--muted-fg);font-size:.85rem">No sessions completed yet. Try starting a scenario!</div>';
              } else {
                recList.innerHTML = data.recent_sessions
                  .map(
                    (s) => `
            <div class="sess-row" style="cursor:pointer;" onclick="viewPastSessionSummary('${s.session_id}')" title="Click to view full lesson summary">
              <div class="sess-icon">${s.emoji || "💬"}</div>
              <div style="flex:1">
                <div style="font-weight:700;font-size:.875rem;display:flex;align-items:center;gap:6px">
                  ${s.scenario_title}
                  <span style="font-size:0.68rem;background:rgba(124,58,237,0.1);color:var(--primary);padding:1px 6px;border-radius:6px;font-weight:600"><i class="bi bi-file-earmark-text"></i> Review</span>
                </div>
                <div style="font-size:.75rem;color:var(--muted-fg)">${s.started_at ? new Date(s.started_at).toLocaleDateString([], { month: "short", day: "numeric" }) + " · " + new Date(s.started_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "Recent"} · ${s.lang || "English"}</div>
              </div>
              <span class="score-tag">Score: ${s.overall_score}%</span>
              <button onclick="event.stopPropagation(); startConv('${s.scenario_id}')" style="background:var(--secondary-bg);color:var(--primary);border:none;border-radius:8px;padding:6px 12px;font-size:.75rem;font-weight:700;cursor:pointer;font-family:'DM Sans',sans-serif" title="Practice this scenario again">
                <i class="bi bi-arrow-repeat"></i> Practice
              </button>
            </div>
          `,
                  )
                  .join("");
              }
            }
          }

          if (analyticsRes.status === "fulfilled" && analyticsRes.value.ok) {
            const analyticsData = await analyticsRes.value.json();
            renderAnalyticsChart(analyticsData);
          } else {
            renderAnalyticsChart(null);
          }
        } catch (e) {
          console.warn("Could not load dashboard data", e);
          renderAnalyticsChart(null);
        }
      }

      async function viewPastSessionSummary(sessionId) {
        if (!sessionId) return;
        try {
          const uid = currentUserId || (currentUser ? currentUser.id : "");
          const res = await apiFetch(
            `/api/sessions/${sessionId}/logs/?user_id=${encodeURIComponent(uid)}`,
          );
          if (!res.ok) {
            console.warn("Could not fetch session logs", res.status);
            return;
          }
          const data = await res.json();
          const history = data.history || [];

          // 1. Gather scores from feedback
          const gScores = [];
          const pScores = [];
          const vScores = [];
          const oScores = [];
          const allCorrections = [];
          const allSuggestions = [];
          const allVocab = [];
          let lastComments = "";

          history.forEach((log) => {
            const fb = log.detailed_feedback;
            if (fb && typeof fb === "object") {
              if (fb.grammar_score !== undefined)
                gScores.push(fb.grammar_score);
              if (fb.pronunciation_score !== undefined)
                pScores.push(fb.pronunciation_score);
              if (fb.vocabulary_score !== undefined)
                vScores.push(fb.vocabulary_score);
              const turnOverall = Math.round(
                ((fb.grammar_score || 85) + (fb.pronunciation_score || 80)) / 2,
              );
              oScores.push(turnOverall);
              if (fb.comments) lastComments = fb.comments;

              if (Array.isArray(fb.corrections)) {
                fb.corrections.forEach((c) => allCorrections.push(c));
              }
              if (Array.isArray(fb.suggestions)) {
                fb.suggestions.forEach((s) => {
                  if (!allSuggestions.includes(s)) allSuggestions.push(s);
                });
              }
              if (Array.isArray(fb.extracted_vocabulary)) {
                fb.extracted_vocabulary.forEach((v) => {
                  if (
                    !allVocab.some(
                      (item) =>
                        item.word.toLowerCase() === v.word.toLowerCase(),
                    )
                  ) {
                    allVocab.push(v);
                  }
                });
              }
            }
          });

          const avg = (arr) =>
            arr.length > 0
              ? Math.round(arr.reduce((a, b) => a + b, 0) / arr.length)
              : 85;
          const avgG = avg(gScores);
          const avgP = avg(pScores);
          const avgV = avg(vScores);
          const avgO =
            data.overall_score ||
            (oScores.length > 0 ? avg(oScores) : Math.round((avgG + avgP) / 2));

          // 2. Populate KPI cards
          document.getElementById("sum-overall-score").textContent = `${avgO}%`;
          document.getElementById("sum-grammar-score").textContent = `${avgG}%`;
          document.getElementById("sum-pronun-score").textContent = `${avgP}%`;
          document.getElementById("sum-vocab-score").textContent = `${avgV}%`;

          // 3. Hero Subtitle & Emoji
          document.getElementById("sum-emoji").textContent =
            data.scenario_emoji || "💬";
          const formattedDate = data.started_at
            ? new Date(data.started_at).toLocaleDateString([], {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })
            : "Previous Lesson";
          document.getElementById("sum-subtitle").textContent =
            `${data.scenario_title} (${data.scenario_lang}) · ${history.length} turns recorded on ${formattedDate}`;

          // 4. AI Comments
          const commentsDiv = document.getElementById("sum-ai-comments");
          if (lastComments) {
            commentsDiv.textContent = lastComments;
          } else if (history.length === 0) {
            commentsDiv.textContent =
              "This session was recorded with 0 conversation turns.";
          } else {
            commentsDiv.textContent =
              "Completed conversation session. Your grammar and pronunciation accuracy were tracked across turns.";
          }

          // 5. Corrections list
          const correctionsWrap = document.getElementById(
            "sum-corrections-wrap",
          );
          const correctionsList = document.getElementById(
            "sum-corrections-list",
          );
          if (allCorrections.length > 0) {
            correctionsWrap.style.display = "block";
            correctionsList.innerHTML = allCorrections
              .map(
                (c) => `
            <div style="background:#fef2f2;border:1px solid #fee2e2;border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:0.85rem;">
              <div style="color:#dc2626;text-decoration:line-through;margin-bottom:2px;">${c.original}</div>
              <div style="color:#16a34a;font-weight:700;">➔ ${c.corrected}</div>
              <div style="color:#6b7280;font-size:0.78rem;margin-top:4px;">${c.explanation}</div>
            </div>
          `,
              )
              .join("");
          } else {
            correctionsWrap.style.display = "none";
          }

          // 6. Suggestions list
          const suggestionsWrap = document.getElementById(
            "sum-suggestions-wrap",
          );
          const suggestionsList = document.getElementById(
            "sum-suggestions-list",
          );
          if (allSuggestions.length > 0) {
            suggestionsWrap.style.display = "block";
            suggestionsList.innerHTML = allSuggestions
              .map(
                (s) => `
            <div style="background:#fffbeb;border:1px solid #fef3c7;border-radius:10px;padding:8px 12px;margin-bottom:6px;font-size:0.85rem;color:#92400e;display:flex;align-items:center;gap:8px;">
              <span>💡</span><span>${s}</span>
            </div>
          `,
              )
              .join("");
          } else {
            suggestionsWrap.style.display = "none";
          }

          // 7. Vocabulary list
          const vocabListDiv = document.getElementById("sum-vocab-list");
          if (allVocab.length > 0) {
            vocabListDiv.innerHTML = allVocab
              .map(
                (v) => `
            <div class="summary-vocab-item">
              <div style="font-weight:700;color:var(--primary);font-size:0.95rem;">🌟 ${v.word}</div>
              <div style="color:#4b5563;font-size:0.82rem;margin-top:2px;">${v.translation || ""}</div>
              ${v.example ? `<div style="color:#9ca3af;font-size:0.75rem;font-style:italic;margin-top:4px;">"${v.example}"</div>` : ""}
            </div>
          `,
              )
              .join("");
          } else {
            vocabListDiv.innerHTML = `<div style="text-align:center;color:var(--muted-fg);font-size:0.85rem;padding:20px;">No new words were extracted in this session.</div>`;
          }

          // 8. Open summary page
          showPage("summary");
        } catch (e) {
          console.error("Error loading past session summary:", e);
        }
      }

      async function loadProfileData() {
        if (!currentUserId) return;
        try {
          const res = await apiFetch(`/api/auth/me/`);
          let user = currentUser;
          if (res.ok) {
            const data = await res.json();
            if (data.authenticated && data.user) {
              user = data.user;
              currentUser = user;
            }
          }

          if (user) {
            const displayName = user.username || user.email || "Learner";
            const email = user.email || "";
            const initial = (displayName[0] || "U").toUpperCase();

            document.getElementById("prof-avatar").textContent = initial;
            document.getElementById("prof-name-display").textContent =
              displayName;
            document.getElementById("prof-email-display").textContent = email;
            const isVip = user.subscription_plan === "VIP";
            document.getElementById("prof-plan-display").textContent = isVip
              ? "VIP Plan ⭐"
              : "Free Tier";
            const upgradeBtn = document.getElementById("prof-upgrade-btn");
            if (upgradeBtn) {
              upgradeBtn.style.display = isVip ? "none" : "inline-flex";
            }
            document.getElementById("prof-username-input").value = displayName;
            document.getElementById("prof-email-input").value = email;

            if (user.proficiency_level) {
              const profSel = document.getElementById(
                "prof-proficiency-select",
              );
              if (profSel) profSel.value = user.proficiency_level;
            }
            if (user.target_language) {
              const langSel = document.getElementById(
                "prof-target-lang-select",
              );
              if (langSel) langSel.value = user.target_language;
            }
          }

          // Load stats into profile
          const dashRes = await apiFetch(`/api/dashboard/${currentUserId}/`);
          if (dashRes.ok) {
            const d = await dashRes.json();
            document.getElementById("prof-stats-sessions").textContent =
              d.total_sessions || 0;
            document.getElementById("prof-stats-grammar").textContent =
              `${d.average_grammar_score || 85}%`;
            document.getElementById("prof-stats-pron").textContent =
              `${d.average_pronunciation_score || 82}%`;
            document.getElementById("prof-stats-streak").textContent =
              `🔥${d.streak_days || 0}`;
          }
        } catch (e) {
          console.warn("Could not load profile data", e);
        }
      }

      async function handleSaveProfile() {
        const username = document
          .getElementById("prof-username-input")
          .value.trim();
        const proficiency_level = document.getElementById(
          "prof-proficiency-select",
        ).value;
        const target_language = document.getElementById(
          "prof-target-lang-select",
        ).value;
        const feedbackEl = document.getElementById("prof-feedback-msg");
        const btn = document.getElementById("prof-save-btn");

        if (btn) {
          btn.disabled = true;
          btn.textContent = "Saving...";
        }

        try {
          const res = await apiFetch("/api/user/profile/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username,
              proficiency_level,
              target_language,
            }),
          });
          const data = await res.json();
          if (res.ok && data.status === "success") {
            currentUser = data.user;
            localStorage.setItem("linguist_user", JSON.stringify(currentUser));
            if (feedbackEl) {
              feedbackEl.style.display = "block";
              feedbackEl.style.background = "#ecfdf5";
              feedbackEl.style.color = "#065f46";
              feedbackEl.style.border = "1px solid #a7f3d0";
              feedbackEl.textContent =
                "✓ Profile preferences saved successfully!";
              setTimeout(() => {
                feedbackEl.style.display = "none";
              }, 4000);
            }
            loadProfileData();
          } else {
            if (feedbackEl) {
              feedbackEl.style.display = "block";
              feedbackEl.style.background = "#fef2f2";
              feedbackEl.style.color = "#991b1b";
              feedbackEl.style.border = "1px solid #fecaca";
              feedbackEl.textContent = data.error || "Failed to save changes.";
            }
          }
        } catch (e) {
          if (feedbackEl) {
            feedbackEl.style.display = "block";
            feedbackEl.style.background = "#fef2f2";
            feedbackEl.style.color = "#991b1b";
            feedbackEl.style.border = "1px solid #fecaca";
            feedbackEl.textContent = "Network error saving profile.";
          }
        } finally {
          if (btn) {
            btn.disabled = false;
            btn.textContent = "Save Changes";
          }
        }
      }

      // Check session and route on load
      document.addEventListener("DOMContentLoaded", async () => {
        // Step 0: Fastest check — restore user from localStorage immediately
        if (!currentUser) {
          const savedUser = localStorage.getItem("linguist_user");
          if (savedUser) {
            try {
              currentUser = JSON.parse(savedUser);
              currentUserId = currentUser.id;
            } catch (e) {
              localStorage.removeItem("linguist_user");
            }
          }
        }

        // Step 2: Validate Django session — only clear user if no user from any source
        try {
          const res = await apiFetch("/api/auth/me/");
          if (res.ok) {
            const meData = await res.json();
            if (meData.authenticated && meData.user) {
              currentUser = meData.user;
              currentUserId = currentUser.id;
              localStorage.setItem(
                "linguist_user",
                JSON.stringify(currentUser),
              );
              localStorage.setItem("linguist_user_id", currentUserId);
              updateDailyTurnUI(
                currentUser.today_turns,
                currentUser.daily_limit,
              );
            }
          }
        } catch (e) {}

        const urlParams = new URLSearchParams(window.location.search);
        let pageFromUrl = urlParams.get("page");
        if (
          !pageFromUrl &&
          window.location.hash &&
          !window.location.hash.includes("access_token")
        ) {
          pageFromUrl = window.location.hash.replace("#", "");
        }

        let targetPage = pageFromUrl;
        if (PROTECTED_PAGES.includes(targetPage) && !currentUser) {
          targetPage = "login";
          const errEl = document.getElementById("auth-error-msg");
          if (errEl) {
            errEl.textContent =
              "Please sign in or create an account to start practicing!";
            errEl.style.display = "block";
          }
        }

        // If visits root (no ?page specified), default to dashboard for users, landing for guests
        if (!targetPage) {
          targetPage = currentUser ? "dashboard" : "landing";
        }

        updateUserNavUI(targetPage === "landing", targetPage === "login");
        showPage(targetPage, false);
      });

      // --- Turn Limit Counter Logic ---
      let userTodayTurns = 0;
      let userDailyLimit = 5;

      function updateDailyTurnUI(todayTurns, dailyLimit) {
        if (todayTurns !== undefined && todayTurns !== null) {
          userTodayTurns = todayTurns;
        } else if (currentUser && currentUser.today_turns !== undefined) {
          userTodayTurns = currentUser.today_turns;
        }
        if (dailyLimit !== undefined && dailyLimit !== null) {
          userDailyLimit = dailyLimit;
        } else if (currentUser && currentUser.daily_limit !== undefined) {
          userDailyLimit = currentUser.daily_limit;
        }

        const plan = (currentUser && (currentUser.subscription_plan || "")).toUpperCase();
        const role = (currentUser && (currentUser.role || "")).toUpperCase();
        const isVip =
          plan === "VIP" ||
          plan === "PRO" ||
          role === "ADMIN" ||
          (currentUser && currentUser.daily_limit === null) ||
          (currentUser && currentUser.is_vip);

        const card = document.getElementById("scen-turn-card");
        const statusText = document.getElementById("scen-turn-status-text");
        const vipBadge = document.getElementById("scen-turn-vip-badge");
        const subText = document.getElementById("scen-turn-sub");
        const progressWrap = document.getElementById("scen-turn-progress-wrap");
        const progressFill = document.getElementById("scen-turn-progress-fill");
        const upgradeBtn = document.getElementById("btn-scen-upgrade");
        const convBadge = document.getElementById("conv-turn-badge");
        const convText = document.getElementById("conv-turns-text");
        const ftBadge = document.getElementById("ft-turn-badge");
        const ftText = document.getElementById("ft-turns-text");

        if (isVip) {
          if (card) card.classList.add("vip");
          if (statusText)
            statusText.innerHTML = `Daily Turn Limit: <strong>Unlimited Access</strong>`;
          if (vipBadge) vipBadge.style.display = "inline-flex";
          if (subText)
            subText.textContent = `You are a VIP Member! Enjoy unrestricted AI conversational practice.`;
          if (progressWrap) progressWrap.style.display = "none";
          if (upgradeBtn) upgradeBtn.style.display = "none";

          if (convBadge) {
            convBadge.className = "conv-turn-badge vip";
            convBadge.innerHTML = '<i class="bi bi-gem"></i> VIP Unlimited';
          }
          if (ftBadge) {
            ftBadge.className = "conv-turn-badge vip";
            ftBadge.innerHTML = '<i class="bi bi-gem"></i> VIP Unlimited';
          }
        } else {
          const limit = userDailyLimit || 5;
          const remaining = Math.max(0, limit - userTodayTurns);
          const percent = Math.min(100, Math.max(0, (remaining / limit) * 100));

          if (card) card.classList.remove("vip");
          if (vipBadge) vipBadge.style.display = "none";
          if (progressWrap) progressWrap.style.display = "block";
          if (upgradeBtn) upgradeBtn.style.display = "inline-flex";

          if (statusText) {
            statusText.innerHTML = `Daily Practice Turns: <strong><span id="scen-turns-remaining">${remaining}</span> / ${limit} remaining today</strong>`;
          }

          if (subText) {
            if (remaining === 0) {
              subText.innerHTML = `<span style="color:#dc2626;font-weight:600">Daily limit reached (0/${limit}).</span> Upgrade to VIP for unlimited turns.`;
            } else {
              subText.textContent = `Free plan includes ${limit} turns per day. Resets daily at midnight.`;
            }
          }

          if (progressFill) {
            progressFill.style.width = `${percent}%`;
            progressFill.className =
              "scen-turn-progress-fill" +
              (remaining <= 1 ? (remaining === 0 ? " empty" : " warn") : "");
          }

          if (convBadge && convText) {
            convBadge.className =
              "conv-turn-badge" +
              (remaining <= 1 ? (remaining === 0 ? " empty" : " warn") : "");
            convText.textContent = `${remaining} / ${limit} turns left`;
          }

          if (ftBadge && ftText) {
            ftBadge.className =
              "conv-turn-badge" +
              (remaining <= 1 ? (remaining === 0 ? " empty" : " warn") : "");
            ftText.textContent = `${remaining} / ${limit} turns left`;
          }
        }
      }

    // --- UX/UI Upgrades & Payment Form ---
      let selectedPaymentPlan = "annual"; // 'monthly' ($29.99) or 'annual' ($239.88)

      // Cross-tab Synchronization Listener
      window.addEventListener("storage", (e) => {
        if (e.key === "linguist_user") {
          try {
            currentUser = e.newValue ? JSON.parse(e.newValue) : null;
            currentUserId = currentUser
              ? currentUser.id
              : "00000000-0000-0000-0000-000000000001";
            updateUserNavUI(false, false);
            updateDailyTurnUI();
          } catch (err) {}
        }
      });

      function selectPaymentPlan(plan) {
        selectedPaymentPlan = plan === "monthly" ? "monthly" : "annual";

        const monthlyCard = document.getElementById("plan-card-monthly");
        const annualCard = document.getElementById("plan-card-annual");
        const summaryTitle = document.getElementById("pay-summary-title");
        const summarySub = document.getElementById("pay-summary-sub");
        const summaryAmount = document.getElementById("pay-summary-amount");
        const summaryUnit = document.getElementById("pay-summary-unit");
        const submitBtn = document.getElementById("btn-pay-submit");
        const pill = document.getElementById("pay-header-pill");

        if (selectedPaymentPlan === "monthly") {
          if (monthlyCard) monthlyCard.classList.add("active");
          if (annualCard) annualCard.classList.remove("active");
          if (summaryTitle)
            summaryTitle.textContent = "LinguistAI VIP Monthly Plan";
          if (summarySub)
            summarySub.textContent = "Billed monthly • Cancel anytime";
          if (summaryAmount) summaryAmount.textContent = "$29.99";
          if (summaryUnit) summaryUnit.textContent = "AUD / mo";
          if (pill)
            pill.innerHTML =
              '<i class="bi bi-check-circle-fill"></i> VIP Monthly Membership — $29.99 AUD / month';
          if (submitBtn && !submitBtn.disabled) {
            submitBtn.innerHTML =
              '<i class="bi bi-shield-lock-fill"></i> Confirm & Upgrade ($29.99 AUD)';
          }
        } else {
          if (monthlyCard) monthlyCard.classList.remove("active");
          if (annualCard) annualCard.classList.add("active");
          if (summaryTitle)
            summaryTitle.textContent = "LinguistAI VIP Annual Plan (Save 33%)";
          if (summarySub)
            summarySub.textContent =
              "Billed $239.88 AUD/year (~$19.99/mo) • Cancel anytime";
          if (summaryAmount) summaryAmount.textContent = "$239.88";
          if (summaryUnit) summaryUnit.textContent = "AUD / yr";
          if (pill)
            pill.innerHTML =
              '<i class="bi bi-check-circle-fill"></i> VIP Annual Membership — $239.88 AUD (~$19.99/mo)';
          if (submitBtn && !submitBtn.disabled) {
            submitBtn.innerHTML =
              '<i class="bi bi-shield-lock-fill"></i> Confirm & Upgrade ($239.88 AUD)';
          }
        }
      }

      function handlePricingPlanClick(plan) {
        if (currentUser) {
          openPaymentModal(plan);
        } else {
          showPage("login");
        }
      }

      function closeUpgradeModal() {
        const modal = document.getElementById("upgradeModal");
        if (modal) modal.style.display = "none";
        if (document.getElementById("text-fallback-input")) {
          document.getElementById("text-fallback-input").value = "";
        }
      }

      // Open Payment Checkout Modal
      function openPaymentModal(plan = "annual") {
        closeUpgradeModal();
        const modal = document.getElementById("paymentModal");
        if (!modal) return;

        // Reset form fields and validation errors
        const form = document.getElementById("payment-checkout-form");
        if (form) form.reset();
        clearPaymentErrors();

        // Set initial plan
        selectPaymentPlan(plan);

        // Prefill cardholder name with current user name if available
        if (currentUser) {
          const nameInput = document.getElementById("pay-cardholder");
          if (nameInput && !nameInput.value) {
            nameInput.value = currentUser.username || "";
          }
        }

        modal.style.display = "flex";
      }

      function closePaymentModal() {
        const modal = document.getElementById("paymentModal");
        if (modal) modal.style.display = "none";
        clearPaymentErrors();
      }

      function clearPaymentErrors() {
        const inputs = document.querySelectorAll(".pay-input");
        inputs.forEach((inp) => {
          inp.classList.remove("is-invalid", "is-valid");
        });
        const errors = document.querySelectorAll(".pay-field-error");
        errors.forEach((err) => {
          err.style.display = "none";
          err.textContent = "";
        });
        const globalErr = document.getElementById("pay-global-error");
        if (globalErr) {
          globalErr.style.display = "none";
          globalErr.textContent = "";
        }
      }

      // Luhn Algorithm Card Check
      function isValidLuhn(numStr) {
        let sum = 0;
        let isEven = false;
        for (let i = numStr.length - 1; i >= 0; i--) {
          let digit = parseInt(numStr.charAt(i), 10);
          if (isNaN(digit)) return false;
          if (isEven) {
            digit *= 2;
            if (digit > 9) digit -= 9;
          }
          sum += digit;
          isEven = !isEven;
        }
        return sum % 10 === 0;
      }

      // Detect card brand
      function detectCardBrand(numStr) {
        const clean = numStr.replace(/\D/g, "");
        if (/^4/.test(clean)) return "VISA";
        if (/^5[1-5]/.test(clean) || /^2[2-7]/.test(clean)) return "MasterCard";
        if (/^3[47]/.test(clean)) return "AMEX";
        if (/^35/.test(clean)) return "JCB";
        if (/^6(?:011|5)/.test(clean)) return "Discover";
        return "CARD";
      }

      function setFieldError(fieldId, errorMsg) {
        const input = document.getElementById(fieldId);
        const errorEl = document.getElementById(fieldId + "-error");
        if (input) {
          input.classList.add("is-invalid");
          input.classList.remove("is-valid");
        }
        if (errorEl) {
          errorEl.textContent = errorMsg;
          errorEl.style.display = "block";
        }
      }

      function clearFieldError(fieldId) {
        const input = document.getElementById(fieldId);
        const errorEl = document.getElementById(fieldId + "-error");
        if (input) {
          input.classList.remove("is-invalid");
          input.classList.add("is-valid");
        }
        if (errorEl) {
          errorEl.style.display = "none";
          errorEl.textContent = "";
        }
      }

      function validatePaymentForm() {
        let isValid = true;
        clearPaymentErrors();

        // 1. Cardholder Name
        const nameInput = document.getElementById("pay-cardholder");
        const nameVal = nameInput ? nameInput.value.trim() : "";
        if (!nameVal || nameVal.length < 3) {
          setFieldError(
            "pay-cardholder",
            "Please enter the full cardholder name (minimum 3 characters).",
          );
          isValid = false;
        } else {
          clearFieldError("pay-cardholder");
        }

        // 2. Card Number
        const cardInput = document.getElementById("pay-cardnumber");
        const cardRaw = cardInput ? cardInput.value.replace(/\s+/g, "") : "";
        if (!cardRaw) {
          setFieldError(
            "pay-cardnumber",
            "Please enter your credit or debit card number.",
          );
          isValid = false;
        } else if (!/^\d{16}$/.test(cardRaw)) {
          setFieldError(
            "pay-cardnumber",
            "Card number must be exactly 16 digits.",
          );
          isValid = false;
        } else if (!isValidLuhn(cardRaw)) {
          setFieldError(
            "pay-cardnumber",
            "Invalid card number checksum. Please verify the digits.",
          );
          isValid = false;
        } else {
          clearFieldError("pay-cardnumber");
        }

        // 3. Expiration Date (MM/YY)
        const expInput = document.getElementById("pay-expiry");
        const expVal = expInput ? expInput.value.trim() : "";
        const expMatch = expVal.match(/^(0[1-9]|1[0-2])\/(\d{2})$/);
        if (!expMatch) {
          setFieldError("pay-expiry", "Enter valid format MM/YY (e.g. 12/28).");
          isValid = false;
        } else {
          const month = parseInt(expMatch[1], 10);
          const year = 2000 + parseInt(expMatch[2], 10);
          const now = new Date();
          const currentYear = now.getFullYear();
          const currentMonth = now.getMonth() + 1;

          if (
            year < currentYear ||
            (year === currentYear && month < currentMonth)
          ) {
            setFieldError("pay-expiry", "Card has expired.");
            isValid = false;
          } else if (year > currentYear + 20) {
            setFieldError("pay-expiry", "Invalid expiration year.");
            isValid = false;
          } else {
            clearFieldError("pay-expiry");
          }
        }

        // 4. CVV
        const cvvInput = document.getElementById("pay-cvv");
        const cvvVal = cvvInput ? cvvInput.value.trim() : "";
        if (!cvvVal || !/^\d{3,4}$/.test(cvvVal)) {
          setFieldError("pay-cvv", "CVV must be 3 or 4 digits.");
          isValid = false;
        } else {
          clearFieldError("pay-cvv");
        }

        return isValid;
      }

      // Submit Payment & Upgrade
      async function handlePaymentSubmit(e) {
        if (e && e.preventDefault) e.preventDefault();

        if (!validatePaymentForm()) {
          return;
        }

        const submitBtn = document.getElementById("btn-pay-submit");
        const globalErr = document.getElementById("pay-global-error");

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML =
            '<i class="bi bi-arrow-repeat spin-icon"></i> Processing Secure Payment...';
        }

        const isAnnual = selectedPaymentPlan === "annual";
        const amount = isAnnual ? 239.88 : 29.99;

        const payload = {
          cardholder_name: document
            .getElementById("pay-cardholder")
            .value.trim(),
          card_number: document
            .getElementById("pay-cardnumber")
            .value.replace(/\s+/g, ""),
          expiry: document.getElementById("pay-expiry").value.trim(),
          cvv: document.getElementById("pay-cvv").value.trim(),
          postal_code: document.getElementById("pay-postal")
            ? document.getElementById("pay-postal").value.trim()
            : "",
          country: document.getElementById("pay-country")
            ? document.getElementById("pay-country").value
            : "VN",
          billing_cycle: selectedPaymentPlan,
          amount: amount,
          currency: "AUD",
          plan: "VIP",
        };

        try {
          const res = await apiFetch("/api/auth/upgrade/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });

          const data = await res.json();

          if (res.ok) {
            if (submitBtn) {
              submitBtn.style.background =
                "linear-gradient(135deg, #10b981 0%, #059669 100%)";
              submitBtn.innerHTML =
                '<i class="bi bi-check-circle-fill"></i> Payment Successful! Upgraded to VIP';
            }

            if (currentUser) {
              currentUser.subscription_plan = "VIP";
              localStorage.setItem(
                "linguist_user",
                JSON.stringify(currentUser),
              );
              updateUserNavUI(false, false);
              updateDailyTurnUI(0, null);
            }

            // Update profile display if on profile page
            const profPlan = document.getElementById("prof-plan-display");
            if (profPlan) profPlan.textContent = "VIP Plan ⭐";
            const profUpBtn = document.getElementById("prof-upgrade-btn");
            if (profUpBtn) profUpBtn.style.display = "none";

            setTimeout(() => {
              closePaymentModal();
              alert(
                "🎉 Congratulations! Your payment has been processed and your account is upgraded to VIP (Unlimited Practice)!",
              );
            }, 1000);
          } else {
            if (globalErr) {
              globalErr.textContent =
                data.error || "Payment authorization failed. Please try again.";
              globalErr.style.display = "block";
            }
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.innerHTML = `<i class="bi bi-shield-lock-fill"></i> Try Again ($${amount} AUD)`;
            }
          }
        } catch (err) {
          if (globalErr) {
            globalErr.textContent =
              "Network or server error processing payment. Please try again.";
            globalErr.style.display = "block";
          }
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="bi bi-shield-lock-fill"></i> Try Again ($${amount} AUD)`;
          }
        }
      }

      // Input masking & auto-formatting setup
      function setupPaymentInputFormatters() {
        // 1. Card number spacing & brand detect
        const cardInput = document.getElementById("pay-cardnumber");
        const brandBadge = document.getElementById("pay-brand-badge");
        if (cardInput) {
          cardInput.addEventListener("input", function (e) {
            let val = this.value.replace(/\D/g, "");
            if (val.length > 16) val = val.substring(0, 16);
            // format into groups of 4 (max 16 digits: XXXX XXXX XXXX XXXX)
            const parts = [];
            for (let i = 0; i < val.length; i += 4) {
              parts.push(val.substring(i, i + 4));
            }
            this.value = parts.join(" ");

            if (brandBadge) {
              brandBadge.textContent = detectCardBrand(val);
            }
          });
        }

        // 2. Expiry MM/YY auto slash
        const expInput = document.getElementById("pay-expiry");
        if (expInput) {
          expInput.addEventListener("input", function (e) {
            let val = this.value.replace(/\D/g, "");
            if (val.length > 4) val = val.substring(0, 4);
            if (val.length >= 2) {
              this.value = val.substring(0, 2) + "/" + val.substring(2);
            } else {
              this.value = val;
            }
          });
        }

        // 3. CVV digits only
        const cvvInput = document.getElementById("pay-cvv");
        if (cvvInput) {
          cvvInput.addEventListener("input", function (e) {
            this.value = this.value.replace(/\D/g, "").substring(0, 4);
          });
        }
      }

      window.addEventListener("DOMContentLoaded", () => {
        setupPaymentInputFormatters();
      });

      function handleTextSubmit(e) {
        if (e.key === "Enter") {
          submitTextFallback();
        }
      }

      function submitTextFallback() {
        const input = document.getElementById("text-fallback-input");
        const text = input.value.trim();
        if (text) {
          input.value = "";
          submitUserMessage(text);
        }
      }

      // Toggle Text Input Fallback if Mic fails or user prefers it
      // Already in HTML, just handle display logic if needed (it's visible now by default in HTML? No, we set display:none. Let's make it display:flex)
      document.getElementById("text-fallback-container").style.display = "flex";

      // --- Anki Flashcards ---
      let dueCards = [];
      let currentCardIndex = 0;

      const LANG_EMOJIS = {
        English: "🇬🇧",
        French: "🇫🇷",
        Spanish: "🇪🇸",
        German: "🇩🇪",
        Japanese: "🇯🇵",
        Chinese: "🇨🇳",
        Korean: "🇰🇷",
        Vietnamese: "🇻🇳",
      };

      let selectedFlashcardLang = "All";
      let availableFlashcardLangs = [];

      function startFlashcardPracticeForSession() {
        const currentScen = SCENARIOS.find(
          (x) => String(x.id) === String(currentScenarioId),
        );
        const targetLang = currentScen ? currentScen.lang || "English" : "All";
        showPage("flashcards");
        loadFlashcards(targetLang);
      }

      let isReviewAllMode = false;

      async function loadFlashcards(lang, includeAll = false) {
        if (lang !== undefined) {
          selectedFlashcardLang = lang;
        }
        isReviewAllMode = includeAll;
        try {
          const uid = currentUserId || (currentUser ? currentUser.id : "");
          const langParam = selectedFlashcardLang
            ? encodeURIComponent(selectedFlashcardLang)
            : "All";
          const allParam = includeAll ? "&all=true" : "";
          const res = await apiFetch(
            `/api/flashcards/due/?lang=${langParam}${allParam}&user_id=${encodeURIComponent(uid)}`,
          );
          if (res.ok) {
            const data = await res.json();
            dueCards = data.due_cards || [];
            availableFlashcardLangs = data.available_languages || [];
            currentCardIndex = 0;
            renderFlashcardLanguageTabs();
            renderCurrentCard();
          }
        } catch (e) {
          console.error("Failed to load flashcards", e);
        }
      }

      const SUPPORTED_LANGUAGES = [
        "English",
        "French",
        "Spanish",
        "German",
        "Japanese",
        "Chinese",
        "Korean",
        "Vietnamese",
      ];

      function renderFlashcardLanguageTabs() {
        const tabsContainer = document.getElementById("fc-lang-tabs");
        if (!tabsContainer) return;

        // Merge available stats with list of languages
        const statsMap = {};
        let totalDue = 0;
        let totalAllCards = 0;
        (availableFlashcardLangs || []).forEach((l) => {
          statsMap[l.language.toLowerCase()] = l;
          totalDue += l.due_count || 0;
          totalAllCards += l.total_count || 0;
        });

        // Collect active languages with cards
        const activeLangs = [];
        SUPPORTED_LANGUAGES.forEach((langName) => {
          const stat = statsMap[langName.toLowerCase()];
          if (stat && stat.total_count > 0) {
            activeLangs.push({
              name: langName,
              due_count: stat.due_count,
              total_count: stat.total_count,
            });
          }
        });

        // If user has other custom languages
        (availableFlashcardLangs || []).forEach((l) => {
          if (
            !SUPPORTED_LANGUAGES.map((x) => x.toLowerCase()).includes(
              l.language.toLowerCase(),
            )
          ) {
            activeLangs.push({
              name: l.language,
              due_count: l.due_count,
              total_count: l.total_count,
            });
          }
        });

        // If no languages have cards yet, show standard languages
        const displayLangs =
          activeLangs.length > 0
            ? activeLangs
            : SUPPORTED_LANGUAGES.map((name) => ({
                name,
                due_count: 0,
                total_count: 0,
              }));
        const remainingActive = Math.max(0, dueCards.length - currentCardIndex);

        let html = `
        <button class="fc-lang-tab ${selectedFlashcardLang === "All" ? "active" : ""}" onclick="loadFlashcards('All')">
          <span>🌐</span> All Languages <span class="tab-badge">${selectedFlashcardLang === "All" && isReviewAllMode ? remainingActive : totalDue}</span>
        </button>
      `;

        displayLangs.forEach((l) => {
          const isSelected =
            selectedFlashcardLang.toLowerCase() === l.name.toLowerCase();
          const flag = LANG_EMOJIS[l.name] || "🌐";
          const badgeVal =
            isSelected && isReviewAllMode ? remainingActive : l.due_count || 0;
          html += `
          <button class="fc-lang-tab ${isSelected ? "active" : ""}" onclick="loadFlashcards('${l.name}')">
            <span>${flag}</span> ${l.name} <span class="tab-badge">${badgeVal}</span>
          </button>
        `;
        });

        tabsContainer.innerHTML = html;
      }

      function renderCurrentCard() {
        const activeDiv = document.getElementById("flashcard-active");
        const emptyDiv = document.getElementById("flashcard-empty");

        if (dueCards.length === 0 || currentCardIndex >= dueCards.length) {
          activeDiv.style.display = "none";
          emptyDiv.style.display = "block";
          const emptyDesc = document.getElementById("fc-empty-desc");
          if (emptyDesc) {
            const lText =
              selectedFlashcardLang === "All"
                ? "all languages"
                : selectedFlashcardLang;
            emptyDesc.textContent = `You have completed all scheduled reviews for ${lText}! Come back later or start a new scenario.`;
          }
          return;
        }

        activeDiv.style.display = "block";
        emptyDiv.style.display = "none";

        const progEl = document.getElementById("fc-progress-text");
        if (progEl) {
          progEl.textContent = `Card ${currentCardIndex + 1} of ${dueCards.length} ${isReviewAllMode ? "· (Review All Mode)" : ""}`;
        }

        const card = dueCards[currentCardIndex];
        const langFlag = LANG_EMOJIS[card.language] || "🌐";
        const langText = `${langFlag} ${card.language || "English"}`;

        const langBadge = document.getElementById("fc-lang-badge");
        if (langBadge) langBadge.textContent = langText;

        document.getElementById("fc-word").textContent = card.word;
        document.getElementById("fc-example").textContent = card.example
          ? `"${card.example}"`
          : "";
        document.getElementById("fc-translation").textContent =
          card.translation;

        // Reset state
        document.getElementById("fc-inner").classList.remove("flipped");
        document.getElementById("fc-buttons").style.display = "none";
      }

      function flipCard() {
        const inner = document.getElementById("fc-inner");
        if (!inner.classList.contains("flipped")) {
          inner.classList.add("flipped");
          document.getElementById("fc-buttons").style.display = "flex";
        }
      }

      async function reviewCard(quality) {
        if (currentCardIndex >= dueCards.length) return;
        const card = dueCards[currentCardIndex];

        // Optimistically decrement due count in availableFlashcardLangs
        const langStat = (availableFlashcardLangs || []).find(
          (l) =>
            l.language.toLowerCase() ===
            (card.language || "English").toLowerCase(),
        );
        if (langStat && langStat.due_count > 0 && !isReviewAllMode) {
          langStat.due_count--;
        }

        // Optimistically move to next card
        currentCardIndex++;
        renderFlashcardLanguageTabs();
        renderCurrentCard();

        // Send review in background
        try {
          const uid = currentUserId || (currentUser ? currentUser.id : "");
          await apiFetch(
            `/api/flashcards/${card.id}/review/?user_id=${encodeURIComponent(uid)}`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              credentials: "include",
              body: JSON.stringify({ quality: quality }),
            },
          );
        } catch (e) {
          console.error("Failed to review card", e);
        }
      }

      // ── DEDICATED FREE TALK STUDIO CONTROLLER ─────────────────────
      let currentFreeTalkSessionId = null;
      let currentFreeTalkPersona = "friendly";
      let freeTalkMediaRecorder = null;
      let freeTalkAudioChunks = [];
      let isFreeTalkRecording = false;
      let freeTalkVisualizerAnimationId = null;

      const FREE_TALK_STARTERS_DB = {
        English: [
          { icon: "☕", text: "Tell me about your day so far!" },
          { icon: "✈️", text: "If you could travel anywhere right now, where would you go?" },
          { icon: "🎬", text: "What's a movie or book you recently enjoyed?" },
          { icon: "💡", text: "What do you think about AI and the future of technology?" },
          { icon: "🎲", text: "Ask me a thought-provoking, interesting question!" },
          { icon: "🍕", text: "What is your comfort food and why do you love it?" },
          { icon: "🎵", text: "What kind of music puts you in the best mood?" },
          { icon: "🌍", text: "What is the most interesting cultural habit you've seen?" }
        ],
        French: [
          { icon: "☕", text: "Raconte-moi ta journée !" },
          { icon: "✈️", text: "Si tu pouvais voyager n'importe où, où irais-tu ?" },
          { icon: "🎬", text: "Quel est ton film ou livre préféré récemment ?" },
          { icon: "💡", text: "Que penses-tu de l'intelligence artificielle ?" },
          { icon: "🎲", text: "Pose-moi une question surprise et intéressante !" },
          { icon: "🥐", text: "Quel est ton plat ou dessert préféré ?" },
          { icon: "🎵", text: "Quel genre de musique écoutes-tu en ce moment ?" }
        ],
        Spanish: [
          { icon: "☕", text: "¡Cuéntame cómo ha ido tu día!" },
          { icon: "✈️", text: "¿Si pudieras viajar a cualquier lugar, a dónde irías?" },
          { icon: "🎬", text: "¿Cuál es tu película o libro favorito recientemente?" },
          { icon: "💡", text: "¿Qué opinas sobre el futuro de la tecnología?" },
          { icon: "🎲", text: "¡Hazme una pregunta interesante y aleatoria!" },
          { icon: "🌮", text: "¿Cuál es tu comida favorita para relajarte?" }
        ],
        German: [
          { icon: "☕", text: "Erzähl mir von deinem Tag!" },
          { icon: "✈️", text: "Wohin würdest du reisen, wenn du könntest?" },
          { icon: "🎬", text: "Was ist dein Lieblingsfilm oder Buch?" },
          { icon: "💡", text: "Was denkst du über Künstliche Intelligenz?" },
          { icon: "🎲", text: "Stell mir eine überraschende, spannende Frage!" }
        ],
        Japanese: [
          { icon: "☕", text: "今日の一日について教えて！" },
          { icon: "✈️", text: "今すぐどこへでも旅行できるなら、どこに行きたい？" },
          { icon: "🎬", text: "最近面白かった映画や本はある？" },
          { icon: "💡", text: "AIや未来のテクノロジーについてどう思う？" },
          { icon: "🎲", text: "何か面白い質問をしてみて！" },
          { icon: "🍜", text: "好きな日本食や料理は何ですか？" }
        ],
        Chinese: [
          { icon: "☕", text: "跟我聊聊你今天过得怎么样吧！" },
          { icon: "✈️", text: "如果你能去任何地方旅行，你想去哪里？" },
          { icon: "🎬", text: "你最近看过什么好看的电影或书吗？" },
          { icon: "💡", text: "你对人工智能和未来科技有什么看法？" },
          { icon: "🎲", text: "问我一个随机有趣的问题吧！" }
        ],
        Korean: [
          { icon: "☕", text: "오늘 하루 어땠는지 이야기해 줘!" },
          { icon: "✈️", text: "어디로든 여행 갈 수 있다면 어디로 가고 싶어?" },
          { icon: "🎬", text: "최근에 재미있게 본 영화나 책 있어?" },
          { icon: "💡", text: "AI와 미래 기술에 대해 어떻게 생각해?" },
          { icon: "🎲", text: "나에게 재미있고 신선한 질문 하나 해줘!" }
        ],
        Vietnamese: [
          { icon: "☕", text: "Hôm nay của bạn thế nào rồi, kể mình nghe với!" },
          { icon: "✈️", text: "Nếu được đi du lịch bất cứ đâu ngay bây giờ, bạn sẽ đi đâu?" },
          { icon: "🎬", text: "Bộ phim hay cuốn sách bạn thích nhất gần đây là gì?" },
          { icon: "💡", text: "Bạn nghĩ gì về tương lai của công nghệ và AI?" },
          { icon: "🎲", text: "Hãy hỏi mình một câu hỏi ngẫu nhiên và thú vị nhé!" },
          { icon: "🍜", text: "Món ăn yêu thích nhất của bạn là gì và vì sao?" }
        ]
      };

      async function initFreeTalkPage() {
        const targetLang = (currentUser && currentUser.target_language) || "English";
        const langBadge = document.getElementById("ft-lang-badge");
        if (langBadge) {
          const langEmojis = {
            English: "🇬🇧 English",
            French: "🇫🇷 French",
            Spanish: "🇪🇸 Spanish",
            German: "🇩🇪 German",
            Japanese: "🇯🇵 Japanese",
            Chinese: "🇨🇳 Chinese",
            Korean: "🇰🇷 Korean",
            Vietnamese: "🇻🇳 Vietnamese",
          };
          langBadge.textContent = langEmojis[targetLang] || targetLang;
        }

        // Update Turn Counter
        updateFreeTalkTurnUI();

        // Render Starters
        renderFreeTalkStarters();

        // Start session if none exists
        if (!currentFreeTalkSessionId) {
          await resetFreeTalkSession();
        }
      }

      function updateFreeTalkTurnUI() {
        updateDailyTurnUI();
      }

      window.setFreeTalkPersona = function (persona) {
        currentFreeTalkPersona = persona;
        document.querySelectorAll(".persona-pill").forEach(p => p.classList.remove("active"));
        const btn = document.getElementById(`p-${persona}`);
        if (btn) btn.classList.add("active");

        const personaLabels = {
          friendly: "Friendly Pal ☕",
          career: "Career Coach 💼",
          debate: "Debate Partner 🧠",
          strict: "Strict Professor 🎓"
        };
        const ml = document.getElementById("ft-msg-list");
        if (ml) {
          const sysNotice = document.createElement("div");
          sysNotice.style.cssText = "text-align:center;font-size:0.75rem;color:var(--muted-fg);margin:10px 0;font-style:italic;";
          sysNotice.innerHTML = `✨ Persona switched to <strong>${personaLabels[persona] || persona}</strong>`;
          ml.appendChild(sysNotice);
          ml.scrollTop = ml.scrollHeight;
        }
      };

      window.renderFreeTalkStarters = function () {
        const targetLang = (currentUser && currentUser.target_language) || "English";
        const pool = FREE_TALK_STARTERS_DB[targetLang] || FREE_TALK_STARTERS_DB["English"];
        const startersList = document.getElementById("ft-starters-list");
        if (!startersList) return;

        startersList.innerHTML = pool
          .slice(0, 5)
          .map(
            (st) =>
              `<button type="button" class="starter-chip" onclick="selectFreeTalkStarter('${st.text.replace(/'/g, "\\'")}')"><span>${st.icon}</span> ${st.text}</button>`
          )
          .join("");
      };

      window.refreshFreeTalkStarters = function () {
        const targetLang = (currentUser && currentUser.target_language) || "English";
        const pool = [...(FREE_TALK_STARTERS_DB[targetLang] || FREE_TALK_STARTERS_DB["English"])];
        // Shuffle
        for (let i = pool.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [pool[i], pool[j]] = [pool[j], pool[i]];
        }
        const startersList = document.getElementById("ft-starters-list");
        if (!startersList) return;

        startersList.innerHTML = pool
          .slice(0, 5)
          .map(
            (st) =>
              `<button type="button" class="starter-chip" onclick="selectFreeTalkStarter('${st.text.replace(/'/g, "\\'")}')"><span>${st.icon}</span> ${st.text}</button>`
          )
          .join("");
      };

      window.selectFreeTalkStarter = function (text) {
        const input = document.getElementById("ft-text-input");
        if (input) input.value = text;
        submitFreeTalkText(text);
      };

      window.resetFreeTalkSession = async function () {
        const targetLang = (currentUser && currentUser.target_language) || "English";
        const greetings = {
          English: "Hey there! 😊 Welcome to Free Talk! What's on your mind today? We can chat about anything!",
          French: "Bonjour ! 😊 Bienvenue dans le studio Free Talk ! De quoi aimerais-tu discuter aujourd'hui ?",
          Spanish: "¡Hola! 😊 ¡Bienvenido al estudio de Free Talk! ¿De qué te gustaría hablar hoy?",
          German: "Hallo! 😊 Willkommen im Free Talk Studio! Worüber möchtest du heute sprechen?",
          Japanese: "こんにちは！😊 フリートークスタジオへようこそ！今日はどんなことについて話したいですか？",
          Chinese: "你好！😊 欢迎来到自由对话室！今天你想聊些什么呢？",
          Korean: "안녕하세요! 😊 자유 대화 스튜디오에 오신 것을 환영합니다! 오늘 어떤 이야기를 나눌까요?",
          Vietnamese: "Chào bạn! 😊 Chào mừng đến với Free Talk Studio! Hôm nay bạn muốn cùng mình tâm sự hay bàn luận chủ đề gì nào?",
        };
        const initialGreeting = greetings[targetLang] || greetings["English"];
        const initVoiceId = "ft-voice-init-" + Date.now();
        const initVoicePill = createAiVoicePillHtml("", initVoiceId, initialGreeting, targetLang);

        const ml = document.getElementById("ft-msg-list");
        if (ml) {
          ml.innerHTML = `
            <div class="msg-wrap">
              <div class="msg-lbl">🤖 LinguistAI (${targetLang})</div>
              <div class="msg-bubble msg-ai">${initialGreeting}</div>
              <div>${initVoicePill}</div>
            </div>`;
          ml.scrollTop = ml.scrollHeight;
        }

        fetch(`/api/tts/?text=${encodeURIComponent(initialGreeting)}&lang=${encodeURIComponent(targetLang)}`)
          .then((r) => r.json())
          .then((d) => {
            if (d && d.audio_url) {
              const p = document.getElementById(`pill-${initVoiceId}`);
              if (p) p.setAttribute("data-url", d.audio_url);
            }
          })
          .catch(() => {});

        // Reset feedback & vocab
        const fbList = document.getElementById("ft-fb-list");
        if (fbList) {
          fbList.innerHTML = `<div class="fb-item" style="color:var(--muted-fg)"><span style="flex-shrink:0">🎙️</span><span>Speak or type freely. Real-time feedback, grammar notes, and scores will appear here!</span></div>`;
        }
        const vList = document.getElementById("ft-vocab-list");
        if (vList) {
          vList.innerHTML = `<div style="color:var(--muted-fg);font-size:0.8rem;text-align:center;padding:12px;">Vocabulary extracted during your chat will be saved here.</div>`;
        }

        // Start backend session using Free Talk Scenario (ID 27 or title match)
        try {
          const activeUid = (currentUser && currentUser.id) || currentUserId || localStorage.getItem("linguist_user_id");
          const freeTalkScenario = SCENARIOS.find(s => s.category === "Open Talk" || (s.title || "").toLowerCase().includes("free talk")) || { id: 27 };
          const res = await apiFetch("/api/sessions/start/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ user_id: activeUid, scenario_id: freeTalkScenario.id }),
          });
          if (res.ok) {
            const data = await res.json();
            currentFreeTalkSessionId = data.session_id;
          }
        } catch (e) {
          console.warn("Could not create Free Talk session:", e);
        }
      };

      window.handleFreeTalkTextSubmit = function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          submitFreeTalkText();
        }
      };

      window.submitFreeTalkText = async function (explicitText) {
        const input = document.getElementById("ft-text-input");
        const text = (explicitText !== undefined ? explicitText : (input ? input.value : "")).trim();
        if (!text) return;
        if (input) input.value = "";

        const plan = (currentUser && (currentUser.subscription_plan || "")).toUpperCase();
        const role = (currentUser && (currentUser.role || "")).toUpperCase();
        const isVip =
          plan === "VIP" ||
          plan === "PRO" ||
          role === "ADMIN" ||
          (currentUser && currentUser.daily_limit === null) ||
          (currentUser && currentUser.is_vip);

        // Check Turn Limit for non-VIP
        if (!isVip && userDailyLimit !== null && userTodayTurns >= userDailyLimit) {
          openPaymentModal();
          return;
        }

        const ml = document.getElementById("ft-msg-list");
        if (ml) {
          ml.innerHTML += `
            <div class="msg-wrap msg-user-wrap">
              <div class="msg-lbl">👤 You</div>
              <div class="msg-bubble msg-user">${text}</div>
            </div>`;
          ml.scrollTop = ml.scrollHeight;
        }

        const targetLang = (currentUser && currentUser.target_language) || "English";
        const placeholderVoiceId = "ft-voice-" + Date.now();
        const placeholderPill = createAiVoicePillHtml("", placeholderVoiceId, "", targetLang);
        if (ml) {
          ml.innerHTML += `
            <div class="msg-wrap" id="ft-ai-loading-wrap">
              <div class="msg-lbl">🤖 LinguistAI</div>
              <div class="msg-bubble msg-ai" id="ft-ai-thinking" style="color:var(--muted-fg);font-style:italic"><i class="bi bi-hourglass-split"></i> Thinking...</div>
              <div id="ft-ai-voice-wrap">${placeholderPill}</div>
            </div>`;
          ml.scrollTop = ml.scrollHeight;
        }

        try {
          const activeUid = (currentUser && currentUser.id) || currentUserId || localStorage.getItem("linguist_user_id");
          const res = await apiFetch(`/api/sessions/${currentFreeTalkSessionId || 1}/respond/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
              user_id: activeUid,
              user_transcript: text,
              transcript: text,
              persona: currentFreeTalkPersona,
            }),
          });

          if (res.ok) {
            const data = await res.json();
            const thinkingEl = document.getElementById("ft-ai-thinking");
            if (thinkingEl) {
              thinkingEl.style.color = "";
              thinkingEl.style.fontStyle = "";
              thinkingEl.textContent = data.ai_response || "...";
            }
            const pillEl = document.getElementById(`pill-${placeholderVoiceId}`);
            if (pillEl) {
              pillEl.setAttribute("data-text", encodeURIComponent(data.ai_response || ""));
              if (data.ai_audio_url) {
                pillEl.setAttribute("data-url", data.ai_audio_url);
              }
            }
            if (data.turns_today !== undefined) {
              updateDailyTurnUI(data.turns_today, data.daily_limit);
            }
            renderFreeTalkFeedback(data.feedback, data.scores);
          } else if (res.status === 403) {
            const errData = await res.json().catch(() => ({}));
            if (errData.limit_reached) {
              const thinkingEl = document.getElementById("ft-ai-thinking");
              if (thinkingEl) thinkingEl.textContent = "You have used all daily turns. Please upgrade to VIP for unlimited practice!";
              openPaymentModal();
            }
          }
        } catch (e) {
          console.error("Free talk submission error:", e);
        }
      };

      function renderFreeTalkFeedback(feedback, scores) {
        const fbList = document.getElementById("ft-fb-list");
        if (!fbList || !feedback) return;

        const grammarScore = scores && scores.grammar !== undefined ? scores.grammar : 85;
        const pronScore = scores && scores.pronunciation !== undefined ? scores.pronunciation : 88;

        let html = `
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
            <div style="background:#f8fafc;border:1px solid var(--border);border-radius:10px;padding:8px;text-align:center;">
              <div style="font-size:1.1rem;font-weight:800;color:var(--primary);">${grammarScore}%</div>
              <div style="font-size:0.68rem;color:var(--muted-fg);font-weight:600;">GRAMMAR</div>
            </div>
            <div style="background:#f8fafc;border:1px solid var(--border);border-radius:10px;padding:8px;text-align:center;">
              <div style="font-size:1.1rem;font-weight:800;color:#10b981;">${pronScore}%</div>
              <div style="font-size:0.68rem;color:var(--muted-fg);font-weight:600;">FLUENCY</div>
            </div>
          </div>`;

        if (feedback.grammar_correction && feedback.grammar_correction !== "No errors detected.") {
          html += `<div class="fb-item" style="border-left:3px solid #ef4444;"><span style="flex-shrink:0">✏️</span><span>${feedback.grammar_correction}</span></div>`;
        }
        if (feedback.pronunciation_tip) {
          html += `<div class="fb-item" style="border-left:3px solid #3b82f6;"><span style="flex-shrink:0">🔊</span><span>${feedback.pronunciation_tip}</span></div>`;
        }
        if (feedback.better_alternative) {
          html += `<div class="fb-item" style="border-left:3px solid #8b5cf6;"><span style="flex-shrink:0">💡</span><span>${feedback.better_alternative}</span></div>`;
        }
        fbList.innerHTML = html;

        // Populate vocabulary if returned
        if (feedback.extracted_vocab && Array.isArray(feedback.extracted_vocab) && feedback.extracted_vocab.length > 0) {
          const vList = document.getElementById("ft-vocab-list");
          if (vList) {
            vList.innerHTML = feedback.extracted_vocab
              .map(v => `
                <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border)">
                  <span style="font-weight:600;color:var(--primary)">${v.word || v.w}</span>
                  <span style="color:var(--muted-fg)">${v.def || v.d}</span>
                </div>`)
              .join("");
          }
        }
      }

      window.toggleFreeTalkMic = async function () {
        const micBtn = document.getElementById("ft-mic-btn");
        const micIcon = document.getElementById("ft-mic-icon");
        const micStatus = document.getElementById("ft-mic-status");

        if (isFreeTalkRecording) {
          // Stop recording
          isFreeTalkRecording = false;
          if (micBtn) micBtn.classList.remove("recording");
          if (micIcon) micIcon.className = "bi bi-mic-fill";
          if (micStatus) micStatus.textContent = "Processing your voice with Whisper AI...";
          stopFreeTalkAudioVisualizer();
          if (freeTalkMediaRecorder && freeTalkMediaRecorder.state !== "inactive") {
            freeTalkMediaRecorder.stop();
          }
          return;
        }

        // Start recording
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          freeTalkAudioChunks = [];
          freeTalkMediaRecorder = new MediaRecorder(stream);
          freeTalkMediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) freeTalkAudioChunks.push(e.data);
          };
          freeTalkMediaRecorder.onstop = async () => {
            stream.getTracks().forEach((track) => track.stop());
            const audioBlob = new Blob(freeTalkAudioChunks, { type: "audio/webm" });
            await submitFreeTalkAudio(audioBlob);
          };

          freeTalkMediaRecorder.start();
          isFreeTalkRecording = true;
          if (micBtn) micBtn.classList.add("recording");
          if (micIcon) micIcon.className = "bi bi-stop-fill";
          if (micStatus) micStatus.textContent = "Listening... Speak freely in your target language!";
          startFreeTalkAudioVisualizer(stream);
        } catch (err) {
          console.warn("Microphone access failed for Free Talk:", err);
          if (micStatus) micStatus.textContent = "Microphone permission denied. Type below instead.";
        }
      };

      async function submitFreeTalkAudio(audioBlob) {
        const micStatus = document.getElementById("ft-mic-status");
        if (micStatus) micStatus.textContent = "Transcribing & evaluating voice...";

        const formData = new FormData();
        const activeUid = (currentUser && currentUser.id) || currentUserId || localStorage.getItem("linguist_user_id");
        formData.append("user_id", activeUid);
        formData.append("audio_file", audioBlob, "freetalk_voice.webm");
        formData.append("persona", currentFreeTalkPersona);

        try {
          const res = await apiFetch(`/api/sessions/${currentFreeTalkSessionId || 1}/respond-audio/`, {
            method: "POST",
            credentials: "include",
            body: formData,
          });

          if (res.ok) {
            const data = await res.json();
            if (micStatus) micStatus.textContent = "Press the mic to start speaking freely";

            const ml = document.getElementById("ft-msg-list");
            const targetLang = (currentUser && currentUser.target_language) || "English";
            const voiceId = "ft-voice-" + Date.now();
            const voicePill = createAiVoicePillHtml(data.ai_audio_url || "", voiceId, data.ai_response || "", targetLang);

            if (ml) {
              ml.innerHTML += `
                <div class="msg-wrap msg-user-wrap">
                  <div class="msg-lbl">👤 You (Voice)</div>
                  <div class="msg-bubble msg-user">${data.user_transcript || "..."}</div>
                </div>
                <div class="msg-wrap">
                  <div class="msg-lbl">🤖 LinguistAI</div>
                  <div class="msg-bubble msg-ai">${data.ai_response || "..."}</div>
                  <div>${voicePill}</div>
                </div>`;
              ml.scrollTop = ml.scrollHeight;
            }

            if (data.turns_today !== undefined) {
              updateDailyTurnUI(data.turns_today, data.daily_limit);
            }
            renderFreeTalkFeedback(data.feedback, data.scores);
          } else if (res.status === 403) {
            if (micStatus) micStatus.textContent = "Daily turns limit reached!";
            openPaymentModal();
          } else {
            if (micStatus) micStatus.textContent = "Error processing audio. Please try again.";
          }
        } catch (e) {
          console.error("Free Talk audio upload failed:", e);
          if (micStatus) micStatus.textContent = "Failed to upload audio. Check your connection.";
        }
      }

      function startFreeTalkAudioVisualizer(stream) {
        const canvas = document.getElementById("ft-audio-visualizer-canvas");
        const wrap = document.getElementById("ft-audio-visualizer-wrap");
        if (!canvas || !wrap) return;
        wrap.classList.add("active");

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioCtx.createAnalyser();
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        analyser.fftSize = 64;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        const canvasCtx = canvas.getContext("2d");

        function draw() {
          if (!isFreeTalkRecording) return;
          freeTalkVisualizerAnimationId = requestAnimationFrame(draw);
          analyser.getByteFrequencyData(dataArray);

          canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
          const barWidth = (canvas.width / bufferLength) * 1.5;
          let barHeight;
          let x = 0;

          for (let i = 0; i < bufferLength; i++) {
            barHeight = (dataArray[i] / 255) * canvas.height;
            canvasCtx.fillStyle = "#8b5cf6";
            canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
            x += barWidth + 2;
          }
        }
        draw();
      }

      function stopFreeTalkAudioVisualizer() {
        const wrap = document.getElementById("ft-audio-visualizer-wrap");
        if (wrap) wrap.classList.remove("active");
        if (freeTalkVisualizerAnimationId) {
          cancelAnimationFrame(freeTalkVisualizerAnimationId);
          freeTalkVisualizerAnimationId = null;
        }
      }

