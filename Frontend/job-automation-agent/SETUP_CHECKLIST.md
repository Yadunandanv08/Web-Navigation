# Complete Setup Checklist

Complete this checklist to get your JobAgent running.

---

## Phase 1: Firebase Project Setup (15 minutes)

### Create Firebase Project
- [ ] Go to https://console.firebase.google.com/
- [ ] Click "Add project"
- [ ] Name it "JobAgent"
- [ ] Accept default settings
- [ ] Project created successfully

### Create Web App
- [ ] In Firebase Console, click "Add app"
- [ ] Select "Web"
- [ ] Register app as "JobAgent Web"
- [ ] Copy the config (6 values shown)
- [ ] Save these values somewhere safe

### Copy Your Credentials
You should now have these 6 values:
```
apiKey
authDomain
projectId
storageBucket
messagingSenderId
appId
```

- [ ] Copied all 6 values
- [ ] Values are correct (no typos)

---

## Phase 2: Enable Firebase Services (10 minutes)

### Enable Authentication
- [ ] Go to Authentication > Sign-in method
- [ ] Click "Email/Password"
- [ ] Enable it
- [ ] Optionally enable "Google" (requires Google Cloud setup)
- [ ] Authentication ready

### Create Firestore Database
- [ ] Go to Firestore Database
- [ ] Click "Create database"
- [ ] Choose "Production mode"
- [ ] Choose region closest to you
- [ ] Click "Create"
- [ ] Database created
- [ ] Copy the project ID (you'll need it)

### Create Cloud Storage
- [ ] Go to Storage
- [ ] Click "Get started"
- [ ] Choose "Production mode"
- [ ] Choose same region as Firestore
- [ ] Click "Done"
- [ ] Storage ready

---

## Phase 3: Set Security Rules (5 minutes)

### Firestore Security Rules
- [ ] Go to Firestore > Rules
- [ ] Copy paste the security rules from FIREBASE_SETUP.md
- [ ] Click "Publish"
- [ ] Wait for "Rules updated" message
- [ ] Rules published successfully

### Storage Security Rules
- [ ] Go to Storage > Rules
- [ ] Copy paste the security rules from FIREBASE_SETUP.md
- [ ] Click "Publish"
- [ ] Wait for "Rules updated" message
- [ ] Rules published successfully

---

## Phase 4: Local Environment Setup (5 minutes)

### Create `.env.local` File
- [ ] In project root, create file `.env.local`
- [ ] Add these 6 Firebase variables (from your copied credentials):
  ```
  NEXT_PUBLIC_FIREBASE_API_KEY=YOUR_API_KEY
  NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
  NEXT_PUBLIC_FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
  NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
  NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=YOUR_MESSAGING_SENDER_ID
  NEXT_PUBLIC_FIREBASE_APP_ID=YOUR_APP_ID
  ```
- [ ] Values are from your Firebase config
- [ ] No quotes around values
- [ ] No extra spaces

### Add Gemini API Key
- [ ] Go to https://aistudio.google.com/app/apikey
- [ ] Create API key
- [ ] Copy it
- [ ] Add to `.env.local`:
  ```
  GEMINI_API_KEY=YOUR_GEMINI_KEY
  ```
- [ ] Note: No `NEXT_PUBLIC_` prefix (server-side only)

### Verify `.env.local`
- [ ] File exists in project root
- [ ] All 7 variables present
- [ ] No typos in variable names
- [ ] No quotes around values
- [ ] File is in `.gitignore` (don't commit it)

---

## Phase 5: Local Testing (5 minutes)

### Start Development Server
- [ ] Open terminal in project root
- [ ] Run: `npm run dev`
- [ ] Wait for "Ready in X.Xs" message
- [ ] Open http://localhost:3000
- [ ] Landing page loads
- [ ] No console errors (F12 to check)

### Test Authentication
- [ ] Click "Sign Up" button
- [ ] Create test account with email
- [ ] Email verification sent (check console)
- [ ] Log in with credentials
- [ ] Dashboard loads
- [ ] Can see profile/settings

### Test Resume Upload
- [ ] In Settings, upload test resume (PDF or DOC)
- [ ] Upload completes
- [ ] File appears in storage
- [ ] Go to Firebase Console > Storage
- [ ] Resume visible in `/resumes/{your-uid}/`

### Test Chat Interface
- [ ] In Dashboard, go to Chat
- [ ] Type a test message
- [ ] AI responds (may use fallback if Gemini API down)
- [ ] Thinking animation shows
- [ ] No console errors

---

## Phase 6: Vercel Deployment (10 minutes)

### Push to GitHub
- [ ] Have GitHub account
- [ ] Create new repository
- [ ] Clone to local
- [ ] Copy project files (except .env.local and node_modules)
- [ ] Run: `git add .`
- [ ] Run: `git commit -m "Initial commit: JobAgent"`
- [ ] Run: `git push origin main`
- [ ] Code is on GitHub

### Connect Vercel
- [ ] Go to https://vercel.com/
- [ ] Sign in or create account
- [ ] Click "Add New Project"
- [ ] Select your GitHub repository
- [ ] Click "Import"
- [ ] Project imported to Vercel

### Add Environment Variables to Vercel
- [ ] In Vercel, go to Settings > Environment Variables
- [ ] Add all 7 variables (same as `.env.local`):
  - [ ] NEXT_PUBLIC_FIREBASE_API_KEY
  - [ ] NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
  - [ ] NEXT_PUBLIC_FIREBASE_PROJECT_ID
  - [ ] NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
  - [ ] NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
  - [ ] NEXT_PUBLIC_FIREBASE_APP_ID
  - [ ] GEMINI_API_KEY
- [ ] Each value correct and complete
- [ ] No typos in variable names

### Deploy
- [ ] Go to Deployments
- [ ] Click "Redeploy" on latest
- [ ] Wait for build to complete (2-5 minutes)
- [ ] "Deployment successful" message appears
- [ ] Click on deployment URL
- [ ] Site loads and works
- [ ] Can sign up and log in
- [ ] Chat responds
- [ ] No console errors

---

## Phase 7: Production Verification (5 minutes)

### Test Live Site
- [ ] Open your Vercel deployment URL
- [ ] Landing page loads fast
- [ ] All animations work
- [ ] Create test account with new email
- [ ] Verify email verification works
- [ ] Log in successfully
- [ ] Upload resume
- [ ] Test chat with AI
- [ ] Everything working

### Test All Features
- [ ] Landing page - loads, animations smooth
- [ ] Sign up - creates account, email works
- [ ] Login - can log back in
- [ ] Settings - can update profile
- [ ] Resume upload - file saved to Firebase
- [ ] Chat interface - responds to messages
- [ ] Dark theme - works on all pages
- [ ] Mobile - responsive on phone/tablet

### Check for Errors
- [ ] Open browser DevTools (F12)
- [ ] Console tab - no red errors
- [ ] Network tab - no failed requests
- [ ] Performance tab - loads fast

---

## Phase 8: Final Checks

### Domain (Optional)
- [ ] If you have custom domain, configure in Vercel
- [ ] Or use free `your-project.vercel.app` URL
- [ ] Domain/URL works

### Share (Optional)
- [ ] Copy your site URL
- [ ] Send to friends/family
- [ ] Get feedback
- [ ] Make improvements

### Customize (Optional)
- [ ] Change colors in `/app/globals.css`
- [ ] Update copy in components
- [ ] Add your branding
- [ ] Deploy again with `git push`

---

## Troubleshooting During Setup

### "env.local not found"
- [ ] Check file is in project root (not subfolder)
- [ ] Check filename is exactly `.env.local`
- [ ] Restart dev server after creating file

### "Cannot find module firebase"
- [ ] Run: `npm install firebase`
- [ ] Wait for install to complete
- [ ] Restart dev server

### "Firebase initialization failed"
- [ ] Check all 6 Firebase variables in `.env.local`
- [ ] Check no typos (exact match required)
- [ ] Check values have no extra spaces
- [ ] Restart dev server

### "GEMINI_API_KEY is undefined"
- [ ] Verify it's in `.env.local` (not `.env`)
- [ ] Check spelling: `GEMINI_API_KEY` (exact)
- [ ] No `NEXT_PUBLIC_` prefix
- [ ] Restart dev server

### "Deployment fails on Vercel"
- [ ] Check all 7 variables in Vercel Environment Variables
- [ ] Check values match `.env.local`
- [ ] Trigger redeploy (not just relying on auto-deploy)
- [ ] Check Vercel deployment logs for errors

---

## Success Signs

You've succeeded when:
- ✅ Local dev server runs without errors
- ✅ Can create account and log in
- ✅ Resume uploads to Firebase Storage
- ✅ Chat interface works with AI
- ✅ Vercel deployment completed
- ✅ Live site works end-to-end
- ✅ All animations are smooth
- ✅ No console errors

---

## Total Time Required

| Phase | Time | Notes |
|-------|------|-------|
| 1. Firebase Setup | 15 min | One-time setup |
| 2. Enable Services | 10 min | Quick toggles |
| 3. Security Rules | 5 min | Copy/paste |
| 4. Env Variables | 5 min | Copy credentials |
| 5. Local Testing | 5 min | Verify everything |
| 6. Vercel Deploy | 10 min | GitHub + Vercel |
| 7. Final Tests | 5 min | Verify live site |
| **TOTAL** | **55 min** | From start to live |

---

## Need Help?

| Problem | Solution |
|---------|----------|
| Firebase errors | Read FIREBASE_SETUP.md |
| Other errors | Read TROUBLESHOOTING.md |
| Setup questions | Read SETUP_GUIDE.md |
| Security questions | Read SECURITY.md |
| Can't find something | Check DOCS_INDEX.md |

---

## What's Next After Setup?

Once everything is working:

1. **Customize:**
   - Change colors in globals.css
   - Update text/copy
   - Add your branding

2. **Enhance:**
   - Add more AI capabilities
   - Improve form detection
   - Add more job boards

3. **Share:**
   - Tell friends/family
   - Get user feedback
   - Iterate based on feedback

4. **Scale:**
   - Add more features
   - Optimize performance
   - Expand functionality

---

## Quick Reference

### Essential Files to Know
- `.env.local` - Your secrets (don't commit)
- `app/page.tsx` - Landing page
- `app/register/page.tsx` - Signup form
- `components/chat/ChatInterface.tsx` - AI chat
- `lib/firebase.ts` - Firebase config
- `app/actions/gemini.ts` - AI processing

### Essential URLs
- Firebase Console: https://console.firebase.google.com/
- Google AI Studio: https://aistudio.google.com/app/apikey
- Vercel Dashboard: https://vercel.com/
- Your Site: https://your-project.vercel.app/

### Essential Commands
```bash
npm install      # Install dependencies
npm run dev      # Start dev server
npm run build    # Build for production
npm start        # Start production server
```

---

## Checklist Complete! 🎉

When you finish this checklist:
- ✅ Firebase project created
- ✅ All services enabled
- ✅ Security rules set
- ✅ Environment variables configured
- ✅ Local testing passed
- ✅ Deployed to Vercel
- ✅ Live site verified

**Your AI-powered job automation platform is ready to use!**

---

**Next Step:** Start the checklist from Phase 1!

Questions? Check the documentation files above or re-read this guide.
