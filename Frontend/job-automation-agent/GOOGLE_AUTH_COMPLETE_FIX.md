# Google Sign-In Setup - Complete Fix Guide

## The Problem
You're getting the error: **"auth/unauthorized-domain"**

This means Firebase doesn't recognize the domain you're accessing the app from. Google Sign-In requires explicit domain authorization for security reasons.

## The Solution (3 Steps - 3 Minutes)

### Step 1: Identify Your Domain

**If running locally:**
```
Your domain is: localhost:3000
```

**If deployed on Vercel:**
```
Your domain is: your-project.vercel.app
(You can find this in Vercel dashboard)
```

**If using a custom domain:**
```
Your domain is: yourdomain.com
```

### Step 2: Add Domain to Firebase

1. Open [Firebase Console](https://console.firebase.google.com/)
2. Select your **JobAgent** project
3. Click **Authentication** in the left sidebar
4. Click the **Settings** gear icon (top right)
5. Scroll down to **Authorized domains**
6. Click **Add domain**
7. Paste your domain (from Step 1)
8. Click **Add**

### Step 3: Test It

1. **Clear your browser completely:**
   - Windows: Press `Ctrl+Shift+Delete`
   - Mac: Press `Cmd+Shift+Delete`
   - Select all data and clear

2. **Refresh your app:**
   - Go to your app URL
   - Refresh with `Ctrl+F5` (or `Cmd+Shift+R` on Mac)

3. **Try Google Sign-In again**

That's it! The error should be gone. 🎉

## Domains to Add

Add these domains based on your setup:

| Use Case | Domain | Example |
|----------|--------|---------|
| Local Development | `localhost:3000` | `localhost:3000` |
| Vercel Production | Your Vercel URL | `my-jobagent.vercel.app` |
| Custom Domain | Your domain | `jobagent.com` |

**Tip:** You can add multiple domains to test both locally and in production.

## Troubleshooting

### Still Getting "auth/unauthorized-domain"?

**Check 1: Domain Format**
- Make sure you added the domain **exactly** as it appears in your browser's address bar
- Firebase is case-sensitive
- Include the port number if using one (`:3000`)
- Don't include `https://` or `http://`

**Check 2: Wait for Firebase to Update**
- After adding a domain, wait 30 seconds
- Firebase needs time to propagate changes

**Check 3: Clear Cache Thoroughly**
- Incognito/Private window test (bypasses cache)
- Open new incognito window
- Navigate to your app
- Try Google Sign-In

**Check 4: Verify Google is Enabled**
1. Firebase Console > Authentication
2. Click **Sign-in method**
3. Make sure **Google** has a **blue toggle** (enabled)
4. If not, click it to enable

**Check 5: Check Your Firebase Config**
```javascript
// In Firebase Console > Project Settings
// Verify these match your environment variables:
- API Key (NEXT_PUBLIC_FIREBASE_API_KEY)
- Auth Domain (NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN)
- Project ID (NEXT_PUBLIC_FIREBASE_PROJECT_ID)
- App ID (NEXT_PUBLIC_FIREBASE_APP_ID)
```

### Getting Different Error?

**"Invalid Client ID"**
- Your Firebase config is wrong
- Check all env vars match Firebase Console exactly

**"Pop-ups blocked"**
- Enable pop-ups for your domain in browser settings
- Google Sign-In uses a pop-up window

**"Google Sign-In not enabled"**
- Go to Firebase > Authentication > Sign-in method
- Click Google
- Toggle to enable (blue)

## Quick Verification Checklist

- [ ] Identified my domain (from browser address bar)
- [ ] Went to Firebase Console > Authentication > Settings
- [ ] Added my domain to "Authorized domains"
- [ ] Waited 30 seconds
- [ ] Cleared browser cache (or tried incognito)
- [ ] Refreshed the page
- [ ] Tried Google Sign-In again

## Code Changes Made

The app now has better error handling:
- Shows helpful error message when domain is unauthorized
- Logs the error code for debugging
- Suggests the fix document
- Handles pop-up blocking gracefully

## Need Help?

Check these files in order:
1. **This file** - You're reading it! 
2. **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - General troubleshooting
3. **[FIREBASE_SETUP.md](./FIREBASE_SETUP.md)** - Complete Firebase setup
4. **[README.md](./README.md)** - Project overview

## Success!

Once you see the Google Sign-In popup (not the error), you've successfully fixed it! 

Your app is ready to use Google authentication. 🚀
