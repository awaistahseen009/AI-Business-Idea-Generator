-- AI Business Idea Generator Database Setup Script
-- Run this script in your Supabase SQL editor

-- Create users table
CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create business_ideas table
CREATE TABLE IF NOT EXISTS public.business_ideas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    niche VARCHAR(255) NOT NULL,
    ideas JSONB NOT NULL, -- stores the 3 ideas, each with pitch, audience, and revenue model
    web_search_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_business_ideas_user_id ON public.business_ideas(user_id);
CREATE INDEX IF NOT EXISTS idx_business_ideas_created_at ON public.business_ideas(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_business_ideas_niche ON public.business_ideas(niche);

-- Enable Row Level Security (RLS) for better security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.business_ideas ENABLE ROW LEVEL SECURITY;

-- Create policies for users table
CREATE POLICY "Users can view their own data" ON public.users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own data" ON public.users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Create policies for business_ideas table
CREATE POLICY "Users can view their own ideas" ON public.business_ideas
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own ideas" ON public.business_ideas
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own ideas" ON public.business_ideas
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own ideas" ON public.business_ideas
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional - remove in production)
-- INSERT INTO public.users (email, password_hash) VALUES 
-- ('demo@example.com', 'scrypt:32768:8:1$salt$hash'); -- This is just an example, use proper hashing

COMMENT ON TABLE public.users IS 'Stores user account information';
COMMENT ON TABLE public.business_ideas IS 'Stores generated business ideas for each user';
COMMENT ON COLUMN public.business_ideas.ideas IS 'JSONB array containing 3 business ideas with name, pitch, audience, and revenue_model';
COMMENT ON COLUMN public.business_ideas.web_search_used IS 'Boolean flag indicating if web search was used during idea generation';
