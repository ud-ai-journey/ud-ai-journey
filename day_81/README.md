# 🏆 One-Minute Win: Supabase Habit Tracker – Day 81

## 🚀 Overview
This project is a **production-ready, full-stack habit tracking app** built with:
- **Supabase** (Postgres, Auth, Edge Functions, RLS)
- **Vite + React** frontend (TypeScript, modern hooks, modular design)
- **Automated testing and deployment scripts**

It's the result of a day-long, hands-on journey—**juggling ideas, debugging, and enhancing**—with the help of Perplexity, Gemini, Bolt, Claude, NotebookLM, and finally, Cursor for deep code integration and automation.

---

## 🧠 Research & AI-Driven Workflow

This project is the result of a deep, multi-stage research and prototyping journey, leveraging the best free AI tools and academic insights:

- **Research Phase:**  
  - Used **Perplexity** to explore the science of micro-habits, small wins, and their neurological impact, referencing research papers from **MIT** and **Stanford**.
  - Consumed podcasts and long-form content, then used **NotebookLM** to synthesize and understand the data provided by Perplexity.
  - Validated the proof of concept with further Perplexity queries and cross-checked with academic sources.

- **Ideation & Prototyping:**  
  - Used **Claude** to brainstorm and ideate features and user flows.
  - Leveraged **Gemini** to structure and refine the thought process, ensuring a solid foundation for the app.
  - Built the initial MVP with **Bolt**, rapidly iterating on the core features.

- **Enhancement & Integration:**  
  - Switched to **Cursor** for deep code integration, debugging, and enhancement—bringing the MVP to a production-ready, full-stack solution.

**All tools and resources used were free.**  
This is **Day 81** of my journey—a testament to the power of open research, AI collaboration, and relentless curiosity.

---

## 🛠️ Technical Journey

### 1. **Backend Foundation**
- **Supabase project setup**: Database, Auth, and Edge Functions.
- **Schema design**: Tables for `user_profiles`, `rituals`, `daily_completions`, `user_badges`, `user_streaks`.
- **Row Level Security (RLS)**: Locked down all tables, then carefully opened up read/insert as needed for both authenticated and anonymous users.
- **Edge Functions**: Wrote robust TypeScript functions for:
  - Completing rituals (with streak and badge logic)
  - Fetching user stats and badges
- **Migrations**: Cleaned up SQL files, removed non-SQL content, and ensured all migrations ran cleanly.

### 2. **DevOps & Automation**
- **Supabase CLI**: Installed and configured, fixed PATH issues, and linked local to cloud project.
- **Automated test scripts**: Wrote Node.js scripts to:
  - Test all backend endpoints
  - Insert test users and rituals
  - Debug RLS and foreign key issues
- **Iterative debugging**: Used logs and error codes to fix UUID, RLS, and foreign key problems.

### 3. **Frontend Integration**
- **Vite + React app**: Modular, modern, and type-safe.
- **Supabase client**: Centralized in `src/lib/supabase.ts` with environment variables.
- **Hooks**: Custom hooks for auth, completions, streaks, and API calls.
- **Edge function integration**: All ritual actions, stats, and badges flow through Supabase edge functions.
- **Celebration UI**: Real-time feedback for completions and badge unlocks.

### 4. **Testing & Verification**
- **Automated end-to-end test script**: Signs up a user, inserts a profile, completes a ritual, and fetches stats/badges.
- **Manual and automated RLS policy adjustments**: Ensured security and smooth developer experience.

### 5. **Production-Ready Deployment**
- **Deployment guides** for Vercel/Netlify.
- **Environment variable management** for secure, scalable deployment.

---

## 🧩 Folder Structure

```
day_81/
  src/                # React frontend (Vite, TypeScript, hooks, components)
  supabase/           # Migrations, edge functions, SQL policies
  *.cjs, *.js         # Automated test and verification scripts
  *.md                # Guides, summaries, and this README
  package.json        # Project dependencies
  .env                # Environment variables (not committed)
```

---

## 📝 How to Run Locally

1. **Clone the repo**
2. **Install dependencies**
   ```bash
   npm install
   ```
3. **Set up your `.env`**
   ```
   VITE_SUPABASE_URL=your-supabase-url
   VITE_SUPABASE_ANON_KEY=your-anon-key
   ```
4. **Start the frontend**
   ```bash
   npm run dev
   ```
5. **Run backend test scripts**
   ```bash
   node final-working-test.cjs
   ```

---

## 🚀 How to Deploy

1. **Push to GitHub**
2. **Deploy to Vercel/Netlify**
3. **Set environment variables in the dashboard**
4. **Enjoy your production-ready habit tracker!**

---

## 🧑‍💻 Credits & Tools Used

- **Perplexity, NotebookLM, Claude, Gemini, Bolt**: For research, ideation, and rapid prototyping.
- **Cursor**: For deep code integration, debugging, and automation.
- **Supabase**: The backbone of authentication, database, and edge logic.
- **Vite + React**: For a modern, fast, and beautiful frontend.
- **You!** For persistence, curiosity, and a willingness to learn and iterate.

---

## 🏁 Reflections

This project is a testament to the power of modern full-stack tools, AI-assisted development, and a growth mindset.  
**Every error was a lesson, every fix a step forward.**  
If you're reading this, you can build, debug, and ship amazing things too!

---

**Happy shipping! 🚀** 