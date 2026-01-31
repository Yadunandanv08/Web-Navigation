# JobAgent - Deployment Guide

## Deploy to Vercel (Recommended - 2 minutes)

### Option 1: One-Click Deploy
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click "New Project"
4. Select your GitHub repository
5. Vercel will automatically detect it's a Next.js project
6. Click "Deploy"
7. Go to Project Settings > Environment Variables
8. Add all variables from `.env.example`
9. Redeploy the project
10. Done! Your app is live

### Option 2: Deploy via GitHub Integration
1. Connect your GitHub account to Vercel
2. Vercel auto-deploys on every push to main
3. Add environment variables in Project Settings
4. Each commit automatically redeploys

## Environment Variables Setup

In Vercel Project Settings > Environment Variables, add:

### Firebase Variables
```
NEXT_PUBLIC_FIREBASE_API_KEY: [Your Firebase API Key]
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN: [your-project].firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID: [your-project-id]
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET: [your-project].appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID: [sender-id]
NEXT_PUBLIC_FIREBASE_APP_ID: [app-id]
```

### Gemini API Variable
```
NEXT_PUBLIC_GEMINI_API_KEY: [Your Gemini API Key]
```

All variables must be `NEXT_PUBLIC_*` to be available in the browser.

## Firebase Setup for Production

### Create Production Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a new project"
3. Name: "JobAgent" (or your choice)
4. Accept terms and create

### Enable Authentication

1. Go to Authentication > Sign-in method
2. Enable "Email/Password"
3. Enable "Google"
4. Add authorized domains:
   - your-domain.vercel.app
   - localhost:3000 (for testing)
5. Copy your credentials to `.env.example`

### Set Up Firestore Database

1. Go to Build > Firestore Database
2. Click "Create database"
3. Start in **Test mode** (you can secure later)
4. Choose closest location
5. Click "Enable"

### Set Up Cloud Storage

1. Go to Build > Storage
2. Click "Get started"
3. Start in **Test mode**
4. Choose same location as Firestore
5. Click "Done"

### Security Rules (Important!)

Update Firestore Security Rules:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    match /applications/{appId} {
      allow read, write: if request.auth.uid == resource.data.userId;
    }
  }
}
```

Update Storage Security Rules:
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /resumes/{userId}/{file=**} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

## Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API key"
3. Select your Google Cloud project
4. Copy the key
5. Add to environment variables

## Domain Configuration

### Custom Domain (Optional)

1. In Vercel Dashboard > Project > Settings > Domains
2. Add your custom domain
3. Follow DNS setup instructions
4. Add domain to Firebase authorized domains
5. Update your website references

### Default Vercel Domain

Your app automatically gets a free `.vercel.app` domain:
- Main: `jobagent.vercel.app`
- Preview: `jobagent-<branch>.vercel.app`
- Production: `jobagent-main.vercel.app`

## Local Development Before Deploying

```bash
# Install dependencies
npm install

# Set up .env.local with your development Firebase config
# Copy from .env.example and fill in your values

# Run development server
npm run dev

# Build for production
npm run build

# Test production build
npm run start
```

## Post-Deployment Checklist

- [ ] App loads at your Vercel URL
- [ ] Landing page shows animations
- [ ] Google Sign-In works
- [ ] Email registration works
- [ ] Resume upload works (check Firebase Storage)
- [ ] Chat interface responds
- [ ] Thinking animation appears
- [ ] No console errors
- [ ] Mobile version responsive
- [ ] Dark mode displays correctly

## Troubleshooting Deployment

### Issue: Blank Page
- Check browser console for errors
- Verify all env vars are set in Vercel Settings
- Check Network tab for failed requests
- Ensure Firebase config is correct

### Issue: Firebase Auth Fails
- Add your Vercel domain to Firebase authorized domains
- Verify `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` is set correctly
- Check Firebase Console > Authentication settings
- Clear browser cookies and try again

### Issue: Gemini API Not Working
- Verify `NEXT_PUBLIC_GEMINI_API_KEY` is set
- Check API quota in Google AI Studio
- Ensure API key has necessary permissions
- Review browser console for specific errors

### Issue: Resume Upload Fails
- Check Firebase Storage permissions
- Verify storage bucket exists
- Check Cloud Storage Security Rules
- Ensure file size is under 10MB

### Issue: Slow Performance
- Check Vercel Analytics dashboard
- Review API response times
- Check if Gemini API quota is being throttled
- Enable image optimization

## Monitoring & Analytics

### Vercel Analytics
1. Dashboard > Analytics
2. View real-time traffic and performance
3. Monitor Core Web Vitals
4. Track deployments

### Firebase Monitoring
1. Console > Performance
2. Check database read/write counts
3. Monitor storage usage
4. View authentication events

## Scaling Considerations

### Firestore Pricing
- Free tier: 1GB storage, 50k reads/day, 20k writes/day
- Excellent for initial launch
- Upgrade if you exceed limits

### Firebase Storage Pricing
- Free tier: 5GB storage, 1GB/day download
- Good for resume storage
- Cheap additional storage

### Gemini API Pricing
- Pay per request
- Very affordable for job forms
- Monitor usage in Google AI Studio

### Vercel Pricing
- Free: Unlimited deployments, 100GB bandwidth
- Pro ($20/month): Advanced features
- Enterprise: Custom limits

## Security Best Practices

1. **Rotate API Keys Regularly**
   - Regenerate Gemini keys every 3 months
   - Update in Vercel environment variables

2. **Monitor Firebase Usage**
   - Check for unusual read/write patterns
   - Set up billing alerts

3. **Keep Dependencies Updated**
   ```bash
   npm update
   npm audit
   ```

4. **Enable HTTPS**
   - Vercel auto-enables HTTPS
   - Update internal links to use HTTPS

5. **Environment Variable Security**
   - Never commit `.env` files
   - Always use Vercel Settings for secrets
   - Rotate keys periodically

## Backup & Recovery

### Database Backups
1. Firebase Console > Firestore > Backups
2. Enable automatic backups
3. Set retention policy

### Code Backups
- GitHub automatically backs up your code
- Keep main branch protected
- Use meaningful commit messages

## Custom Domain Setup

If using a custom domain (e.g., `jobagent.com`):

1. Register domain with registrar
2. Add to Vercel in Settings > Domains
3. Update DNS records as shown by Vercel
4. Add domain to Firebase authorized domains
5. Update Google OAuth redirect URIs

## Continuous Integration / Deployment

Vercel automatically:
1. Builds on every push
2. Runs preview deployments on PRs
3. Deploys to production on merge to main
4. Manages SSL certificates
5. Handles CDN distribution

To customize CI/CD:
1. Create `vercel.json` in project root
2. Define build and environment settings
3. Configure preview and production separately

Example `vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "env": {
    "NEXT_PUBLIC_FIREBASE_API_KEY": "@firebase_api_key",
    "NEXT_PUBLIC_GEMINI_API_KEY": "@gemini_key"
  }
}
```

## Next Steps After Deployment

1. **Share your app** - Get feedback from friends
2. **Optimize performance** - Check Vercel Analytics
3. **Add more features** - Email notifications, integrations
4. **Promote on social media** - Let people know
5. **Collect feedback** - Improve based on usage
6. **Monitor costs** - Watch Firebase and API usage

---

**Congratulations!** Your JobAgent is now live on the internet! 🚀
