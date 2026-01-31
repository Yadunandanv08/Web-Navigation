# JobAgent Setup Guide

## Quick Start

JobAgent is an AI-powered job application automation platform built with React, Tailwind CSS, and Firebase.

### Features Included:
✅ Stunning animated landing page
✅ Google Sign-In & Email Authentication
✅ Job application registration form with resume upload
✅ AI-powered chat interface with Gemini
✅ Thinking animation (like Google Gemini)
✅ Form filling automation agent
✅ Resume management & profile settings
✅ Application tracking dashboard
✅ Responsive design with smooth animations

---

## Environment Variables Setup

Add these to your Vercel project in the `Settings > Environment Variables` section:

### Firebase Configuration
Get these from your [Firebase Console](https://console.firebase.google.com/):

```
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### Gemini API Configuration
Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey):

```
GEMINI_API_KEY=your_gemini_api_key
```

⚠️ **Important:** Use `GEMINI_API_KEY` (no `NEXT_PUBLIC_` prefix)
- This keeps your API key private and secure
- Never exposed to the browser
- Handled via secure server actions

---

## Firebase Setup

For detailed Firebase setup instructions, see **[FIREBASE_SETUP.md](./FIREBASE_SETUP.md)**.

Quick steps:
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project called "JobAgent"
3. Add a Web app
4. Copy the config to `.env.local` (or Vercel environment variables)
5. Enable Authentication (Email/Password + optional Google)
6. Create Firestore Database (Production mode)
7. Create Storage bucket (Production mode)
8. Apply the provided Security Rules

See **[FIREBASE_SETUP.md](./FIREBASE_SETUP.md)** for complete step-by-step instructions.

---

## Google Sign-In Setup

1. In Firebase Console, go to Authentication > Sign-in method
2. Enable Google provider
3. Add your domain to authorized domains
4. The app will automatically handle OAuth redirects

---

## Page Routes

### Public Pages:
- `/` - Landing page with features and CTA
- `/login` - Email login & Google Sign-In
- `/register` - Registration with job questionnaire

### Protected Pages (require login):
- `/dashboard` - Main chat interface with AI agent
- `/dashboard/settings` - Profile & resume management
- `/dashboard/applications` - Track submitted applications

---

## How to Use

### For Job Seekers:
1. Sign up with email or Google
2. Complete your profile on settings page
3. Upload your resume
4. Go to dashboard and chat with the AI agent
5. Provide job form URLs (Google Forms, company websites, etc.)
6. The agent will fill forms automatically using your resume
7. Track your applications

### For Developers:
- All components use Tailwind CSS for styling
- Dark theme is enabled by default
- Custom animations defined in `globals.css`
- Firebase integration in `lib/firebase.ts`
- Gemini API integration in `lib/gemini.ts`
- Auth context in `context/AuthContext.tsx`

---

## Customization Tips

### Change Brand Colors:
Edit the design tokens in `/app/globals.css` in the `:root` and `.dark` sections.

### Add More AI Features:
- Extend `lib/gemini.ts` with new prompts
- Modify chat system prompt in `geminiService.createSystemPrompt()`
- Add new message types to `ChatMessage.tsx`

### Styling Components:
- Use existing shadcn/ui components in `/components/ui`
- Follow Tailwind utility-first approach
- Check color tokens for consistency

---

## Deployment

1. Push to GitHub
2. Connect to Vercel
3. Add environment variables in Vercel Settings
4. Deploy!

The app is optimized for Vercel with Next.js 16, React 19, and streaming responses.

---

## Troubleshooting

**Firebase Auth not working:**
- Check CORS settings in Firebase Console
- Verify authorized domains
- Ensure environment variables are set

**Gemini API errors:**
- Check your API key is valid
- Verify quota limits
- Check browser console for detailed errors

**Resume upload not working:**
- Check Firebase Storage permissions
- Ensure Storage bucket is created
- Check file size limits

---

## Support

For issues:
1. Check the `.env.example` file for required variables
2. Review Firebase Console settings
3. Check browser DevTools console for errors
4. Verify all environment variables are properly set

Enjoy automating your job applications! 🚀
