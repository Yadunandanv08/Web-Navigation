# JobAgent - AI-Powered Job Application Automation

An amazing, animated frontend platform that automates job applications using AI. Fill forms, upload resumes, and apply to jobs instantly with our intelligent agent.

## Overview

JobAgent is a cutting-edge web application that harnesses the power of Google's Gemini AI to automate job application processes. With a stunning animated interface and ChatGPT-like chat experience, users can provide job form URLs or direct application links, and the AI agent automatically fills them out using the user's resume and profile information.

## Key Features

🎨 **Stunning Animated UI**
- Modern dark theme with glassmorphism design
- Smooth animations and transitions throughout
- Responsive design that works on all devices
- Beautiful gradient accents and interactive elements

🤖 **AI-Powered Form Filling**
- Google Gemini AI integration
- Thinking animations (like Google Gemini)
- Automatic form detection and filling
- Support for multiple form types:
  - Google Forms
  - Custom HTML forms
  - LinkedIn/Indeed style forms
  - Text-based questionnaires

🔐 **Authentication & Security**
- Firebase Authentication
- Google Sign-In support
- Email/password authentication
- Secure session management

📄 **Resume Management**
- Upload and store multiple resumes
- Auto-fill forms with resume data
- Profile management dashboard
- Application tracking

💬 **ChatGPT-Like Interface**
- Real-time chat with AI agent
- Message history and context
- Typing indicators
- Beautiful message UI

📊 **Application Dashboard**
- Track submitted applications
- View submission history
- Application status tracking
- Analytics and insights

## Tech Stack

- **Frontend**: React 19 with Next.js 16
- **Styling**: Tailwind CSS v4 with custom animations
- **AI**: Google Gemini API
- **Backend**: Firebase (Auth, Firestore, Storage)
- **Deployment**: Optimized for Vercel

## Installation

### 1. Clone and Install
```bash
git clone <your-repo>
cd jobagent
npm install
```

### 2. Set Up Firebase
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable these services:
   - Authentication (Email/Password + Google)
   - Cloud Firestore
   - Cloud Storage
4. Copy your Firebase config

### 3. Get Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 4. Configure Environment Variables
Create a `.env.local` file:
```
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Authorize Domains for Google Sign-In
To use Google Sign-In, you must authorize your domain:
- See **[GOOGLE_AUTH_DOMAINS_FIX.md](./GOOGLE_AUTH_DOMAINS_FIX.md)** for step-by-step instructions
- Add `localhost:3000` for local development
- Add your Vercel domain for production

### 6. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

## Project Structure

```
/app
  ├── page.tsx              # Landing page
  ├── login/page.tsx        # Login page
  ├── register/page.tsx     # Registration page
  └── dashboard/
      ├── page.tsx          # Main dashboard
      ├── settings/page.tsx # Profile & resume
      └── applications/     # Application tracking

/components
  ├── landing/              # Landing page components
  ├── chat/                 # Chat interface components
  ├── dashboard/            # Dashboard components
  └── ui/                   # Reusable UI components

/lib
  ├── firebase.ts          # Firebase config
  ├── gemini.ts            # Gemini API integration
  └── utils.ts             # Utility functions

/context
  └── AuthContext.tsx      # Auth provider

/styles
  └── globals.css          # Global styles & animations
```

## Page Routes

### Public Pages
- `/` - Landing page
- `/login` - Sign in page
- `/register` - Registration with questionnaire

### Protected Pages (Login Required)
- `/dashboard` - AI chat interface
- `/dashboard/settings` - Profile management
- `/dashboard/applications` - Track applications

## Component Highlights

### AnimatedHeader
Gradient animated header with smooth transitions and navigation links.

### HeroSection
Eye-catching hero with animated text and call-to-action buttons.

### ThinkingAnimation
Google Gemini-style thinking animation with bouncing dots.

### ChatInterface
ChatGPT-like interface with:
- Message history
- File uploads
- Thinking state
- Response streaming

### DashboardHeader & DashboardSidebar
Navigation components for the protected dashboard area.

## Customization

### Change Colors
Edit the design tokens in `/app/globals.css`:
```css
:root {
  --primary: oklch(0.6 0.25 272); /* Change this for brand color */
  --accent: oklch(0.65 0.3 50);   /* Change for accent */
  /* ... more tokens ... */
}
```

### Add More AI Prompts
Edit `/lib/gemini.ts` and update the `createSystemPrompt()` method:
```typescript
createSystemPrompt() {
  return `You are an expert job application filler...`
}
```

### Modify Animations
Add/edit animations in `/app/globals.css`:
```css
@keyframes custom-animation {
  /* Your animation here */
}
```

## Features Explained

### AI Form Filling Agent
The agent receives:
1. Job form URL or form data
2. User's resume content
3. User's profile information

It then:
1. Analyzes the form structure
2. Extracts required fields
3. Matches data from resume
4. Fills form intelligently
5. Provides next steps

### Thinking Animation
Shows when AI is processing:
- Loading state with animated dots
- Smooth fade-in for responses
- Indicates "AI is thinking"

### Resume Management
Users can:
- Upload multiple resume versions
- Set primary resume
- View upload history
- Download resumes

## Security Features

- Firebase Authentication for user security
- Cloud Storage for encrypted resume storage
- **Gemini API key kept server-side only** (never exposed to client)
- Server Actions for secure API calls
- Environment variables for sensitive data
- Firebase Security Rules for data protection
- CORS configuration for API security
- HTTPS everywhere (Vercel automatic)
- No sensitive data stored client-side

See **[SECURITY.md](./SECURITY.md)** for detailed security information.

## Performance

- Optimized for Vercel edge network
- Lazy loading for images and components
- CSS-in-JS optimization
- Efficient state management
- Streaming API responses

## Deployment

### Deploy to Vercel

1. Push to GitHub
```bash
git push origin main
```

2. Connect to Vercel
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Add environment variables in settings

3. Deploy
```bash
npm run build
npm run start
```

### Environment Variables in Vercel
1. Go to Project Settings > Environment Variables
2. Add all variables from `.env.example`
3. Redeploy to apply changes

## Troubleshooting

### Firebase Not Loading
- Check Firebase config in environment variables
- Verify CORS settings
- Clear browser cache

### Gemini API Errors
- Verify API key is valid
- Check API quota limits
- Review API documentation

### Resume Upload Fails
- Check Firebase Storage permissions
- Verify bucket exists
- Check file size (max 10MB recommended)

### Chat Not Working
- Verify Gemini API key
- Check network tab for errors
- Review browser console

## Future Enhancements

- [ ] Multi-language support
- [ ] Email notifications for applications
- [ ] Job board integration APIs
- [ ] Advanced form parsing
- [ ] Interview preparation coaching
- [ ] Cover letter generation
- [ ] Job matching algorithm
- [ ] Team collaboration features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project

## Support

For issues or questions:
1. Check the [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Review error messages in browser console
3. Verify all environment variables are set
4. Check Firebase and Gemini documentation

## Authors

Built with Next.js 16, React 19, and powered by Google Gemini AI.

---

**Ready to revolutionize job hunting?** Deploy JobAgent now and start automating your applications! 🚀
