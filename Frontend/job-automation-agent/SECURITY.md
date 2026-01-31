# JobAgent - Security Guidelines

Important security information for deploying and maintaining JobAgent.

---

## 🔐 API Key Security

### Gemini API Key

**Status:** ✅ SECURE (Server-side only)

Your Gemini API key is **never exposed to the client browser**. It's handled securely:

1. **Environment Variable:** `GEMINI_API_KEY` (no `NEXT_PUBLIC_` prefix)
2. **Location:** Only on the server (Next.js server actions)
3. **Access:** Handled via secure server action in `/app/actions/gemini.ts`
4. **Browser:** Client never sees the key

**Why this matters:**
- Prevents API key theft or misuse
- Protects your API quota
- Prevents unauthorized API calls
- Maintains application security

### Firebase API Keys

**Status:** ⚠️ SEMI-PUBLIC (By design)

Firebase keys are prefixed with `NEXT_PUBLIC_` because:
1. Firebase uses browser-based security (Authentication)
2. Security Rules protect data on the backend
3. No sensitive data stored in keys
4. Industry standard for Firebase apps

**Firebase Security Rules:**
```javascript
// Only users can read/write their own data
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

---

## 🛡️ Security Best Practices

### Environment Variables

**DO:**
- ✅ Store all API keys in environment variables
- ✅ Use `GEMINI_API_KEY` (no NEXT_PUBLIC_)
- ✅ Keep `.env.local` in `.gitignore`
- ✅ Never commit `.env` files
- ✅ Rotate keys regularly

**DON'T:**
- ❌ Hardcode API keys in source code
- ❌ Commit `.env` files to git
- ❌ Share API keys in emails/messages
- ❌ Use `NEXT_PUBLIC_` for sensitive keys
- ❌ Expose keys in client-side code

### Server Actions

All API calls to Gemini are handled via **Server Actions** (`/app/actions/gemini.ts`):

```typescript
'use server'; // Runs only on server

export async function sendGeminiMessage(message: string) {
  const apiKey = process.env.GEMINI_API_KEY; // Only available on server
  // API call happens here, never exposed to client
  return response;
}
```

### Database Security

**Firestore Security Rules** protect user data:
- Users can only access their own data
- Applications are tied to user IDs
- Resumes are stored securely
- No cross-user data access

---

## 🔒 Before Deploying

### Checklist

- [ ] Never include `.env` files in git
- [ ] Add `.env.local` to `.gitignore`
- [ ] All API keys in Vercel environment variables (not in code)
- [ ] Firebase Security Rules configured
- [ ] Cloud Storage rules configured
- [ ] GEMINI_API_KEY set as private env var
- [ ] No `NEXT_PUBLIC_` prefix on sensitive keys
- [ ] No console.log of sensitive data
- [ ] Review all API calls are server-side
- [ ] Test with different user accounts

### Vercel Settings

1. **Project Settings > Environment Variables:**
   ```
   GEMINI_API_KEY=your_key_here [Private]
   NEXT_PUBLIC_FIREBASE_API_KEY=your_key [Public]
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=... [Public]
   ... other Firebase keys ...
   ```

2. **Mark as Private:** Only `GEMINI_API_KEY` should be private
3. **Different values for different environments:** Dev vs Production

### Firebase Console

1. **Authentication > Settings:**
   - Add authorized domains
   - Enable only needed providers

2. **Firestore > Rules:**
   - Enforce user-specific access
   - Test rules before deploying

3. **Storage > Rules:**
   - Only users can access their own resumes
   - Example rule:
   ```javascript
   match /resumes/{userId}/{file=**} {
     allow read, write: if request.auth.uid == userId;
   }
   ```

---

## 🚨 Security Issues & Fixes

### Issue: API Key Exposed in Client

**Problem:** Seeing `NEXT_PUBLIC_GEMINI_API_KEY` in browser

**Solution:** ✅ Already Fixed!
- Changed to `GEMINI_API_KEY` (no NEXT_PUBLIC_)
- Moved to server action `/app/actions/gemini.ts`
- Key never leaves the server

### Issue: Unauthorized API Access

**Prevention:**
- Authenticate users with Firebase Auth
- Only authenticated users can access chat
- Each request tied to user ID
- Rate limiting on API calls (if needed)

### Issue: Data Leaks

**Prevention:**
- Firestore Security Rules restrict data access
- Cloud Storage rules restrict file access
- No sensitive data in localStorage
- HTTPS everywhere (Vercel auto-enables)

### Issue: DDoS / Quota Exhaustion

**Prevention:**
- Firebase free tier has limits
- Monitor API quota in Google AI Studio
- Set up billing alerts
- Implement rate limiting if needed

---

## 🔐 Running Locally

### Setup

1. Create `.env.local`:
```bash
# Firebase
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=...
NEXT_PUBLIC_FIREBASE_PROJECT_ID=...
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=...
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=...

# Gemini (Private - never in NEXT_PUBLIC_)
GEMINI_API_KEY=your_key_here
```

2. `.env.local` is already in `.gitignore` ✅

3. Keys only loaded on server ✅

### Development

```bash
npm run dev
# API calls go through server actions
# Keys never visible in browser
```

---

## 📊 Monitoring & Alerts

### Google AI Studio
- Monitor API usage: https://aistudio.google.com/
- Check quota limits
- Set up billing alerts
- Review usage patterns

### Firebase Console
- Monitor read/write counts
- Check storage usage
- Review authentication events
- Set up billing alerts

### Vercel Analytics
- Monitor API response times
- Check error rates
- Review performance metrics
- Set up alerts for downtime

---

## 🔄 Key Rotation

### When to Rotate
- Monthly (recommended)
- After suspected compromise
- Before public release
- When leaving the team

### How to Rotate

1. **Generate new key** in Google AI Studio
2. **Test** with new key locally
3. **Update** in Vercel environment variables
4. **Monitor** for errors (wait 15 minutes)
5. **Delete** old key in console
6. **Confirm** everything works

### Firebase Keys
- Regenerate in Firebase Console
- Update all environment variables
- Redeploy to Vercel

---

## 🎯 Security Checklist (Ongoing)

**Weekly:**
- [ ] Monitor API usage in Google AI Studio
- [ ] Check Vercel build logs
- [ ] Review authentication errors

**Monthly:**
- [ ] Rotate API keys
- [ ] Review Firebase usage
- [ ] Update dependencies (`npm update`)
- [ ] Audit npm packages (`npm audit`)

**Quarterly:**
- [ ] Full security review
- [ ] Update all dependencies
- [ ] Test disaster recovery
- [ ] Review Firebase rules

**Yearly:**
- [ ] Complete security audit
- [ ] Penetration testing
- [ ] Update security policies
- [ ] Team training

---

## 📚 Additional Resources

- [Google AI API Security](https://ai.google.dev/docs)
- [Firebase Security Rules](https://firebase.google.com/docs/database/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security Best Practices](https://nextjs.org/docs/app/building-your-application/security)
- [Vercel Security](https://vercel.com/docs/security)

---

## 🆘 Report a Security Issue

If you discover a security vulnerability:

1. **DO NOT** post it publicly
2. **DO NOT** create a GitHub issue
3. **Email** the maintainer privately
4. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix

Response time: 24-48 hours

---

## Summary

✅ **API keys are secure** - handled server-side
✅ **User data is protected** - Firebase Security Rules
✅ **No client exposure** - No secrets in browser
✅ **Production ready** - Follows industry best practices

**Your JobAgent is secure!** 🔐

For questions, review the relevant sections above or check the documentation files.
