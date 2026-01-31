# JobAgent - Start Here 🚀

Welcome to **JobAgent**, your AI-powered job application automation platform!

## What You've Got

A fully-featured, beautifully animated web application that:
- ✨ Automates job applications with AI
- 🤖 Uses Google Gemini for intelligent form filling
- 💬 Provides a ChatGPT-like interface
- 🎨 Features stunning animations and dark theme
- 🔐 Includes user authentication with Google Sign-In
- 📄 Manages resumes and job applications
- 📊 Tracks application history

---

## Quick Setup (5 minutes)

### 1. Get Your API Keys

**Firebase:**
- Visit [Firebase Console](https://console.firebase.google.com/)
- Create a new project
- Go to Project Settings
- Copy: API Key, Auth Domain, Project ID, Storage Bucket, Messaging Sender ID, App ID

**Gemini:**
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Click "Create API key"
- Copy your API key

### 2. Add Environment Variables

In your Vercel Project Settings > Environment Variables, add:

```
NEXT_PUBLIC_FIREBASE_API_KEY=your_key_here
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
NEXT_PUBLIC_GEMINI_API_KEY=your_gemini_key_here
```

### 3. Deploy

Push to GitHub and Vercel will auto-deploy, or use the Deploy button in Vercel.

---

## Explore the App

### 🏠 Landing Page (`/`)
Beautiful welcome page with features showcase

### 🔑 Authentication (`/login` & `/register`)
- Sign up with email or Google
- Complete job questionnaire
- Upload your resume

### 💬 Dashboard (`/dashboard`)
Main chat interface:
1. Share a job form URL or Google Form link
2. Chat with the AI agent
3. Watch the thinking animation
4. AI automatically fills the form
5. Application gets tracked

### ⚙️ Settings (`/dashboard/settings`)
- Manage your profile
- Upload/manage resumes
- View job preferences

### 📋 Applications (`/dashboard/applications`)
- See all submitted applications
- Track submission dates
- Review form URLs

---

## File Guide

| File | Purpose |
|------|---------|
| `/README.md` | Complete documentation |
| `/QUICKSTART.md` | Quick setup checklist |
| `/SETUP_GUIDE.md` | Detailed setup instructions |
| `/DEPLOYMENT.md` | How to deploy to production |
| `/PROJECT_STRUCTURE.md` | Code organization guide |
| `/app/page.tsx` | Landing page code |
| `/app/login/page.tsx` | Login page code |
| `/app/register/page.tsx` | Registration page code |
| `/app/dashboard/page.tsx` | Main chat interface |
| `/components/chat/ChatInterface.tsx` | Chat component |
| `/lib/firebase.ts` | Firebase setup |
| `/lib/gemini.ts` | Gemini AI service |
| `/context/AuthContext.tsx` | Authentication context |
| `/app/globals.css` | Theme & animations |

---

## Key Features Explained

### 🎨 Animations
Every page has smooth animations:
- Gradient text shifts
- Thinking pulse when AI processes
- Smooth fade-ins and slides
- All defined in `/app/globals.css`

### 🤖 AI Form Filling
1. User provides job form URL
2. Gemini analyzes the form
3. Extracts fields needed
4. Matches data from user's resume
5. Auto-fills form intelligently
6. Shows thinking animation while processing

### 🔐 Security
- Firebase authentication (email & Google)
- Secure resume storage in Cloud Storage
- User-specific data access with Firestore rules
- Environment variables never exposed

### 📱 Responsive Design
Works beautifully on:
- Desktop (full features)
- Tablet (optimized layout)
- Mobile (touch-friendly)

---

## Customization Options

### Change Theme Colors
Edit `/app/globals.css`:
```css
:root {
  --primary: oklch(0.6 0.25 272); /* Change purple to your color */
  --accent: oklch(0.65 0.3 50);   /* Change gold/amber */
}
```

### Modify AI Behavior
Edit `/lib/gemini.ts`:
- Update `createSystemPrompt()` for different AI instructions
- Customize form analysis logic
- Adjust response formatting

### Add More Animations
Edit `/app/globals.css`:
- Add new `@keyframes` in `@layer utilities`
- Apply to components with utility classes

### Change Text & Copy
- Update headlines in component files
- Modify prompts in `/lib/gemini.ts`
- Edit form labels in page files

---

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# Open http://localhost:3000

# Build for production
npm run build

# Run production build locally
npm run start

# Lint code
npm run lint
```

---

## Architecture Overview

```
User Interface (React Components)
    ↓
Chat Interface (ChatInterface.tsx)
    ↓
Gemini API Service (gemini.ts)
    ↓
Google Gemini AI
    ↓
Response → Display with animations
    ↓
Firebase Storage (Save results)
```

---

## Troubleshooting

### App Won't Load
- Check browser console for errors
- Verify all env vars are set in Vercel
- Clear browser cache
- Check network tab for failed requests

### Firebase Issues
- Add your Vercel domain to Firebase authorized domains
- Verify Firebase services are enabled (Auth, Firestore, Storage)
- Check Firebase security rules

### Gemini API Errors
- Verify API key is correct in Vercel env vars
- Check API quota limits
- Review browser console for specific errors

### Resume Upload Fails
- Check file size (keep under 10MB)
- Verify Firebase Storage is enabled
- Check storage security rules allow uploads

---

## Next Steps

1. **Review** - Read through the documentation files
2. **Customize** - Change colors, text, animations to match your brand
3. **Test** - Try uploading a resume and using the AI chat
4. **Deploy** - Push to production when ready
5. **Iterate** - Get feedback and improve features

---

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Firebase Docs](https://firebase.google.com/docs)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini API Docs](https://ai.google.dev/docs)

---

## Getting Help

1. Check the `/README.md` for full documentation
2. Read `/SETUP_GUIDE.md` for detailed setup
3. Review `/PROJECT_STRUCTURE.md` to understand code organization
4. Check browser DevTools console for error messages
5. Visit documentation links above

---

## You're All Set! 🎉

Your JobAgent platform is ready to revolutionize job hunting. The code is clean, well-documented, and ready to customize.

**Next: Start with `/QUICKSTART.md` or go straight to `/README.md` for full details.**

Happy coding! 🚀
