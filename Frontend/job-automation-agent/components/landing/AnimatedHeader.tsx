'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export function AnimatedHeader() {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border/40">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
            <span className="text-white font-bold text-lg">JA</span>
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            JobAgent
          </h1>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-foreground/70 hover:text-foreground transition">
            Features
          </a>
          <a href="#how-it-works" className="text-foreground/70 hover:text-foreground transition">
            How it Works
          </a>
          <a href="#contact" className="text-foreground/70 hover:text-foreground transition">
            Contact
          </a>
        </nav>

        {/* CTA */}
        <div className="flex items-center gap-3">
          {user ? (
            <Link 
              href="/dashboard" 
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition"
            >
              Dashboard
            </Link>
          ) : (
            <>
              <Link 
                href="/login" 
                className="px-4 py-2 text-foreground hover:text-primary transition"
              >
                Login
              </Link>
              <Link 
                href="/register" 
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
