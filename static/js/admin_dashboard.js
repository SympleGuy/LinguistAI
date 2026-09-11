let currentSection = 'overview';
let currentDays = 14;
let timelineChart = null;
let cefrChart = null;
let languageChart = null;
let userSearchTimeout = null;

// Scenario Studio & Free Talk state
let allLoadedScenarios = [];
let activeScenarioLang = 'all';
let scenarioSearchQuery = '';
let freeTalkScenarioObj = null;

function escapeHTML(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  updateClock();
  setInterval(updateClock, 1000);

  // Check URL hash routing
  const hash = window.location.hash.replace('#', '');
  if (hash && ['overview', 'users', 'scenarios', 'freetalk', 'sessions', 'flashcards', 'maintenance'].includes(hash)) {
    currentSection = hash;
  }

          // Check if already authenticated
          const gate = document.getElementById('adminLoginGate');
          if (gate && gate.style.display !== 'none') {
            // Unauthenticated -> wait for gate login
            return;
          }

          initAdminDashboard();
        });

        function initAdminDashboard() {
          // 1. SWR Immediate Cache Render (0ms latency!)
          applySwrMetricsCache();
          applySwrAnalyticsCache();

          // 2. Switch to active section
          switchSection(currentSection, false);

          // 3. Background fresh parallel fetch
          Promise.all([
            loadMetrics(),
            loadAnalyticsData(currentDays)
          ]).catch(e => console.error("Initial load error:", e));
        }

        // Theme Management
        function initTheme() {
          const savedTheme = localStorage.getItem('linguist_admin_theme') || 'dark';
          document.documentElement.setAttribute('data-theme', savedTheme);
          updateThemeIcon(savedTheme);
        }

        function toggleTheme() {
          const current = document.documentElement.getAttribute('data-theme') || 'dark';
          const next = current === 'dark' ? 'light' : 'dark';
          document.documentElement.setAttribute('data-theme', next);
          localStorage.setItem('linguist_admin_theme', next);
          updateThemeIcon(next);
          if (timelineChart) loadAnalyticsData(currentDays);
        }

        function updateThemeIcon(theme) {
          const icon = document.getElementById('themeIcon');
          if (!icon) return;
          icon.className = theme === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars text-primary';
        }

        function toggleSidebar() {
          document.getElementById('adminSidebar').classList.toggle('open');
          document.getElementById('sidebarBackdrop').classList.toggle('active');
        }

        function updateClock() {
          const now = new Date();
          const clockEl = document.getElementById('liveClock');
          if (clockEl) {
            clockEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' • ' + now.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
          }
        }

        // Modal helpers with Bootstrap 5 getOrCreateInstance
        function showModal(modalId) {
          const el = document.getElementById(modalId);
          if (!el) return;
          const modal = bootstrap.Modal.getOrCreateInstance(el);
          modal.show();
        }

        function hideModal(modalId) {
          const el = document.getElementById(modalId);
          if (!el) return;
          const modal = bootstrap.Modal.getOrCreateInstance(el);
          modal.hide();
        }

        // Toast Notification System
        function showToast(message, type = 'info') {
          const container = document.getElementById('adminToastContainer');
          const toast = document.createElement('div');
          toast.className = 'admin-toast';

          const iconMap = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-exclamation-triangle-fill text-danger',
            info: 'bi-info-circle-fill text-primary'
          };

          toast.innerHTML = `
        <i class="bi ${iconMap[type] || iconMap.info} fs-5"></i>
        <div style="font-size: 0.88rem; font-weight: 500;">${message}</div>
      `;

          container.appendChild(toast);
          setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.25s ease';
            setTimeout(() => toast.remove(), 250);
          }, 3500);
        }

        // ─────────────────────────────────────────────────────────────────
        // AUTHENTICATION & GATE CONTROLLERS
        // ─────────────────────────────────────────────────────────────────
        async function handleAdminLogin(event) {
          event.preventDefault();
          const email = document.getElementById('gateEmail').value.trim();
          const password = document.getElementById('gatePassword').value;
          const alertBox = document.getElementById('gateAlert');
          const btn = document.getElementById('btnGateSubmit');

          alertBox.classList.add('d-none');
          btn.disabled = true;
          btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Authenticating...';

          try {
            const res = await fetch('/api/admin/auth/login/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ email, password })
            });

            const data = await res.json();
            if (!res.ok) {
              alertBox.textContent = data.error || 'Authentication failed.';
              alertBox.classList.remove('d-none');
              btn.disabled = false;
              btn.innerHTML = '<i class="bi bi-box-arrow-in-right me-1"></i>Authenticate & Enter';
              return;
            }

            // Login success -> unlock interface smoothly
            document.getElementById('adminLoginGate').style.display = 'none';
            const appContainer = document.getElementById('adminAppContainer');
            appContainer.style.display = 'flex';
            appContainer.style.animation = 'fadeInView 0.3s ease';

            showToast('Welcome Administrator! Master Control Unlocked.', 'success');
            initAdminDashboard();
          } catch (err) {
            alertBox.textContent = 'Connection error: ' + err.message;
            alertBox.classList.remove('d-none');
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-box-arrow-in-right me-1"></i>Authenticate & Enter';
          }
        }

        async function handleAdminLogout() {
          if (!confirm("Are you sure you want to terminate this Admin session?")) return;
          try {
            await fetch('/api/admin/auth/logout/', { method: 'POST' });
            localStorage.removeItem('linguist_admin_metrics');
            localStorage.removeItem('linguist_admin_analytics');
            window.location.reload();
          } catch (e) {
            window.location.reload();
          }
        }

        // Section Navigation & URL Hash
        function switchSection(sectionId, updateHash = true) {
          currentSection = sectionId;
          if (updateHash) {
            window.location.hash = '#' + sectionId;
          }

          document.querySelectorAll('.admin-nav-item').forEach(el => el.classList.remove('active'));
          document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));

          const activeSection = document.getElementById(`section-${sectionId}`);
          if (activeSection) activeSection.classList.add('active');

          const navItems = document.querySelectorAll('.admin-nav-item');
          navItems.forEach(item => {
            if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(`'${sectionId}'`)) {
              item.classList.add('active');
            }
          });

          // Auto-close sidebar on mobile/tablet after navigating
          if (window.innerWidth < 992) {
            const sidebar = document.getElementById('adminSidebar');
            const backdrop = document.getElementById('sidebarBackdrop');
            if (sidebar && sidebar.classList.contains('open')) {
              sidebar.classList.remove('open');
              if (backdrop) backdrop.classList.remove('active');
            }
          }

          const titles = {
            overview: 'Platform Overview & Telemetry',
            users: 'Learners & User Management',
            scenarios: 'Scenario Studio & Roleplay Catalog',
            freetalk: 'Free Talk AI Studio & Personas',
            sessions: 'Session Replays & Feedback Inspector',
            flashcards: 'Flashcards & Spaced Repetition (SM-2)',
            maintenance: 'Storage & Data Management'
          };
          document.getElementById('currentSectionTitle').textContent = titles[sectionId] || 'Admin Portal';

          if (sectionId === 'users') loadUsersData(1);
          if (sectionId === 'scenarios') loadScenariosData();
          if (sectionId === 'freetalk') loadFreeTalkData();
          if (sectionId === 'sessions') loadSessionsData(1);
          if (sectionId === 'flashcards') loadFlashcardsData();
          if (sectionId === 'maintenance') loadMaintenanceData();
        }

        function refreshCurrentSection() {
          const icon = document.getElementById('refreshIcon');
          if (icon) icon.classList.add('spin');
          loadMetrics();
          switchSection(currentSection, false);
          setTimeout(() => {
            if (icon) icon.classList.remove('spin');
            showToast('Telemetry refreshed successfully', 'success');
          }, 400);
        }

        // ─────────────────────────────────────────────────────────────────
        // 1. SWR ZERO-LATENCY METRICS & OVERVIEW
        // ─────────────────────────────────────────────────────────────────
        function applySwrMetricsCache() {
          try {
            const cached = localStorage.getItem('linguist_admin_metrics');
            if (!cached) return;
            const data = JSON.parse(cached);
            renderMetricsUI(data);
          } catch (e) { }
        }

        function applySwrAnalyticsCache() {
          try {
            const cached = localStorage.getItem('linguist_admin_analytics');
            if (!cached) return;
            const data = JSON.parse(cached);
            if (data.timeline) renderTimelineChart(data.timeline);
            if (data.cefr_distribution) renderCefrChart(data.cefr_distribution);
            if (data.language_distribution) renderLanguageChart(data.language_distribution);
            if (data.scenario_stats) renderTopScenarios(data.scenario_stats);
          } catch (e) { }
        }

        function renderMetricsUI(data) {
          if (!data) return;
          document.getElementById('kpiTotalUsers').textContent = data.users.total;
          document.getElementById('kpiProCount').textContent = `${data.users.pro || 0} VIP`;
          document.getElementById('kpiFreeCount').textContent = `${data.users.free || 0} Free`;
          document.getElementById('kpiActiveToday').textContent = data.users.active_today;
          document.getElementById('kpiNew7d').textContent = `+${data.users.new_7d} new`;
          document.getElementById('kpiTotalSessions').textContent = data.activity.total_sessions;
          document.getElementById('kpiTotalTurns').textContent = `${data.activity.total_turns} turns`;
          document.getElementById('kpiAvgScore').textContent = `${data.activity.avg_score}%`;
          document.getElementById('kpiGrammarAvg').textContent = data.activity.avg_grammar;
          document.getElementById('kpiPronAvg').textContent = data.activity.avg_pronunciation;

          document.getElementById('navUserBadge').textContent = data.users.total;
          if (allLoadedScenarios.length > 0) {
            updateScenarioBadges();
          } else {
            const totalScenarios = data.scenarios_count || 0;
            document.getElementById('navScenarioBadge').textContent = Math.max(0, totalScenarios - 1);
          }

          if (data.storage) {
            document.getElementById('maintAudioFilesCount').textContent = data.storage.audio_files_count;
            document.getElementById('maintAudioMb').textContent = data.storage.audio_mb;
            document.getElementById('maintMediaPath').textContent = data.storage.media_path;
          }

          if (data.ai_status) {
            const llmLabel = document.getElementById('aiLlmLabel');
            if (llmLabel) llmLabel.textContent = data.ai_status.llm_engine;
            const ttsLabel = document.getElementById('aiTtsLabel');
            if (ttsLabel) ttsLabel.textContent = data.ai_status.tts_engine;
          }
        }

        async function loadMetrics() {
          try {
            const res = await fetch('/api/admin/metrics/');
            if (res.status === 401) {
              document.getElementById('adminLoginGate').style.display = 'flex';
              document.getElementById('adminAppContainer').style.display = 'none';
              return;
            }
            if (!res.ok) return;
            const data = await res.json();
            renderMetricsUI(data);
            localStorage.setItem('linguist_admin_metrics', JSON.stringify(data));
          } catch (e) {
            console.error('Error loading metrics:', e);
          }
        }

        async function loadAnalyticsData(days = 14, btnEl = null) {
          currentDays = days;
          if (btnEl) {
            btnEl.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btnEl.classList.add('active');
          }

          try {
            const res = await fetch(`/api/admin/analytics/?days=${days}`);
            if (!res.ok) return;
            const data = await res.json();

            renderTimelineChart(data.timeline);
            renderCefrChart(data.cefr_distribution);
            renderLanguageChart(data.language_distribution);
            renderTopScenarios(data.scenario_stats);

            localStorage.setItem('linguist_admin_analytics', JSON.stringify(data));
          } catch (e) {
            console.error('Error loading analytics:', e);
          }
        }

        function renderTimelineChart(timeline) {
          const ctx = document.getElementById('timelineChart');
          if (!ctx) return;
          if (timelineChart) timelineChart.destroy();

          const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
          const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
          const textColor = isDark ? '#94A3B8' : '#64748B';

          timelineChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: timeline.labels,
              datasets: [
                {
                  label: 'Conversational Turns',
                  data: timeline.turns,
                  borderColor: '#6366F1',
                  backgroundColor: 'rgba(99, 102, 241, 0.12)',
                  fill: true,
                  tension: 0.35,
                  borderWidth: 2
                },
                {
                  label: 'Practice Sessions',
                  data: timeline.sessions,
                  borderColor: '#06B6D4',
                  backgroundColor: 'transparent',
                  borderWidth: 2,
                  tension: 0.35
                },
                {
                  label: 'New Learners',
                  data: timeline.users,
                  borderColor: '#10B981',
                  backgroundColor: 'transparent',
                  borderWidth: 2,
                  borderDash: [4, 4],
                  tension: 0.35
                }
              ]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { position: 'top', labels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } } },
                tooltip: { padding: 10, cornerRadius: 8 }
              },
              scales: {
                x: { grid: { color: gridColor }, ticks: { color: textColor } },
                y: { grid: { color: gridColor }, ticks: { color: textColor, precision: 0 } }
              }
            }
          });
        }

        function renderCefrChart(cefrData) {
          const ctx = document.getElementById('cefrChart');
          if (!ctx) return;
          if (cefrChart) cefrChart.destroy();

          const labels = Object.keys(cefrData);
          const values = Object.values(cefrData);

          cefrChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: labels.length ? labels : ['Beginner'],
              datasets: [{
                data: values.length ? values : [1],
                backgroundColor: ['#6366F1', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B', '#F43F5E', '#A855F7'],
                borderWidth: 0
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { position: 'bottom', labels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 10 } } }
              },
              cutout: '72%'
            }
          });
        }

        function renderLanguageChart(langData) {
          const ctx = document.getElementById('languageChart');
          if (!ctx) return;
          if (languageChart) languageChart.destroy();

          const labels = Object.keys(langData);
          const values = Object.values(langData);

          languageChart = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [{
                label: 'Learners',
                data: values,
                backgroundColor: '#8B5CF6',
                borderRadius: 6
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: false } },
              scales: {
                x: { grid: { display: false }, ticks: { color: '#64748B' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748B', precision: 0 } }
              }
            }
          });
        }

        function renderTopScenarios(scenarios) {
          const tbody = document.getElementById('topScenariosTableBody');
          if (!tbody) return;

          if (!scenarios || !scenarios.length) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center text-dim py-4">No scenario sessions yet</td></tr>';
            return;
          }

          tbody.innerHTML = scenarios.map(s => `
        <tr>
          <td><span class="fw-bold">${s.title}</span></td>
          <td><span class="badge bg-secondary text-white font-mono">${s.sessions_count}</span></td>
          <td><span class="status-badge ${s.avg_score >= 80 ? 'badge-vip' : 'badge-free'}">${s.avg_score}%</span></td>
        </tr>
      `).join('');
        }

        // ─────────────────────────────────────────────────────────────────
        // 2. LEARNERS & USERS CRUD
        // ─────────────────────────────────────────────────────────────────
        function debounceUserSearch() {
          clearTimeout(userSearchTimeout);
          userSearchTimeout = setTimeout(() => loadUsersData(1), 300);
        }

        function renderUsersTable(data) {
          const tbody = document.getElementById('usersTableBody');
          if (!tbody) return;
          if (!data.users || !data.users.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center text-dim py-5">No learners found matching filters</td></tr>';
            document.getElementById('userPaginationInfo').textContent = '0 users';
            document.getElementById('userPaginationButtons').innerHTML = '';
            return;
          }

          tbody.innerHTML = data.users.map(u => {
            const isVip = (u.subscription_plan || '').toUpperCase() === 'VIP';
            const turnBadge = isVip
              ? `<span class="status-badge badge-vip">Unlimited</span>`
              : `<span class="badge ${u.today_turns >= (u.daily_turn_limit || 5) ? 'bg-danger' : 'bg-secondary'} font-mono">${u.today_turns} / ${u.daily_turn_limit || 5}</span>`;

            const resetActionBtn = isVip
              ? ''
              : `<button class="btn btn-subtle p-1 px-2 text-warning" title="Reset Today's Turn Limit to 0" onclick="resetUserTurns('${u.id}', '${u.username}')">
               <i class="bi bi-arrow-counterclockwise"></i>
             </button>`;

            return `
        <tr>
          <td>
            <div class="d-flex align-items-center gap-2">
              <div class="rounded-circle bg-primary bg-opacity-25 text-primary d-flex align-items-center justify-content-center fw-bold" style="width: 34px; height: 34px; font-size: 0.82rem;">
                ${(u.username || 'U')[0].toUpperCase()}
              </div>
              <div>
                <div class="fw-bold">${u.username || 'Anonymous'}</div>
                <small class="text-dim font-mono" style="font-size: 0.75rem;">${u.email || u.id.slice(0, 8)}</small>
              </div>
            </div>
          </td>
          <td>
            <span class="status-badge ${u.role === 'admin' ? 'badge-admin' : 'badge-free'}">
              ${u.role === 'admin' ? 'ADMIN' : 'LEARNER'}
            </span>
          </td>
          <td><span class="status-badge badge-lang">${u.target_language}</span></td>
          <td><span class="status-badge badge-cefr">${u.proficiency_level}</span></td>
          <td><span class="status-badge ${isVip ? 'badge-vip' : 'badge-free'}">${u.subscription_plan || 'Free'}</span></td>
          <td><span class="fw-bold font-mono">${u.sessions_count}</span></td>
          <td>${turnBadge}</td>
          <td><small class="text-dim font-mono">${u.created_at ? new Date(u.created_at).toLocaleDateString() : '-'}</small></td>
          <td class="text-end">
            <div class="btn-group btn-group-sm">
              <button class="btn btn-subtle p-1 px-2" title="Edit Profile, Role, Plan & Limits" onclick='editUserModal(${JSON.stringify(u)})'>
                <i class="bi bi-pencil"></i>
              </button>
              ${resetActionBtn}
              <button class="btn btn-subtle p-1 px-2 text-danger" title="Delete User" onclick="deleteUser('${u.id}', '${u.username}')">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
          }).join('');

          document.getElementById('userPaginationInfo').textContent = `Showing page ${data.page} of ${data.total_pages} (${data.total} total learners)`;
          renderPaginationButtons('userPaginationButtons', data.page, data.total_pages, loadUsersData);
        }

        async function loadUsersData(page = 1) {
          const q = document.getElementById('userSearchInput').value.trim();
          const plan = document.getElementById('userPlanFilter').value;
          const role = document.getElementById('userRoleFilter').value;
          const lang = document.getElementById('userLangFilter').value;

          const isDefaultFilter = (page === 1 && !q && plan === 'all' && role === 'all' && lang === 'all');

          // 1. SWR Instant render from localStorage
          if (isDefaultFilter) {
            try {
              const cached = localStorage.getItem('linguist_admin_users_p1');
              if (cached) {
                const parsed = JSON.parse(cached);
                renderUsersTable(parsed);
              }
            } catch (e) { }
          }

          // 2. Fresh Background Fetch
          try {
            const res = await fetch(`/api/admin/users/?page=${page}&q=${encodeURIComponent(q)}&plan=${plan}&role=${role}&lang=${lang}`);
            if (!res.ok) return;
            const data = await res.json();

            renderUsersTable(data);

            if (isDefaultFilter) {
              localStorage.setItem('linguist_admin_users_p1', JSON.stringify(data));
            }
          } catch (e) {
            console.error('Error loading users:', e);
          }
        }

        function togglePlanLimitField() {
          const plan = document.getElementById('userFormPlan').value;
          const isVip = plan === 'VIP';
          const limitFields = document.getElementById('userFormLimitFields');
          const vipBanner = document.getElementById('userFormVipBanner');

          if (isVip) {
            if (limitFields) limitFields.classList.add('d-none');
            if (vipBanner) vipBanner.classList.remove('d-none');
          } else {
            if (limitFields) limitFields.classList.remove('d-none');
            if (vipBanner) vipBanner.classList.add('d-none');
            const limitInput = document.getElementById('userFormDailyLimit');
            if (limitInput && !limitInput.value) limitInput.value = 5;
          }
        }

        function renderPaginationButtons(containerId, currentPage, totalPages, callback) {
          const container = document.getElementById(containerId);
          if (!container) return;
          let html = '';
          if (currentPage > 1) {
            html += `<button class="btn btn-subtle" onclick="${callback.name}(${currentPage - 1})"><i class="bi bi-chevron-left"></i></button>`;
          }
          for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
            html += `<button class="btn btn-subtle ${i === currentPage ? 'active' : ''}" onclick="${callback.name}(${i})">${i}</button>`;
          }
          if (currentPage < totalPages) {
            html += `<button class="btn btn-subtle" onclick="${callback.name}(${currentPage + 1})"><i class="bi bi-chevron-right"></i></button>`;
          }
          container.innerHTML = html;
        }

        function openNewUserModal() {
          document.getElementById('userModalTitle').textContent = 'Add New Learner';
          document.getElementById('userFormId').value = '';
          document.getElementById('userFormUsername').value = '';
          document.getElementById('userFormEmail').value = '';
          document.getElementById('userFormPassword').value = '';
          document.getElementById('pwdHint').textContent = '(default: 123456)';
          document.getElementById('userFormLang').value = 'English';
          document.getElementById('userFormLevel').value = 'Beginner';
          document.getElementById('userFormPlan').value = 'Free';
          document.getElementById('userFormRole').value = 'user';
          document.getElementById('userFormDailyLimit').value = 5;
          document.getElementById('userFormDailyLimit').disabled = false;
          document.getElementById('userFormTurnsUsed').value = 0;
          showModal('userModal');
        }

        function editUserModal(user) {
          document.getElementById('userModalTitle').textContent = `Edit Profile: ${user.username}`;
          document.getElementById('userFormId').value = user.id;
          document.getElementById('userFormUsername').value = user.username;
          document.getElementById('userFormEmail').value = user.email;
          document.getElementById('userFormPassword').value = '';
          document.getElementById('pwdHint').textContent = '(leave blank to keep unchanged)';
          document.getElementById('userFormLang').value = user.target_language;
          document.getElementById('userFormLevel').value = user.proficiency_level;
          document.getElementById('userFormPlan').value = user.subscription_plan || 'Free';
          document.getElementById('userFormRole').value = user.role || 'user';
          document.getElementById('userFormDailyLimit').value = user.daily_turn_limit !== null && user.daily_turn_limit !== undefined ? user.daily_turn_limit : 5;
          document.getElementById('userFormTurnsUsed').value = user.today_turns || 0;
          togglePlanLimitField();
          showModal('userModal');
        }

        async function saveUserForm() {
          const id = document.getElementById('userFormId').value;
          const username = document.getElementById('userFormUsername').value.trim();
          const email = document.getElementById('userFormEmail').value.trim();
          const password = document.getElementById('userFormPassword').value;
          const target_language = document.getElementById('userFormLang').value;
          const proficiency_level = document.getElementById('userFormLevel').value;
          const subscription_plan = document.getElementById('userFormPlan').value;
          const role = document.getElementById('userFormRole').value;
          const daily_turn_limit = subscription_plan === 'VIP' ? null : parseInt(document.getElementById('userFormDailyLimit').value) || 5;
          const daily_turns_used = parseInt(document.getElementById('userFormTurnsUsed').value) || 0;

          if (!username && !email) {
            showToast('Please enter a username or email', 'error');
            return;
          }

          const payload = {
            username,
            email,
            target_language,
            proficiency_level,
            subscription_plan,
            role,
            daily_turn_limit,
            daily_turns_used
          };
          if (password) payload.password = password;

          try {
            const url = id ? `/api/admin/users/${id}/` : `/api/admin/users/create/`;
            const method = id ? 'PUT' : 'POST';

            const res = await fetch(url, {
              method,
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) {
              showToast(data.error || 'Failed to save learner profile', 'error');
              return;
            }

            hideModal('userModal');
            showToast(data.message || 'Learner saved successfully', 'success');
            loadUsersData(1);
            loadMetrics();
          } catch (e) {
            showToast('Error saving user: ' + e, 'error');
          }
        }

        async function resetUserTurns(userId, username) {
          if (!confirm(`Reset daily turn limit counter for "${username}"?`)) return;
          try {
            const res = await fetch(`/api/admin/users/${userId}/reset-turns/`, { method: 'POST' });
            const data = await res.json();
            if (res.ok) {
              showToast(data.message, 'success');
              loadUsersData(1);
            } else {
              showToast(data.error || 'Reset failed', 'error');
            }
          } catch (e) {
            showToast('Error resetting turns', 'error');
          }
        }

        async function deleteUser(userId, username) {
          if (!confirm(`Permanently delete learner "${username}"? All associated sessions will be removed.`)) return;
          try {
            const res = await fetch(`/api/admin/users/${userId}/`, { method: 'DELETE' });
            const data = await res.json();
            if (res.ok) {
              showToast(data.message, 'success');
              loadUsersData(1);
              loadMetrics();
            } else {
              showToast(data.error || 'Delete failed', 'error');
            }
          } catch (e) {
            showToast('Error deleting user', 'error');
          }
        }

        // ─────────────────────────────────────────────────────────────────
        // 3. SCENARIOS STUDIO CRUD & AI SIMULATOR
        // ─────────────────────────────────────────────────────────────────
        function isFreeTalkScenario(s) {
          if (!s) return false;
          return s.category === 'Open Talk' || (s.title || '').toLowerCase().includes('free talk');
        }

        function handleScenarioSearch() {
          const input = document.getElementById('scenarioSearchInput');
          scenarioSearchQuery = (input ? input.value : '').trim().toLowerCase();
          renderFilteredScenariosGrid();
        }

        function filterScenariosByLang(lang) {
          activeScenarioLang = lang;
          renderScenarioLangFilterPills();
          renderFilteredScenariosGrid();
        }

        function clearScenarioFilters() {
          activeScenarioLang = 'all';
          scenarioSearchQuery = '';
          const input = document.getElementById('scenarioSearchInput');
          if (input) input.value = '';
          renderScenarioLangFilterPills();
          renderFilteredScenariosGrid();
        }

        function renderScenarioLangFilterPills() {
          const container = document.getElementById('scenarioLangFilters');
          if (!container) return;

          const roleplayScenarios = allLoadedScenarios.filter(s => !isFreeTalkScenario(s));
          const counts = { all: roleplayScenarios.length };

          roleplayScenarios.forEach(s => {
            const lang = s.lang || 'English';
            counts[lang] = (counts[lang] || 0) + 1;
          });

          const availableLangs = Object.keys(counts).filter(k => k !== 'all').sort();
          const allOptions = ['all', ...availableLangs];

          container.innerHTML = allOptions.map(lang => `
            <button type="button" class="lang-filter-pill ${activeScenarioLang === lang ? 'active' : ''}" onclick="filterScenariosByLang('${lang}')">
              <span>${lang === 'all' ? 'All Languages' : lang}</span>
              <span class="lang-count-badge">${counts[lang] || 0}</span>
            </button>
          `).join('');
        }

        function renderFilteredScenariosGrid() {
          const grid = document.getElementById('scenariosGrid');
          if (!grid) return;

          let scenarios = allLoadedScenarios.filter(s => !isFreeTalkScenario(s));

          if (activeScenarioLang !== 'all') {
            scenarios = scenarios.filter(s => (s.lang || 'English').toLowerCase() === activeScenarioLang.toLowerCase());
          }

          if (scenarioSearchQuery) {
            scenarios = scenarios.filter(s => {
              const t = (s.title || '').toLowerCase();
              const d = (s.description || '').toLowerCase();
              const c = (s.category || '').toLowerCase();
              const p = (s.prompt || '').toLowerCase();
              return t.includes(scenarioSearchQuery) || d.includes(scenarioSearchQuery) || c.includes(scenarioSearchQuery) || p.includes(scenarioSearchQuery);
            });
          }

          if (!scenarios.length) {
            grid.innerHTML = `
              <div class="col-12 text-center py-5">
                <i class="bi bi-filter-circle fs-1 text-dim mb-3 d-block"></i>
                <h3 class="h6 text-dim mb-2">No matching scenarios found</h3>
                <p class="text-dim small mb-3">Try adjusting your search query or selecting another language filter.</p>
                <button class="btn btn-subtle btn-sm" onclick="clearScenarioFilters()">
                  <i class="bi bi-arrow-counterclockwise me-1"></i>Reset Filters
                </button>
              </div>
            `;
            return;
          }

          grid.innerHTML = scenarios.map(s => {
            const safeTitle = escapeHTML(s.title || 'Untitled Scenario');
            const safeEscapedTitle = safeTitle.replace(/'/g, "\\'");
            return `
            <div class="col-12 col-md-6 col-xl-4">
              <div class="glass-card h-100 d-flex flex-column justify-content-between">
                <div>
                  <div class="d-flex align-items-center justify-content-between mb-2">
                    <span class="fs-3">${escapeHTML(s.emoji || '💬')}</span>
                    <div class="d-flex gap-1">
                      <span class="status-badge badge-lang">${escapeHTML(s.lang || 'English')}</span>
                      <span class="status-badge badge-cefr">${escapeHTML(s.cefr || 'Beginner')}</span>
                    </div>
                  </div>
                  <h3 class="h6 mb-1 text-main fw-bold">${safeTitle}</h3>
                  <small class="text-dim d-block mb-3" style="font-size: 0.8rem;">${escapeHTML(s.description || 'No description')}</small>
                  
                  <div class="p-2 rounded mb-3 font-mono text-dim" style="background: var(--bg-surface-elevated); font-size: 0.72rem; max-height: 70px; overflow: hidden; text-overflow: ellipsis;">
                    ${escapeHTML(s.prompt ? s.prompt.slice(0, 110) + '...' : 'No prompt set')}
                  </div>
                </div>

                <div class="d-flex align-items-center justify-content-between pt-2 border-top border-subtle">
                  <small class="text-dim font-mono"><i class="bi bi-play-circle me-1"></i>${s.sessions_count || 0} plays (${s.avg_score || 0}%)</small>
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-subtle p-1 px-2" title="Edit Scenario" onclick="openEditScenarioModalById(${s.id})">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-subtle p-1 px-2 text-danger" title="Delete Scenario" onclick="deleteScenario(${s.id}, '${safeEscapedTitle}')">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          `;
          }).join('');
        }

        function openEditScenarioModalById(id) {
          const scenario = allLoadedScenarios.find(s => s.id === id);
          if (scenario) {
            openEditScenarioModal(scenario);
          }
        }

        function updateScenarioBadges() {
          const roleplayCount = allLoadedScenarios.filter(s => !isFreeTalkScenario(s)).length;
          const navBadge = document.getElementById('navScenarioBadge');
          if (navBadge) navBadge.textContent = roleplayCount;
        }

        async function loadScenariosData() {
          // 1. SWR Instant render from localStorage
          try {
            const cached = localStorage.getItem('linguist_admin_scenarios');
            if (cached) {
              const parsed = JSON.parse(cached);
              allLoadedScenarios = parsed;
              freeTalkScenarioObj = allLoadedScenarios.find(isFreeTalkScenario) || null;
              updateScenarioBadges();
              renderScenarioLangFilterPills();
              renderFilteredScenariosGrid();
            }
          } catch (e) { }

          // 2. Background fresh fetch
          try {
            const res = await fetch('/api/admin/scenarios/');
            if (!res.ok) return;
            const data = await res.json();
            allLoadedScenarios = data.scenarios || [];
            freeTalkScenarioObj = allLoadedScenarios.find(isFreeTalkScenario) || null;
            localStorage.setItem('linguist_admin_scenarios', JSON.stringify(allLoadedScenarios));
            updateScenarioBadges();
            renderScenarioLangFilterPills();
            renderFilteredScenariosGrid();
            if (currentSection === 'freetalk') {
              loadFreeTalkData();
            }
          } catch (e) {
            console.error('Error loading scenarios:', e);
          }
        }

        // ─────────────────────────────────────────────────────────────────
        // FREE TALK STUDIO CONTROLLER & DIRECT AI SIMULATOR
        // ─────────────────────────────────────────────────────────────────
        let currentFreeTalkPersonaTab = 'master';
        const freeTalkPersonasData = {
          master: 'Free Talk Mode: You are a friendly, witty, and engaging conversational partner. Talk freely about any topic.',
          friendly: 'AI Persona: Friendly Pal. Warm, relatable, humorous, and curious friend chatting casually about life, hobbies, and ideas.',
          career: 'AI Persona: Career Coach & Professional Mentor. Maintain a polished, ambitious, and encouraging tone suitable for business, careers, and interviews.',
          debate: 'AI Persona: Intellectual Debate Partner. Offer intriguing, polite counter-arguments and thought-provoking perspectives to encourage deep reasoning.',
          strict: 'AI Persona: Academic Professor. Emphasize precise diction, eloquent expression, and grammatical elegance while being supportive.'
        };

        const PERSONA_CONFIG_META = {
          master: {
            label: 'AI Master Global Instructions',
            badge: 'GLOBAL MASTER',
            hint: 'This master guideline governs overall AI persona behavior, response length, and error handling for all unscripted student conversations.'
          },
          friendly: {
            label: 'Friendly Pal Persona Prompt',
            badge: '😊 FRIENDLY PAL',
            hint: 'Configures the warm, approachable, empathetic casual friend persona.'
          },
          career: {
            label: 'Career Coach Persona Prompt',
            badge: '💼 CAREER COACH',
            hint: 'Configures the ambitious, professional interview, networking, and workplace mentor persona.'
          },
          debate: {
            label: 'Debate Partner Persona Prompt',
            badge: '🧠 DEBATE PARTNER',
            hint: 'Configures the intellectually stimulating, polite counter-argument debate persona.'
          },
          strict: {
            label: 'Strict Professor Persona Prompt',
            badge: '🎓 STRICT PROFESSOR',
            hint: 'Configures the academic, linguistically precise grammar professor persona.'
          }
        };

        function switchFreeTalkPersonaTab(tabKey) {
          // 1. Sync current textarea input to in-memory store
          const input = document.getElementById('ftDirectPromptInput');
          if (input && currentFreeTalkPersonaTab) {
            freeTalkPersonasData[currentFreeTalkPersonaTab] = input.value.trim();
          }

          currentFreeTalkPersonaTab = tabKey;

          // 2. Update Tab Pills UI
          document.querySelectorAll('#ftPersonaTabs button').forEach(b => b.classList.remove('active'));
          const activeBtn = document.getElementById(`tab-persona-${tabKey}`);
          if (activeBtn) activeBtn.classList.add('active');

          // 3. Update Labels & Badges
          const meta = PERSONA_CONFIG_META[tabKey] || PERSONA_CONFIG_META.master;
          const labelEl = document.getElementById('ftPromptLabel');
          const badgeEl = document.getElementById('ftActivePersonaBadge');
          const hintEl = document.getElementById('ftPromptHint');

          if (labelEl) labelEl.textContent = meta.label;
          if (badgeEl) badgeEl.textContent = meta.badge;
          if (hintEl) hintEl.textContent = meta.hint;

          // 4. Update Textarea Value
          if (input) {
            input.value = freeTalkPersonasData[tabKey] || '';
          }
        }
        window.switchFreeTalkPersonaTab = switchFreeTalkPersonaTab;

        async function loadFreeTalkData() {
          if (!allLoadedScenarios.length) {
            await loadScenariosData();
          }

          freeTalkScenarioObj = allLoadedScenarios.find(isFreeTalkScenario) || {
            id: 27,
            title: 'Free Talk AI Studio',
            emoji: '💬',
            category: 'Open Talk',
            cefr: 'Adaptive (All Levels)',
            lang: 'English',
            description: 'Spontaneous unscripted conversational practice.',
            prompt: 'You are an intelligent, empathetic, and highly versatile language tutor in Free Talk mode. Engage the learner naturally without forcing any scripted scenario or storyline. Keep your answers concise, authentic, and culturally natural.',
            personas: {},
            sessions_count: 0,
            avg_score: 0
          };

          const sessionsEl = document.getElementById('ftKpiSessions');
          if (sessionsEl) sessionsEl.textContent = freeTalkScenarioObj.sessions_count || 0;

          const scoreEl = document.getElementById('ftKpiAvgScore');
          if (scoreEl) scoreEl.textContent = `${freeTalkScenarioObj.avg_score || 0}%`;

          const idEl = document.getElementById('ftScenarioId');
          if (idEl) idEl.textContent = freeTalkScenarioObj.id || 27;

          // Hydrate in-memory personas data from scenario object if present
          if (freeTalkScenarioObj.prompt) {
            freeTalkPersonasData.master = freeTalkScenarioObj.prompt;
          }
          if (freeTalkScenarioObj.personas && typeof freeTalkScenarioObj.personas === 'object') {
            if (freeTalkScenarioObj.personas.friendly) freeTalkPersonasData.friendly = freeTalkScenarioObj.personas.friendly;
            if (freeTalkScenarioObj.personas.career) freeTalkPersonasData.career = freeTalkScenarioObj.personas.career;
            if (freeTalkScenarioObj.personas.debate) freeTalkPersonasData.debate = freeTalkScenarioObj.personas.debate;
            if (freeTalkScenarioObj.personas.strict) freeTalkPersonasData.strict = freeTalkScenarioObj.personas.strict;
          }

          switchFreeTalkPersonaTab('master');

          const saveStatus = document.getElementById('ftSaveStatusText');
          if (saveStatus) {
            saveStatus.innerHTML = '<i class="bi bi-check2-circle text-success me-1"></i>Synchronized with database';
          }
        }

        async function saveFreeTalkDirect() {
          const promptInput = document.getElementById('ftDirectPromptInput');
          if (promptInput && currentFreeTalkPersonaTab) {
            freeTalkPersonasData[currentFreeTalkPersonaTab] = promptInput.value.trim();
          }

          const btn = document.getElementById('btnSaveFreeTalkDirect');
          const saveStatus = document.getElementById('ftSaveStatusText');
          if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Saving...';
          }
          if (saveStatus) {
            saveStatus.innerHTML = '<span class="spinner-border spinner-border-sm me-1 text-primary"></span>Saving to database...';
          }

          const id = freeTalkScenarioObj ? freeTalkScenarioObj.id : 27;
          const payload = {
            title: freeTalkScenarioObj?.title || 'Free Talk AI Studio',
            emoji: freeTalkScenarioObj?.emoji || '💬',
            category: 'Open Talk',
            cefr: 'Beginner',
            lang: 'English',
            description: freeTalkScenarioObj?.description || 'Spontaneous unscripted conversational practice.',
            prompt: freeTalkPersonasData.master || 'Free Talk Mode: You are a friendly, witty, and engaging conversational partner. Talk freely about any topic.',
            personas: {
              friendly: freeTalkPersonasData.friendly,
              career: freeTalkPersonasData.career,
              debate: freeTalkPersonasData.debate,
              strict: freeTalkPersonasData.strict
            }
          };

          try {
            const url = id ? `/api/admin/scenarios/${id}/` : `/api/admin/scenarios/`;
            const method = id ? 'PUT' : 'POST';

            const res = await fetch(url, {
              method,
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) {
              showToast(data.error || 'Failed to save Free Talk prompt', 'error');
              if (saveStatus) saveStatus.innerHTML = '<i class="bi bi-exclamation-triangle text-danger me-1"></i>Failed to save changes';
              return;
            }

            if (freeTalkScenarioObj) {
              freeTalkScenarioObj.prompt = payload.prompt;
              freeTalkScenarioObj.personas = payload.personas;
            }
            showToast('All Free Talk personas saved successfully!', 'success');
            if (saveStatus) {
              saveStatus.innerHTML = '<i class="bi bi-check2-circle text-success me-1"></i>Saved at ' + new Date().toLocaleTimeString();
            }
            loadScenariosData();
            loadMetrics();
          } catch (e) {
            showToast('Error saving Free Talk: ' + e, 'error');
            if (saveStatus) saveStatus.innerHTML = '<i class="bi bi-exclamation-triangle text-danger me-1"></i>Connection error';
          } finally {
            if (btn) {
              btn.disabled = false;
              btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Save All Personas';
            }
          }
        }

        async function testFreeTalkDirect() {
          const promptInput = document.getElementById('ftDirectPromptInput');
          if (promptInput && currentFreeTalkPersonaTab) {
            freeTalkPersonasData[currentFreeTalkPersonaTab] = promptInput.value.trim();
          }

          const selectedPersona = document.getElementById('ftSimPersona')?.value || 'friendly';
          const userMsg = (document.getElementById('ftSimInput')?.value || '').trim();
          const lang = document.getElementById('ftSimLang')?.value || 'English';
          const cefr = document.getElementById('ftSimCefr')?.value || 'Intermediate';
          const resultBox = document.getElementById('ftSimResultBox');
          const btn = document.getElementById('btnTestFreeTalkDirect');

          if (!userMsg) {
            showToast('Please enter a sample message to simulate', 'info');
            document.getElementById('ftSimInput')?.focus();
            return;
          }

          const personaPrompt = freeTalkPersonasData[selectedPersona] || freeTalkPersonasData.master;
          const fullPromptToSend = `${freeTalkPersonasData.master}\n${personaPrompt}`;

          if (btn) btn.disabled = true;
          if (resultBox) {
            resultBox.innerHTML = '<span class="spinner-border spinner-border-sm me-2 text-primary"></span>Simulating <strong>' + selectedPersona.toUpperCase() + '</strong> in <strong>' + lang + '</strong> (' + cefr + ')...';
          }

          try {
            const res = await fetch('/api/admin/scenarios/test-prompt/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                prompt: fullPromptToSend,
                persona: selectedPersona,
                user_message: userMsg,
                cefr,
                lang
              })
            });
            const data = await res.json();
            if (res.ok) {
              const fb = data.feedback || {};
              resultBox.innerHTML = `
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="text-primary fw-bold small"><i class="bi bi-robot me-1"></i>AI Persona (${selectedPersona.toUpperCase()} • ${data.target_language || lang}):</span>
                  <span class="status-badge badge-lang">${data.target_language || lang} • ${data.cefr || cefr}</span>
                </div>
                <div class="p-2 rounded mb-2 text-main bg-dark bg-opacity-50 border border-subtle">
                  "${data.ai_reply || 'No response generated'}"
                </div>
                <div class="d-flex flex-wrap gap-2 small font-mono text-dim">
                  <span>Grammar: <strong class="text-info">${fb.grammar_score ?? 85}%</strong></span>
                  <span>•</span>
                  <span>Pronunciation: <strong class="text-success">${fb.pronunciation_score ?? 90}%</strong></span>
                  <span>•</span>
                  <span>Vocabulary: <strong class="text-warning">${fb.vocabulary_score ?? 80}%</strong></span>
                </div>
                ${fb.comments ? `<div class="text-dim small mt-1"><em>${fb.comments}</em></div>` : ''}
              `;
            } else {
              resultBox.innerHTML = `<span class="text-danger"><i class="bi bi-exclamation-triangle me-1"></i>Error: ${data.error || 'AI simulation failed'}</span>`;
            }
          } catch (e) {
            resultBox.innerHTML = `<span class="text-danger"><i class="bi bi-exclamation-triangle me-1"></i>Error: ${e}</span>`;
          } finally {
            if (btn) btn.disabled = false;
          }
        }

        function openCreateScenarioModal() {
          document.getElementById('scenarioModalTitle').textContent = 'Create Practice Scenario';
          document.getElementById('scenarioFormId').value = '';
          document.getElementById('scenarioFormTitle').value = '';
          document.getElementById('scenarioFormEmoji').value = '💬';
          document.getElementById('scenarioFormCategory').value = 'Daily Life';
          document.getElementById('scenarioFormCefr').value = 'Beginner';
          document.getElementById('scenarioFormLang').value = 'English';
          document.getElementById('scenarioFormDesc').value = '';
          document.getElementById('scenarioFormPrompt').value = 'You are a helpful and polite conversation partner.';
          document.getElementById('scenarioTestResult').textContent = 'AI simulation test results will appear here.';
          showModal('scenarioModal');
        }

        function openEditScenarioModal(s) {
          document.getElementById('scenarioModalTitle').textContent = `Edit Scenario: ${s.title}`;
          document.getElementById('scenarioFormId').value = s.id;
          document.getElementById('scenarioFormTitle').value = s.title;
          document.getElementById('scenarioFormEmoji').value = s.emoji || '💬';
          document.getElementById('scenarioFormCategory').value = s.category || 'Daily Life';
          document.getElementById('scenarioFormCefr').value = s.cefr || 'Beginner';
          document.getElementById('scenarioFormLang').value = s.lang || 'English';
          document.getElementById('scenarioFormDesc').value = s.description || '';
          document.getElementById('scenarioFormPrompt').value = s.prompt || '';
          document.getElementById('scenarioTestResult').textContent = 'AI simulation test results will appear here.';
          showModal('scenarioModal');
        }

        async function saveScenarioForm() {
          const id = document.getElementById('scenarioFormId').value;
          const title = document.getElementById('scenarioFormTitle').value.trim();
          if (!title) {
            showToast('Scenario title is required', 'error');
            return;
          }

          const payload = {
            title,
            emoji: document.getElementById('scenarioFormEmoji').value.trim() || '💬',
            category: document.getElementById('scenarioFormCategory').value.trim(),
            cefr: document.getElementById('scenarioFormCefr').value,
            lang: document.getElementById('scenarioFormLang').value,
            description: document.getElementById('scenarioFormDesc').value.trim(),
            prompt: document.getElementById('scenarioFormPrompt').value.trim()
          };

          try {
            const url = id ? `/api/admin/scenarios/${id}/` : `/api/admin/scenarios/`;
            const method = id ? 'PUT' : 'POST';

            const res = await fetch(url, {
              method,
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) {
              showToast(data.error || 'Failed to save scenario', 'error');
              return;
            }

            hideModal('scenarioModal');
            showToast('Scenario saved successfully!', 'success');
            loadScenariosData();
            loadMetrics();
          } catch (e) {
            showToast('Error saving scenario: ' + e, 'error');
          }
        }

        async function deleteScenario(id, title) {
          if (!confirm(`Delete scenario "${title}"?`)) return;
          try {
            const res = await fetch(`/api/admin/scenarios/${id}/`, { method: 'DELETE' });
            const data = await res.json();
            if (res.ok) {
              showToast(data.message, 'success');
              loadScenariosData();
              loadMetrics();
            } else {
              showToast(data.error || 'Delete failed', 'error');
            }
          } catch (e) {
            showToast('Error deleting scenario', 'error');
          }
        }

        async function seedScenariosTrigger() {
          try {
            showToast('Seeding default scenarios...', 'info');
            const res = await fetch('/api/admin/scenarios/seed/', { method: 'POST' });
            const data = await res.json();
            if (res.ok) {
              showToast(data.message, 'success');
              loadScenariosData();
              loadMetrics();
            } else {
              showToast(data.error || 'Seeding failed', 'error');
            }
          } catch (e) {
            showToast('Error triggering scenario seed', 'error');
          }
        }

        async function testScenarioPromptLive() {
          const prompt = document.getElementById('scenarioFormPrompt').value.trim() || 'You are a friendly conversation partner.';
          const userMsg = document.getElementById('scenarioTestInput').value.trim() || 'Hello! What do you recommend?';
          const cefr = document.getElementById('scenarioFormCefr').value || 'Beginner';
          const lang = document.getElementById('scenarioFormLang').value || 'English';
          const resultBox = document.getElementById('scenarioTestResult');

          resultBox.innerHTML = '<span class="spinner-border spinner-border-sm me-2 text-primary"></span>Simulating AI Persona response in <strong>' + lang + '</strong> (' + cefr + ')...';

          try {
            const res = await fetch('/api/admin/scenarios/test-prompt/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ prompt, user_message: userMsg, cefr, lang })
            });
            const data = await res.json();
            if (res.ok) {
              const fb = data.feedback || {};
              resultBox.innerHTML = `
            <div class="d-flex align-items-center justify-content-between mb-2">
              <span class="text-primary fw-bold small"><i class="bi bi-robot me-1"></i>AI Persona (${data.target_language || lang}):</span>
              <span class="status-badge badge-lang">${data.target_language || lang} • ${data.cefr || cefr}</span>
            </div>
            <div class="p-2 rounded mb-2 text-main bg-dark bg-opacity-50 border border-subtle">
              "${data.ai_reply || 'No response generated'}"
            </div>
            <div class="d-flex flex-wrap gap-2 small font-mono text-dim">
              <span>Grammar: <strong class="text-info">${fb.grammar_score ?? 85}%</strong></span>
              <span>•</span>
              <span>Pronunciation: <strong class="text-success">${fb.pronunciation_score ?? 90}%</strong></span>
              <span>•</span>
              <span>Vocabulary: <strong class="text-warning">${fb.vocabulary_score ?? 80}%</strong></span>
            </div>
            ${fb.comments ? `<div class="text-dim small mt-1"><em>${fb.comments}</em></div>` : ''}
          `;
            } else {
              resultBox.innerHTML = `<span class="text-danger"><i class="bi bi-exclamation-triangle me-1"></i>Error: ${data.error || 'AI simulation failed'}</span>`;
            }
          } catch (e) {
            resultBox.innerHTML = `<span class="text-danger"><i class="bi bi-exclamation-triangle me-1"></i>Error: ${e}</span>`;
          }
        }

        // ─────────────────────────────────────────────────────────────────
        // 4. SESSIONS & CONVERSATION INSPECTOR
        // ─────────────────────────────────────────────────────────────────
        function renderSessionsTable(data) {
          const tbody = document.getElementById('sessionsTableBody');
          if (!tbody) return;
          if (!data.sessions || !data.sessions.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-dim py-5">No learning sessions recorded yet</td></tr>';
            document.getElementById('sessionPaginationInfo').textContent = '0 sessions';
            document.getElementById('sessionPaginationButtons').innerHTML = '';
            return;
          }

          tbody.innerHTML = data.sessions.map(s => {
            const numScore = (s.overall_score !== null && s.overall_score !== undefined) ? parseFloat(s.overall_score) : null;
            const scoreDisplay = numScore !== null && !isNaN(numScore) ? numScore.toFixed(1) + '%' : '-';
            const scoreBadgeClass = numScore !== null ? (numScore >= 80 ? 'badge-vip' : (numScore >= 60 ? 'badge-free' : 'bg-danger text-white')) : 'badge-free';

            return `
            <tr>
              <td><code class="text-primary font-mono">${(s.id || '').slice(0, 8)}...</code></td>
              <td>
                <div class="fw-bold">${s.user_name || 'Anonymous'}</div>
                <small class="text-dim font-mono" style="font-size: 0.75rem;">${s.user_email || '-'}</small>
              </td>
              <td><span class="fw-bold">${s.scenario_title || 'Free Practice'}</span></td>
              <td>
                <span class="status-badge ${scoreBadgeClass} font-mono">
                  ${scoreDisplay}
                </span>
              </td>
              <td><span class="badge bg-secondary text-white font-mono">${s.turns_count || 0} turns</span></td>
              <td><small class="text-dim font-mono">${s.started_at ? new Date(s.started_at).toLocaleString() : '-'}</small></td>
              <td class="text-end">
                <button class="btn btn-sm btn-subtle" onclick="inspectSession('${s.id}')">
                  <i class="bi bi-search me-1"></i>Inspect Replay
                </button>
              </td>
            </tr>
          `;
          }).join('');

          document.getElementById('sessionPaginationInfo').textContent = `Showing page ${data.page || 1} of ${data.total_pages || 1} (${data.total || 0} total sessions)`;
          renderPaginationButtons('sessionPaginationButtons', data.page || 1, data.total_pages || 1, loadSessionsData);
        }

        async function loadSessionsData(page = 1) {
          // 1. SWR Instant render from localStorage for page 1
          if (page === 1) {
            try {
              const cached = localStorage.getItem('linguist_admin_sessions_p1');
              if (cached) {
                const parsed = JSON.parse(cached);
                renderSessionsTable(parsed);
              }
            } catch (e) {}
          }

          // 2. Fresh background fetch
          try {
            const res = await fetch(`/api/admin/sessions/?page=${page}`);
            if (!res.ok) {
              const tbody = document.getElementById('sessionsTableBody');
              if (tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center text-dim py-5">Failed to load sessions data</td></tr>';
              return;
            }
            const data = await res.json();
            renderSessionsTable(data);

            if (page === 1) {
              localStorage.setItem('linguist_admin_sessions_p1', JSON.stringify(data));
            }
          } catch (e) {
            console.error('Error loading sessions:', e);
            const tbody = document.getElementById('sessionsTableBody');
            if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="text-center text-dim py-5">Error: ${e.message || e}</td></tr>`;
          }
        }

        async function inspectSession(sessionId) {
          try {
            const res = await fetch(`/api/admin/sessions/${sessionId}/`);
            if (!res.ok) return;
            const data = await res.json();

            document.getElementById('sessionInspectorTitle').textContent = `Session: ${data.session.scenario_title}`;
            document.getElementById('sessionInspectorSubtitle').textContent = `Learner: ${data.session.user_name} (${data.session.user_email}) • ${data.session.total_turns} Turns • Score: ${data.session.overall_score || 0}%`;

            const container = document.getElementById('sessionInspectorTurns');
            if (!data.turns.length) {
              container.innerHTML = '<div class="text-center text-dim py-4">No interaction turns logged in this session.</div>';
            } else {
              container.innerHTML = data.turns.map(t => {
                let feedbackHtml = '';
                if (t.detailed_feedback) {
                  const fb = t.detailed_feedback;
                  feedbackHtml = `
                <div class="mt-2 p-2 rounded small" style="background: var(--bg-base); border: 1px solid var(--border-subtle);">
                  <div class="d-flex gap-2 mb-1">
                    <span class="status-badge badge-vip font-mono">Grammar: ${fb.grammar_score || 0}%</span>
                    <span class="status-badge badge-lang font-mono">Pronunciation: ${fb.pronunciation_score || 0}%</span>
                    <span class="status-badge badge-cefr font-mono">Vocabulary: ${fb.vocabulary_score || 0}%</span>
                  </div>
                  ${fb.corrections && fb.corrections.length ? `
                    <div class="text-danger small mt-1">
                      <b>Correction:</b> "${fb.corrections[0].original}" ➔ <span class="text-success">"${fb.corrections[0].corrected}"</span>
                      <div class="text-dim">${fb.corrections[0].explanation || ''}</div>
                    </div>
                  ` : ''}
                </div>
              `;
                }

                return `
              <div class="turn-card">
                <div class="d-flex justify-content-between mb-2">
                  <span class="turn-speaker text-primary"><i class="bi bi-person me-1"></i>Learner Turn #${t.turn_number}</span>
                  <small class="text-dim font-mono">${t.created_at ? new Date(t.created_at).toLocaleTimeString() : ''}</small>
                </div>
                <div class="p-2 rounded mb-2" style="background: var(--bg-base);">
                  <div class="text-main">"${t.user_transcript || '<i class="text-dim">No transcript</i>'}"</div>
                </div>

                <div class="turn-speaker text-success"><i class="bi bi-robot me-1"></i>AI Companion Response</div>
                <div class="p-2 rounded mb-2 text-main" style="background: var(--bg-base);">
                  <div>"${t.ai_response_text || '<i class="text-dim">No reply</i>'}"</div>
                  ${t.ai_audio_url ? `
                    <audio controls src="${t.ai_audio_url}" class="mt-2 w-100" style="height: 32px;"></audio>
                  ` : ''}
                </div>

                ${feedbackHtml}
              </div>
            `;
              }).join('');
            }

            showModal('sessionModal');
          } catch (e) {
            showToast('Error loading session details: ' + e, 'error');
          }
        }

        // ─────────────────────────────────────────────────────────────────
        // 5. FLASHCARDS & VOCABULARY
        // ─────────────────────────────────────────────────────────────────
        async function loadFlashcardsData() {
          try {
            const res = await fetch('/api/admin/flashcards/');
            if (!res.ok) return;
            const data = await res.json();

            document.getElementById('fcTotalCards').textContent = data.total_cards;
            document.getElementById('fcDueCards').textContent = data.due_cards;
            document.getElementById('fcAvgEase').textContent = data.avg_ease_factor;
            document.getElementById('fcAvgReps').textContent = data.avg_repetitions;

            const tbody = document.getElementById('flashcardsTableBody');
            if (!data.recent_cards.length) {
              tbody.innerHTML = '<tr><td colspan="8" class="text-center text-dim py-5">No vocabulary cards in database</td></tr>';
              return;
            }

            tbody.innerHTML = data.recent_cards.map(c => `
          <tr>
            <td><span class="fw-bold text-main">${c.word}</span></td>
            <td><span class="text-dim">${c.translation || '-'}</span></td>
            <td><span class="status-badge badge-lang">${c.language}</span></td>
            <td><small class="text-dim font-mono">${c.user_email}</small></td>
            <td><span class="badge bg-secondary font-mono">${c.repetitions}</span></td>
            <td class="font-mono">${c.interval} d</td>
            <td><span class="status-badge badge-cefr font-mono">${c.ease_factor}</span></td>
            <td><small class="text-dim font-mono">${c.next_review ? new Date(c.next_review).toLocaleDateString() : '-'}</small></td>
          </tr>
        `).join('');
          } catch (e) {
            console.error('Error loading flashcards:', e);
          }
        }

        // ─────────────────────────────────────────────────────────────────
        // 6. SYSTEM HEALTH & MAINTENANCE
        // ─────────────────────────────────────────────────────────────────
        async function loadMaintenanceData() {
          try {
            const res = await fetch('/api/admin/system-health/');
            if (!res.ok) return;
            const data = await res.json();

            document.getElementById('maintAudioFilesCount').textContent = data.storage.total_files;
            document.getElementById('maintAudioMb').textContent = data.storage.size_mb;
            document.getElementById('maintMediaPath').textContent = data.storage.media_path;
          } catch (e) {
            console.error('Error loading system health:', e);
          }
        }

        async function runAudioCleanup() {
          const btn = document.getElementById('btnAudioCleanup');
          btn.disabled = true;
          btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Running Garbage Collection...';

          try {
            const res = await fetch('/api/admin/system/cleanup-audio/', { method: 'POST' });
            const data = await res.json();
            if (res.ok) {
              showToast(data.message || 'Cleanup completed', 'success');
              loadMaintenanceData();
              loadMetrics();
            } else {
              showToast(data.error || 'Cleanup failed', 'error');
            }
          } catch (e) {
            showToast('Error triggering audio cleanup: ' + e, 'error');
          } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-trash3-fill me-1 text-danger"></i>Run Audio GC (30d+ Cleanup)';
          }
        }
