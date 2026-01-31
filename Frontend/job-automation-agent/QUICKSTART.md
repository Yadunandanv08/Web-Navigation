# JobAgent - Quick Start Checklist

## Pre-Launch Setup (5 minutes)

### Step 1: Get Your API Keys
- [ ] Firebase API Key (from [Firebase Console](https://console.firebase.google.com/))
- [ ] Gemini API Key (from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Step 2: Set Environment Variables
In your Vercel Project Settings > Environment Variables, add:

```
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID
NEXT_PUBLIC_GEMINI_API_KEY
```

See `.env.example` for exact format.

### Step 3: Deploy
```bash
npm run build
npm run start
```

Or deploy to Vercel with a single click.

## First Time User Flow

1. **Visit landing page** (`/`)
   - See amazing animations
   - Read features
   - Click "Get Started"

2. **Sign up** (`/register`)
   - Email or Google Sign-In
   - Fill job questionnaire
   - Upload resume

3. **Complete profile** (`/dashboard/settings`)
   - Add more details
   - Manage resumes
   - View profile

4. **Start using AI** (`/dashboard`)
   - Chat with agent
   - Share job URLs
   - Let AI fill forms

5. **Track applications** (`/dashboard/applications`)
   - See submitted apps
   - View history
   - Get insights

## Key Files Structure

```
Landing Page
├── Components: AnimatedHeader, HeroSection, FeaturesSection
└── Route: /

Authentication
├── Login: /login
├── Register: /register (with questionnaire)
└── Context: AuthContext.tsx (handles Firebase Auth)

Protected Dashboard
├── Main Chat: /dashboard
├── Settings: /dashboard/settings (resume upload)
├── Applications: /dashboard/applications
└── Components: ChatInterface, DashboardHeader, DashboardSidebar

AI Integration
├── Gemini Service: lib/gemini.ts
├── Thinking Animation: components/chat/ThinkingAnimation.tsx
└── Chat Component: components/chat/ChatInterface.tsx

Firebase Integration
├── Config: lib/firebase.ts
├── Auth Provider: context/AuthContext.tsx
└── Storage: Resumes stored in Firebase Cloud Storage
```

## Environment Variables Quick Reference

### Firebase (Copy from Firebase Console > Project Settings)
- `NEXT_PUBLIC_FIREBASE_API_KEY` - API Key
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` - Your_ProjectID.firebaseapp.com
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID` - Your project ID
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` - Your_ProjectID.appspot.com
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` - Sender ID
- `NEXT_PUBLIC_FIREBASE_APP_ID` - App ID

### Gemini
- `NEXT_PUBLIC_GEMINI_API_KEY` - Your Gemini API Key from Google AI Studio

## Features by Page

### Landing Page (/)
- Animated gradient header
- Hero section with CTA
- Features showcase
- Responsive design

### Login (/login)
- Email/password login
- Google Sign-In button
- Forgot password link
- Register link

### Register (/register)
- Sign up form
- Job application questionnaire
- Resume upload
- Profile completion

### Dashboard (/dashboard)
- ChatGPT-like interface
- AI agent for form filling
- Thinking animations
- Message history
- File attachment support

### Settings (/dashboard/settings)
- Profile management
- Resume upload/management
- Job preferences
- Account settings

### Applications (/dashboard/applications)
- Application history
- Status tracking
- Date submitted
- Form URL reference

## Customization Options

### Change Brand Colors
Edit `/app/globals.css` - look for `:root` and `.dark` sections

### Modify AI Behavior
Edit `/lib/gemini.ts` - update `createSystemPrompt()`

### Add Custom Animations
Edit `/app/globals.css` - add `@keyframes` in @layer utilities

### Change Theme
Already set to dark mode. To add light mode support:
1. Extend globals.css with light mode tokens
2. Add theme toggle in DashboardHeader

## Common Issues & Solutions

### Issue: Blank page on load
**Solution**: Check browser console for errors. Verify all env vars are set.

### Issue: Can't sign up
**Solution**: Enable Email/Password auth in Firebase Console

### Issue: Google Sign-In not working
**Solution**: Add authorized domain in Firebase Console

### Issue: Gemini API errors
**Solution**: Check API key validity and quota limits

### Issue: Resume upload fails
**Solution**: Verify Firebase Storage is enabled and configured

### Issue: Chat is slow
**Solution**: Check network tab. Verify Gemini API key and quota.

## Next Steps

1. Review SETUP_GUIDE.md for detailed configuration
2. Read README.md for full documentation
3. Customize colors and branding
4. Deploy to Vercel
5. Add more custom AI prompts
6. Implement email notifications
7. Add job board integrations

## Testing Checklist

- [ ] Landing page loads with animations
- [ ] Google Sign-In works
- [ ] Email registration works
- [ ] Resume upload works
- [ ] Chat interface responds
- [ ] Thinking animation appears
- [ ] Application tracking shows submissions
- [ ] Logout works properly
- [ ] Mobile responsive
- [ ] Dark mode looks good

## Deployment Checklist

- [ ] All env vars set in Vercel
- [ ] Firebase configured
- [ ] Gemini API key valid
- [ ] npm run build succeeds
- [ ] No console errors
- [ ] All routes accessible after login
- [ ] Resume upload functional
- [ ] Chat responding

## Need Help?

1. Check SETUP_GUIDE.md for detailed setup
2. Review README.md for feature documentation
3. Check .env.example for required variables
4. Look at console.log messages in browser DevTools
5. Verify Firebase settings in Console

---

**You're all set!** Your amazing JobAgent platform is ready to revolutionize job hunting. 🚀
