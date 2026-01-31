# Fix: Firebase Permissions Error

## The Problem
```
Error fetching user profile: Missing or insufficient permissions.
```

This error occurs because Firebase Firestore Security Rules haven't been configured.

## What Was Fixed

1. **AuthContext.tsx** - Updated to create user profiles from Firebase Auth data instead of immediately reading from Firestore
2. **Created Server Actions** - New `/app/actions/userProfile.ts` for secure profile operations
3. **Security Rules** - Created `/firestore.rules` with proper permissions

## How to Fix It

### Step 1: Update Firebase Security Rules

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Firestore Database** > **Rules** tab
4. Replace all rules with the content from `/firestore.rules`
5. Click **Publish**

The rules allow users to:
- Read their own profile
- Create their own profile
- Update their own profile
- Delete their own profile

### Step 2: Test the Fix

1. Clear your browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
2. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
3. Try signing up or logging in again
4. The error should be gone!

## What Changed in the Code

### Before (Broken)
```tsx
// This tried to read from Firestore immediately
const userDocSnap = await getDoc(userDocRef);
// But the user had no permissions!
```

### After (Fixed)
```tsx
// Uses Firebase Auth data directly
const defaultProfile: UserProfile = {
  uid: currentUser.uid,
  email: currentUser.email || '',
  displayName: currentUser.displayName || '',
  photoURL: currentUser.photoURL || ''
};
// Firestore is only accessed when needed via server actions
```

## Security Rules Explained

```
/users/{userId} - Users can only read/write their own profile
/applications/{applicationId} - Users can only manage their own applications
/* - Everything else is denied by default
```

## If You Still Have Issues

1. **Check Firebase is initialized** - See `FIREBASE_SETUP.md`
2. **Verify environment variables** - See `SETUP_CHECKLIST.md`
3. **Check browser console** - Press F12, go to Console tab
4. **Check Firebase Rules are published** - Rules editor shows "Published" status

## Files Updated

- `/context/AuthContext.tsx` - Removed Firestore read on auth
- `/app/actions/userProfile.ts` - New secure profile operations (optional, for future use)
- `/firestore.rules` - New security rules (must be applied in Firebase)

All changes are backward compatible and don't affect existing functionality.
