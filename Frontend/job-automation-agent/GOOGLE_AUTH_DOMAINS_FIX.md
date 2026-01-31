# Fix: Firebase auth/unauthorized-domain Error

## What's the Problem?

The error `auth/unauthorized-domain` means Firebase doesn't recognize the domain you're accessing the app from. This is a security measure - you need to explicitly authorize each domain that will use Google Sign-In.

## Fix It in 3 Minutes

### Step 1: Get Your Current Domain

**For localhost (local development):**
- Domain: `localhost`
- Add to Firebase as: `localhost:3000`

**For Vercel deployment:**
- Check your deployment URL
- Example: `my-jobagent.vercel.app`
- Add to Firebase as: `my-jobagent.vercel.app`

### Step 2: Add Domain to Firebase Console

1. Open [Firebase Console](https://console.firebase.google.com/)
2. Select your JobAgent project
3. Go to **Authentication** → **Settings** (gear icon top-right)
4. Scroll down to **Authorized domains**
5. Click **Add domain**
6. Enter your domain:
   - `localhost:3000` (for local testing)
   - Your Vercel domain (for production)
   - Both if you want both to work

### Step 3: Test It

Clear your browser cache and refresh:
- Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
- Select all data and clear
- Go back to login page
- Try Google Sign-In again

## Domains You Should Add

### Local Development
```
localhost:3000
```

### Vercel Production
```
your-project-name.vercel.app
```

### Custom Domain (if you have one)
```
yourdomain.com
```

## Note: localhost vs 127.0.0.1

If you get an error accessing via `127.0.0.1:3000`, use `localhost:3000` instead. They're different to Firebase.

## Troubleshooting

### Still Getting Error?
1. Make sure you added the domain **exactly** as it appears in your browser's address bar
2. Check capitalization (Firebase is case-sensitive)
3. Include port number if accessing via port (`:3000`)
4. Wait 30 seconds after adding domain (Firebase needs time to update)
5. Try in an incognito window (clears old sessions)

### Getting "Google Sign-In not enabled"?
1. Go to Firebase > Authentication
2. Click **Sign-in method**
3. Make sure Google is **Enabled** (blue toggle)
4. If not, click it and enable it

### Getting "Invalid Client ID"?
Your Firebase config might be wrong. Check:
1. Go to Project Settings
2. Verify all your environment variables match exactly:
   - NEXT_PUBLIC_FIREBASE_API_KEY
   - NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
   - NEXT_PUBLIC_FIREBASE_PROJECT_ID
   - etc.

## Quick Copy-Paste Instructions

```
1. Firebase Console → Authentication → Settings
2. Scroll to "Authorized domains"
3. Add domain button → Copy-paste your domain
4. Click Add
5. Wait 30 seconds
6. Refresh browser (Ctrl+F5)
7. Try Google Sign-In again
```

That's it! 🎉
