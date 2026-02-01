'use client';

import { auth, db } from '@/lib/firebase';
import { doc, getDoc } from 'firebase/firestore';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

import { Mail, Lock, Loader, Chrome } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user) {
      router.push('/dashboard');
    }
  }, [user, router]);

  const handleEmailLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  setLoading(true);

  try {
    const result = await signInWithEmailAndPassword(auth, email, password);
    const user = result.user;

    const userRef = doc(db, 'users', user.uid);
    const snap = await getDoc(userRef);

    if (!snap.exists()) {
      await auth.signOut();
      setError('Account not found. Please register first.');
      return;
    }

    router.push('/dashboard');
  } catch (err: any) {
    setError(err.message || 'Failed to login');
  } finally {
    setLoading(false);
  }
};


  const handleGoogleLogin = async () => {
  setError('');
  setLoading(true);

  try {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    const user = result.user;

    // 🔒 Check if user exists in Firestore
    const userRef = doc(db, 'users', user.uid);
    const snap = await getDoc(userRef);

    if (!snap.exists()) {
      await auth.signOut();
      router.push('/register');
      return;
    }

    router.push('/dashboard');
  } catch (err: any) {
    let errorMessage = err.message || 'Failed to login with Google';

    if (err.code === 'auth/popup-closed-by-user') {
      errorMessage = 'Popup closed before completing sign in';
    }

    if (err.code === 'auth/unauthorized-domain') {
      errorMessage = 'Domain not authorized in Firebase';
    }

    setError(errorMessage);
  } finally {
    setLoading(false);
  }
};


 

  if (user) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-20 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-accent/20 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-md slide-in-up">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">JA</span>
          </div>
          <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
          <p className="text-foreground/60">Sign in to your JobAgent account</p>
        </div>

        <div className="bg-card/50 border border-border/40 rounded-2xl p-8 backdrop-blur-sm">
          {/* Google Sign In */}
          <button
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full py-3 px-4 border border-border/60 rounded-lg font-medium hover:bg-card/80 transition flex items-center justify-center gap-2 mb-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Chrome className="w-5 h-5" />
            {loading ? 'Signing in...' : 'Continue with Google'}
          </button>

          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border/40" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-card/50 text-foreground/60">Or with email</span>
            </div>
          </div>

          {/* Error message */}
          {error && (
            <div className="mb-4 p-3 bg-destructive/10 border border-destructive/30 rounded-lg text-destructive text-sm">
              {error}
            </div>
          )}

          {/* Email login form */}
          <form onSubmit={handleEmailLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-foreground/40" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  required
                  className="w-full pl-10 pr-4 py-2 bg-input border border-border/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/40 transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-foreground/40" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full pl-10 pr-4 py-2 bg-input border border-border/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/40 transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>
        </div>

        {/* Sign up link */}
        <p className="text-center mt-6 text-foreground/60">
          Don't have an account?{' '}
          <Link href="/register" className="text-primary hover:text-primary/80 font-medium">
            Create one
          </Link>
        </p>

        {/* Back to home */}
        <div className="text-center mt-4">
          <Link href="/" className="text-foreground/60 hover:text-foreground text-sm transition">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}