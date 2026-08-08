# 📋 LinguistAI Backend Task Roadmap & Progress Checklist

Tài liệu theo dõi và quản lý toàn bộ các đầu việc Backend cho dự án **LinguistAI**.

---

## 🟢 PHASE 1: CORE AI & AUDIO ENGINE (ĐÃ HOÀN THÀNH ✅)
- [x] **Task 1.1**: Dynamic LLM Conversation Service (`myapp/ai_services.py`) kết nối OpenAI GPT-4o-mini với ngữ cảnh kịch bản, cấp độ CEFR & lịch sử hội thoại (`context_history`).
- [x] **Task 1.2**: Multi-layered JSON Feedback Generator (Đánh giá Grammar, Pronunciation, Vocab score, xuất câu sửa lỗi `corrections` và gợi ý `suggestions`).
- [x] **Task 1.3**: OpenAI Whisper Speech-to-Text Endpoint (`POST /api/sessions/<uuid>/respond-audio/`) tiếp nhận file giọng nói `.webm`.
- [x] **Task 1.4**: ElevenLabs Text-to-Speech Voice Generation (`generate_tts_elevenlabs`) phát sinh file audio mp3 giọng đọc AI tự nhiên.
- [x] **Task 1.5**: Smart Simulation / Fallback Mode (Tự động giả lập phản hồi mượt mà khi chưa khai báo API Keys).

---

## 🟢 PHASE 2: AUTHENTICATION & SUPABASE SYNC (ĐÃ HOÀN THÀNH ✅)
- [x] **Task 2.1**: Hệ thống API Xác thực (`/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/me/`).
- [x] **Task 2.2**: Phân tách rõ ràng giữa `email` (đăng nhập) và `username` (biệt danh hiển thị).
- [x] **Task 2.3**: Đồng bộ bản ghi người dùng trực tiếp vào Supabase Auth và Supabase PostgreSQL `users` table via Client SDK.
- [x] **Task 2.4**: Sửa lỗi thông báo Session Message & làm sạch Session Storage khi Logout.
- [x] **Task 2.5**: User Profile Update API (`PUT /api/user/profile/`) hỗ trợ cập nhật Target Language, CEFR level, Username và đồng bộ Supabase.

---

## 🟢 PHASE 3: DATABASE, RATE LIMITING & TESTING (ĐÃ HOÀN THÀNH ✅)
- [x] **Task 3.1**: Cấu hình CSDL PostgreSQL Supabase Cloud qua `dj-database-url` & `psycopg2-binary` (kèm SQLite fallback cho dev).
- [x] **Task 3.2**: B-Tree Indexes cho `LearningSession` (`user_id`, `started_at`) và `InteractionLog` (`session_id`, `created_at`).
- [x] **Task 3.3**: Free Tier Daily Rate Limiting Enforcer (`check_user_daily_turn_limit` - Giới hạn 5 lượt/ngày, trả lỗi HTTP 403).
- [x] **Task 3.4**: Django Management Command Dọn Dẹp File Audio Quá 30 Ngày (`python manage.py cleanup_audio_files`).
- [x] **Task 3.5**: Bộ Kiểm Thử Tự Động Backend (`myapp/tests.py` - 6/6 Unit Test Cases PASSED 100%).

---

## 🟡 PHASE 4: ADVANCED BACKEND ENHANCEMENTS (CÁC TASK NÂNG CẤP TIẾP THEO 🚀)

### 1. Task 4.1: Script SQL Cấu Hình Row Level Security (RLS) Trên Supabase
- [ ] **Mô tả**: Viết file script `supabase_rls_policies.sql` cài đặt RLS trên các bảng `users`, `learning_sessions`, `interaction_logs`.
- [ ] **Mục tiêu**: Đảm bảo trên Supabase Database, mỗi người dùng chỉ có quyền SELECT, INSERT, UPDATE, DELETE bản ghi của chính họ (`auth.uid() = user_id`).

### 2. Task 4.2: Middleware Kiểm Tra Quyền Authentication Token (`myapp/middleware.py`)
- [ ] **Mô tả**: Tạo Django Middleware kiểm tra Session / Bearer Token đối với tất cả các API nằm trong `/api/`.
- [ ] **Mục tiêu**: Trả về lỗi HTTP 401 Unauthorized chuẩn JSON khi request chưa được xác thực, ngăn chặn truy cập trái phép vào API.

### 3. Task 4.3: API Thống Kê Tiến Độ Học Tập Cho Dashboard (`GET /api/user/<uuid>/analytics/`)
- [ ] **Mô tả**: Viết endpoint tính toán điểm trung bình Grammar, Pronunciation, Vocabulary theo từng tuần/tháng từ bảng `interaction_logs`.
- [ ] **Mục tiêu**: Trả về JSON tổng hợp dữ liệu tiến độ sẵn sàng cho Frontend vẽ biểu đồ (Chart.js / ApexCharts).

### 4. Task 4.4: Script Tự Động Hóa Lịch Dọn Dẹp Audio (`crontab` / System Cron)
- [ ] **Mô tả**: Tạo file script bash `scripts/run_cleanup_cron.sh` và hướng dẫn cài đặt `crontab` trên server Linux.
- [ ] **Mục tiêu**: Tự động kích hoạt lệnh `python manage.py cleanup_audio_files` định kỳ 00:00 mỗi Chủ Nhật.

### 5. Task 4.5: Middleware Xử Lý Lỗi Hệ Thống Toàn Cục (Global Exception Handler)
- [ ] **Mô tả**: Viết Middleware bắt tất cả các ngoại lệ không mong muốn (500 Internal Server Error).
- [ ] **Mục tiêu**: Tránh làm lộ Traceback mã nguồn Python ra client, trả về định dạng JSON lỗi chuẩn `{ "error": "Internal server error", "code": 500 }`.
