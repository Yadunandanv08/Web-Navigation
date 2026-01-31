# Troubleshooting Guide

## Firebase Errors

### Error: "auth/configuration-not-found"

**Cause:** Firebase credentials are not properly configured.

**Solutions:**
1. Check `.env.local` has all 6 Firebase variables with no extra spaces
2. Restart dev server: `Ctrl+C`, then `npm run dev`
3. Verify values in Firebase Console match your env vars exactly
4. Make sure you used `NEXT_PUBLIC_` prefix for all Firebase variables

### Error: "Firebase App named '[DEFAULT]' already exists"

**Cause:** Firebase is being initialized multiple times.

**Solution:**
- Already handled in the code, but if you see this:
- Clear browser cache/cookies
- Restart dev server

### Error: "Missing or insufficient permissions" or "Permission denied" on Firestore

**Cause:** Firestore Security Rules are blocking your request or not configured.

**Solutions:**
1. See **[FIX_PERMISSIONS_ERROR.md](./FIX_PERMISSIONS_ERROR.md)** for step-by-step fix
2. Apply the security rules from `/firestore.rules`:
   - Go to Firebase Console > Firestore Database > Rules
   - Replace with content from `/firestore.rules`
   - Click Publish
3. Check you're logged in (user should appear in Firebase Console > Authentication)
4. Verify Firestore Security Rules are set correctly (see FIREBASE_SETUP.md)
5. Check the user UID matches in rules
6. For testing only (NOT production):
   ```javascript
   match /{document=**} {
     allow read, write: if true;
   }
   ```

### Error: "auth/unauthorized-domain" (FIXED!)

**Status:** This error is now resolved! App uses Google Redirect method instead of popups.

**What Changed:**
- Google Sign-In now uses `signInWithRedirect()` 
- Works immediately without domain authorization
- More reliable and no pop-up blocker issues

**See:** **[GOOGLE_AUTH_FIX_REDIRECT.md](./GOOGLE_AUTH_FIX_REDIRECT.md)** for full details

**Quick Test:**
1. Go to login or register page
2. Click "Continue with Google"
3. Complete Google sign-in
4. Should redirect back automatically

**If Still Having Issues:**
- Clear browser cache (Ctrl+Shift+Delete)
- Try in incognito window
- Verify Firebase API key in environment variables
- Check Google is enabled: Firebase Console > Authentication > Sign-in methods

### Error: "Cannot read storage bucket"

**Cause:** Cloud Storage not initialized or rules blocking access.

**Solutions:**
1. Create a Cloud Storage bucket in Firebase Console
2. Set Storage Security Rules (see FIREBASE_SETUP.md)
3. Check bucket name in Firebase Console > Storage

---

## Gemini API Errors

### Error: "GEMINI_API_KEY is not set"

**Cause:** Server-side Gemini API key missing.

**Solution:**
1. Get key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add to `.env.local`: `GEMINI_API_KEY=your_key`
3. For Vercel: Add to Environment Variables (NOT `NEXT_PUBLIC_`)
4. Restart dev server

### Error: "API quota exceeded"

**Cause:** You've hit the Gemini API rate limit.

**Solution:**
- Wait a few minutes and try again
- Check Google AI Studio for quota information
- Consider upgrading to paid plan if heavy usage

---

## Environment Variables

### How to verify env vars are loaded

Add this to the browser console:
```javascript
console.log(process.env)
```

**You should see:**
- All `NEXT_PUBLIC_*` vars listed
- Server-side vars (like `GEMINI_API_KEY`) NOT listed (correct for security)

### Variables missing even though I added them?

1. **Local development:**
   - Create `.env.local` in project root
   - Add variables exactly as shown
   - Restart dev server: `Ctrl+C`, then `npm run dev`

2. **Vercel deployment:**
   - Go to Project Settings > Environment Variables
   - Add variables for Production environment
   - Trigger a redeploy (Deployments > Redeploy)

---

## Authentication Issues

### Can't sign up

**Check:**
1. Firebase Authentication > Sign-in method > Email/Password is enabled
2. Check browser console for specific error
3. Try email that hasn't been used before

### Google Sign-In not working

**Check:**
1. Firebase Authentication > Google is enabled
2. OAuth consent screen is configured in Google Cloud Console
3. Your app URL is in authorized redirect URIs
4. You're using HTTPS (required for Google Sign-In)

### User created but profile not showing

**Check:**
1. User exists in Firebase Console > Authentication
2. Firestore Database is created
3. Security Rules allow read/write to `/users/{uid}`

---

## App Won't Start

### Error: "Cannot find module..."

**Cause:** Dependencies not installed or old cache.

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Error: "Unexpected token in JSON"

**Cause:** Malformed JSON in files.

**Solution:**
- Check all `.json` files for syntax errors
- Check `.env.local` format (should not have quotes around values)
- Example:
  ```
  # Correct:
  NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
  
  # Wrong:
  NEXT_PUBLIC_FIREBASE_API_KEY="AIza..."
  ```

### Error: "Port 3000 already in use"

**Solution:**
```bash
# Kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Then start again
npm run dev
```

---

## Deployment Issues

### App works locally but not on Vercel

**Check:**
1. All env vars are set in Vercel project settings
2. Env vars are identical to `.env.local`
3. Triggered a redeploy (not just relying on auto-deploy)
4. Check deployment logs: Vercel Dashboard > Deployments > View logs

### 404 errors on Vercel

**Check:**
1. All pages exist in `/app` directory
2. Routes are correct in links
3. Try a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Blank page on Vercel

**Check:**
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab - is the page loading?
4. Check Vercel logs

---

## Performance Issues

### App feels slow

**Check:**
1. Open DevTools > Network tab
2. Look for slow requests (especially to Firebase or Gemini)
3. Check Vercel Edge Network performance
4. Consider using Firestore indexing for queries

### Firebase responses slow

**Cause:** No indexes on Firestore queries.

**Solution:**
1. Firebase Console > Firestore Database > Indexes
2. Create indexes for common queries
3. Responses will be instant after indexing

---

## Resume Upload Issues

### Resume won't upload

**Check:**
1. File size < 10MB
2. File format is PDF, DOC, or DOCX
3. Storage bucket exists in Firebase
4. Storage Security Rules allow uploads

### Uploaded resume not visible

**Check:**
1. Go to Firebase Console > Storage
2. Browse to `/resumes/{your_uid}/`
3. Should see the file there
4. If not, check Security Rules

---

## Chat/AI Issues

### Chat not responding

**Check:**
1. Open browser Console (F12)
2. Look for errors about Gemini API
3. Check that GEMINI_API_KEY is set
4. Check Gemini API quota hasn't been exceeded

### Thinking animation not showing

**Check:**
1. Browser supports animations (modern browsers)
2. Check for console errors
3. Try a hard refresh
4. Check that Gemini API is being called (Network tab)

---

## Debug Mode

To enable debug logging, add this to `.env.local`:

```
NEXT_PUBLIC_DEBUG=true
```

Then check browser Console for `[v0]` debug messages.

---

## Still Having Issues?

1. Check the relevant documentation file:
   - Firebase issues → FIREBASE_SETUP.md
   - Security issues → SECURITY.md
   - Setup issues → SETUP_GUIDE.md

2. Check browser Console (F12) for specific error messages

3. Check Vercel Deployment logs if deployed

4. Common fixes:
   - Restart dev server
   - Clear browser cache
   - Reinstall node_modules
   - Check env var spelling (exact match required)

---

## Quick Checklist

Before declaring something broken, verify:

- [ ] Dev server is running
- [ ] Env vars are set (correct spelling, no extra spaces)
- [ ] Env vars have correct values (copy/paste from Firebase Console)
- [ ] Firebase services are enabled (Auth, Firestore, Storage)
- [ ] Browser console doesn't have errors
- [ ] You waited > 5 seconds (first load can be slow)
- [ ] You tried a hard refresh (Ctrl+Shift+R)
- [ ] You tried restarting dev server (Ctrl+C, npm run dev)
