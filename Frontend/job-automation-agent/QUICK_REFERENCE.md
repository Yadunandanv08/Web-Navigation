# JobAgent - Quick Reference Card

Print this or keep it handy! One-page reference for common tasks.

---

## 📍 Important URLs

```
Landing:  https://jobagent.vercel.app/
Login:    https://jobagent.vercel.app/login
Register: https://jobagent.vercel.app/register
Dashboard: https://jobagent.vercel.app/dashboard
Settings: https://jobagent.vercel.app/dashboard/settings
Apps:     https://jobagent.vercel.app/dashboard/applications
```

---

## 🔑 Required Environment Variables

```
NEXT_PUBLIC_FIREBASE_API_KEY=[from Firebase Console]
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=[your-project].firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=[your-project-id]
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=[your-project].appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=[sender-id-number]
NEXT_PUBLIC_FIREBASE_APP_ID=[app-id]
NEXT_PUBLIC_GEMINI_API_KEY=[from Google AI Studio]
```

---

## 🚀 Development Commands

```bash
npm install              # Install dependencies
npm run dev             # Start dev server (localhost:3000)
npm run build           # Build for production
npm run start           # Run production build
npm run lint            # Check code quality
```

---

## 🔗 Important Links

| Service | Link | Purpose |
|---------|------|---------|
| Firebase Console | firebase.google.com | Auth, Database, Storage |
| Google AI Studio | aistudio.google.com/app/apikey | Get Gemini API key |
| Vercel Dashboard | vercel.com | Deploy & manage |
| Next.js Docs | nextjs.org/docs | Framework docs |
| Tailwind CSS | tailwindcss.com | Styling framework |
| Shadcn/UI | ui.shadcn.com | UI components |

---

## 📁 Key Files Quick Guide

| File | What to Edit |
|------|--------------|
| `/app/globals.css` | Colors, animations, theme |
| `/lib/gemini.ts` | AI behavior & prompts |
| `/app/page.tsx` | Landing page content |
| `/app/login/page.tsx` | Login page text |
| `/app/register/page.tsx` | Registration form |
| `/components/landing/*` | Landing page sections |
| `/context/AuthContext.tsx` | Auth logic |
| `/lib/firebase.ts` | Firebase config |

---

## 🎨 Common Customizations

### Change Primary Color
```css
/* In /app/globals.css */
:root {
  --primary: oklch(0.6 0.25 272); /* Change this */
}
```

### Change Accent Color
```css
:root {
  --accent: oklch(0.65 0.3 50); /* Change this */
}
```

### Update Hero Text
```tsx
// In /components/landing/HeroSection.tsx
const title = "Your new title here";
```

### Change AI System Prompt
```typescript
// In /lib/gemini.ts - createSystemPrompt() method
return `You are an expert job filler...`
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Blank page | Check browser console for errors |
| Firebase fail | Verify env vars in Vercel Settings |
| No auth | Add domain to Firebase authorized domains |
| API errors | Check API key in env vars |
| Resume won't upload | Check file size < 10MB, enable Storage |
| Slow chat | Check Gemini API quota limits |

---

## ✅ Deployment Checklist

- [ ] All env vars set in Vercel Settings
- [ ] Firebase services enabled (Auth, Firestore, Storage)
- [ ] Gemini API key valid
- [ ] Domain added to Firebase authorized domains
- [ ] npm run build succeeds
- [ ] No console errors
- [ ] Test signup/login
- [ ] Test resume upload
- [ ] Test chat interface
- [ ] Test on mobile

---

## 📊 Architecture Quick View

```
Frontend (React)
    ↓
Chat Interface
    ↓
Gemini API
    ↓
Form Analysis & Filling
    ↓
Firebase (Auth + Storage + DB)
```

---

## 🎯 Common Tasks

**Add a new page:**
```
1. Create /app/[route]/page.tsx
2. Add navigation link
3. Import components as needed
```

**Add animation:**
```
1. Add @keyframes in /app/globals.css
2. Add utility class
3. Use class in component
```

**Change text:**
- Find in component file
- Update string
- Rebuild

**Add new form field:**
1. Update registration page
2. Update Firebase schema
3. Update display in settings

**Deploy changes:**
```
git add .
git commit -m "message"
git push origin main
# Vercel auto-deploys!
```

---

## 🔐 Security Checklist

- [ ] Never commit .env files
- [ ] Use env vars in Vercel Settings only
- [ ] Keep API keys private
- [ ] Use HTTPS everywhere
- [ ] Enable Firebase security rules
- [ ] Validate all user inputs
- [ ] Rotate keys monthly
- [ ] Monitor Firebase usage

---

## 💾 Local Development Setup

```bash
# 1. Clone repo
git clone [your-repo]
cd jobagent

# 2. Install
npm install

# 3. Create .env.local
cp .env.example .env.local
# Fill in your values

# 4. Start dev server
npm run dev

# 5. Open browser
# localhost:3000
```

---

## 🌐 Deployment to Vercel

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to vercel.com
# Click "Import Project"
# Select your repo

# 3. Add Environment Variables
# Settings > Environment Variables
# Add all from .env.example

# 4. Deploy!
# Click Deploy
# Wait 2-5 minutes
# Your app is live!
```

---

## 📱 Test Checklist

- [ ] Desktop (Chrome, Firefox, Safari)
- [ ] Mobile (iOS, Android)
- [ ] Tablet
- [ ] Login flow
- [ ] Registration flow
- [ ] Resume upload
- [ ] Chat interface
- [ ] Thinking animation
- [ ] Logout
- [ ] Dark mode
- [ ] Responsive design

---

## 🚨 Emergency Fixes

**App won't load:**
```
1. Check browser console (F12)
2. Verify env vars in Vercel
3. Clear browser cache
4. Hard refresh (Ctrl+Shift+R)
```

**Can't login:**
```
1. Check Firebase is enabled
2. Verify domain in Firebase
3. Check auth error message
4. Review Firebase logs
```

**API not working:**
```
1. Verify API key in env vars
2. Check quota/limits
3. Review API response in DevTools
4. Check network connection
```

---

## 📞 Support Resources

| Resource | Use For |
|----------|---------|
| Browser Console | Debug errors |
| Vercel Dashboard | Check builds/logs |
| Firebase Console | Check services |
| Google AI Studio | Check API quota |
| Documentation files | Reference |
| Next.js docs | Framework help |

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Initial setup | 5-10 min |
| Firebase config | 10-15 min |
| Gemini API setup | 5 min |
| Deploy to Vercel | 5 min |
| First form fill | 2 min |
| Customize colors | 10 min |
| Full customization | 2-4 hours |

---

## 🎊 Success Indicators

- ✓ App loads at your Vercel URL
- ✓ Can sign up/login
- ✓ Can upload resume
- ✓ AI chat responds
- ✓ Thinking animation appears
- ✓ Forms fill automatically
- ✓ No console errors
- ✓ Mobile responsive
- ✓ Fast loading times

---

## 🆘 When Stuck

1. **Check errors** → Browser console (F12)
2. **Check docs** → Look in DOCS_INDEX.md
3. **Check code** → See similar components
4. **Check Firebase** → Console for logs
5. **Check API** → Verify quota limits
6. **Check deployment** → Vercel build logs
7. **Restart** → `npm run dev` again
8. **Clear cache** → Hard refresh browser

---

**Print this card or bookmark this page!**

For detailed info, see DOCS_INDEX.md to find what you need.

Good luck! 🚀
