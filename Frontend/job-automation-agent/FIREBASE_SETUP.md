# Firebase Setup Guide

## Error: auth/configuration-not-found

This error means Firebase authentication isn't properly configured. Follow these steps to fix it.

---

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or select an existing project
3. Follow the setup wizard (all defaults are fine)
4. Create a **Web App** when prompted

---

## Step 2: Get Your Firebase Credentials

After creating the web app, you'll see the Firebase config. Copy these values:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

**You can always find these in:**
- Firebase Console > Project Settings > General > Your apps > Web

---

## Step 3: Add to Your Project (Local Development)

Create or update `.env.local` in your project root:

```bash
NEXT_PUBLIC_FIREBASE_API_KEY=YOUR_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=YOUR_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID=YOUR_APP_ID
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important:** 
- `.env.local` is in `.gitignore` - it won't be committed
- Restart your dev server after adding env vars: `Ctrl+C` then `npm run dev`

---

## Step 4: Enable Firebase Services

In the Firebase Console, enable these services:

### 4a. Authentication
1. Go to **Authentication** > **Sign-in method**
2. Enable **Email/Password**
3. Enable **Google** (optional but recommended)
   - You'll need a Google Cloud project (created automatically)
   - Set redirect URI to your app URL

### 4b. Firestore Database
1. Go to **Firestore Database**
2. Click **Create database**
3. Start in **Production mode**
4. Choose your region (closest to you)
5. Click **Create**

### 4c. Storage
1. Go to **Storage**
2. Click **Get started**
3. Start in **Production mode**
4. Choose your region (same as Firestore)
5. Click **Done**

---

## Step 5: Set Firestore Security Rules

In Firebase Console > Firestore Database > Rules, paste:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow users to read/write their own documents
    match /users/{uid} {
      allow read, write: if request.auth.uid == uid;
    }
    
    // Allow users to read/write their own application data
    match /applications/{doc=**} {
      allow read, write: if request.auth != null;
    }
    
    // Default deny all
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

Click **Publish** to apply.

---

## Step 6: Set Storage Security Rules

In Firebase Console > Storage > Rules, paste:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /resumes/{uid}/{filename} {
      allow read, write: if request.auth.uid == uid;
    }
    
    match /{allPaths=**} {
      allow read, write: if false;
    }
  }
}
```

Click **Publish** to apply.

---

## Step 7: Deploy to Vercel

### For Vercel Deployment:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add Firebase setup"
   git push
   ```

2. **Add Environment Variables in Vercel**
   - Go to Vercel Dashboard > Project > Settings > Environment Variables
   - Add all six Firebase variables (same values as `.env.local`)
   - Also add `GEMINI_API_KEY` (server-side only)

3. **Redeploy**
   - Go to Deployments
   - Click the three dots on the latest deployment
   - Select "Redeploy"

---

## Troubleshooting

### Error: "auth/configuration-not-found"
- Check that all six Firebase env vars are set
- Restart dev server: `Ctrl+C` then `npm run dev`
- Verify values don't have extra spaces or quotes

### Error: "firebaseConfig is not defined"
- Same as above - missing environment variables

### Error: "Permission denied" on Firestore
- Check Firestore Security Rules (Step 5)
- Make sure you're logged in with a real Firebase auth account

### Error: "Cannot read storage bucket"
- Check Storage Security Rules (Step 6)
- Make sure bucket is configured in Firebase Console > Storage

### Everything works locally but fails after deploying to Vercel
- Verify all env vars are set in Vercel project settings
- They should be identical to `.env.local`
- Trigger a redeploy after adding/changing env vars

---

## Verifying Setup

After setup, test this:

1. Go to your app homepage
2. Click **Sign Up**
3. Create an account with email
4. You should be able to log in
5. Go to Firebase Console > Authentication to see your user

If you see your user in Firebase, it's working! 

---

## Optional: Local Emulation

For completely local testing without Firebase cloud:

1. Install Firebase emulators:
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase init emulators
   ```

2. Start emulators:
   ```bash
   firebase emulators:start
   ```

3. Enable in your app:
   ```bash
   NEXT_PUBLIC_USE_FIREBASE_EMULATORS=true
   ```

4. Restart dev server

Now everything runs locally - useful for testing without costs!

---

## Production Checklist

- [ ] Firebase project created
- [ ] Web app configured
- [ ] All 6 env vars set locally
- [ ] Authentication enabled (Email, optionally Google)
- [ ] Firestore Database created in Production mode
- [ ] Storage bucket created in Production mode
- [ ] Firestore Security Rules set
- [ ] Storage Security Rules set
- [ ] App works locally
- [ ] All 7 env vars set in Vercel (6 Firebase + 1 Gemini)
- [ ] Deployed to Vercel and tested
- [ ] User can sign up and log in
- [ ] User profile visible in Firestore/Firebase Console

---

## Quick Reference

| Service | Purpose | Required |
|---------|---------|----------|
| Authentication | User login/signup | Yes |
| Firestore | Store user profiles, app data | Yes |
| Storage | Store resume files | Yes |
| Gemini API | AI form filling | Yes |
| Emulators | Local development | Optional |

---

## Need More Help?

- Firebase Docs: https://firebase.google.com/docs
- Getting Started: https://firebase.google.com/docs/web/setup
- Firestore Rules: https://firebase.google.com/docs/firestore/security/overview
- Storage Rules: https://firebase.google.com/docs/storage/security/overview
