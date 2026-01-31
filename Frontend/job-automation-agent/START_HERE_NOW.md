# Start Here - Google Auth Fix

You're getting a Google Sign-In error. Here's how to fix it in 3 minutes:

## Your Error
```
auth/unauthorized-domain
```

## The Fix (Copy-Paste Ready)

### 1. Go to Firebase Console
Open this link: https://console.firebase.google.com/

### 2. Find Your Domain
Look at your browser's address bar. Your domain is:
- **If local:** `localhost:3000`
- **If Vercel:** `your-project.vercel.app`
- **If custom:** `yourdomain.com`

### 3. Add Domain to Firebase

```
Authentication → Settings (gear icon) → Scroll to "Authorized domains" → Add domain → Paste your domain → Add
```

### 4. Clear Cache & Refresh
- Press: `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
- Click "Clear all"
- Go back to your app
- Refresh: `Ctrl+F5` or `Cmd+Shift+R`
- Try Google Sign-In again

## It Works?
Great! Your app is ready. 🎉

## Still Getting Error?
See: **[GOOGLE_AUTH_COMPLETE_FIX.md](./GOOGLE_AUTH_COMPLETE_FIX.md)** for troubleshooting

## All Set?
Now explore your JobAgent app! 🚀
- Landing page: Home
- Login/Register: Create account
- Dashboard: Chat with AI to fill forms
