-- ==============================================================================
-- LinguistAI Supabase Row Level Security (RLS) Policies
-- ==============================================================================
-- This SQL script configures strict Row Level Security (RLS) on Supabase PostgreSQL
-- ensuring users can only access their own profile, learning sessions, and interaction logs.
-- ==============================================================================

-- 1. Enable Row Level Security on all core tables
ALTER TABLE IF EXISTS users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS learning_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS interaction_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS scenarios ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------------------
-- 2. POLICIES FOR `users` TABLE
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Users can view their own profile" ON users;
CREATE POLICY "Users can view their own profile"
ON users FOR SELECT
USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update their own profile" ON users;
CREATE POLICY "Users can update their own profile"
ON users FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Users can insert their own profile on signup" ON users;
CREATE POLICY "Users can insert their own profile on signup"
ON users FOR INSERT
WITH CHECK (auth.uid() = id);

-- ------------------------------------------------------------------------------
-- 3. POLICIES FOR `learning_sessions` TABLE
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Users can view their own learning sessions" ON learning_sessions;
CREATE POLICY "Users can view their own learning sessions"
ON learning_sessions FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can create learning sessions for themselves" ON learning_sessions;
CREATE POLICY "Users can create learning sessions for themselves"
ON learning_sessions FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update their own learning sessions" ON learning_sessions;
CREATE POLICY "Users can update their own learning sessions"
ON learning_sessions FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete their own learning sessions" ON learning_sessions;
CREATE POLICY "Users can delete their own learning sessions"
ON learning_sessions FOR DELETE
USING (auth.uid() = user_id);

-- ------------------------------------------------------------------------------
-- 4. POLICIES FOR `interaction_logs` TABLE
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Users can view interaction logs of their own sessions" ON interaction_logs;
CREATE POLICY "Users can view interaction logs of their own sessions"
ON interaction_logs FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM learning_sessions
        WHERE learning_sessions.id = interaction_logs.session_id
        AND learning_sessions.user_id = auth.uid()
    )
);

DROP POLICY IF EXISTS "Users can insert interaction logs for their own sessions" ON interaction_logs;
CREATE POLICY "Users can insert interaction logs for their own sessions"
ON interaction_logs FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM learning_sessions
        WHERE learning_sessions.id = interaction_logs.session_id
        AND learning_sessions.user_id = auth.uid()
    )
);

DROP POLICY IF EXISTS "Users can delete interaction logs of their own sessions" ON interaction_logs;
CREATE POLICY "Users can delete interaction logs of their own sessions"
ON interaction_logs FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM learning_sessions
        WHERE learning_sessions.id = interaction_logs.session_id
        AND learning_sessions.user_id = auth.uid()
    )
);

-- ------------------------------------------------------------------------------
-- 5. POLICIES FOR `scenarios` TABLE (Read-only catalog for learners)
-- ------------------------------------------------------------------------------
DROP POLICY IF EXISTS "Allow read access to scenarios for all authenticated and anonymous users" ON scenarios;
CREATE POLICY "Allow read access to scenarios for all authenticated and anonymous users"
ON scenarios FOR SELECT
USING (true);

-- End of Supabase RLS Policies Configuration
