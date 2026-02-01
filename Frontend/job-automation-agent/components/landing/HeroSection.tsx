'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, Zap, Brain, FileCheck } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Animated gradient background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="max-w-5xl mx-auto px-4 text-center slide-in-up">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/30 mb-6">
          <Zap className="w-4 h-4 text-accent" />
          <span className="text-sm font-medium text-foreground/80">Powered by AI</span>
        </div>

        {/* Main heading */}
        <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          <span className="bg-gradient-to-r from-primary via-purple-500 to-accent bg-clip-text text-transparent">
            Automate Your Job
          </span>
          <br />
          <span className="text-foreground">Applications with AI</span>
        </h1>

        {/* Subheading */}
        <p className="text-lg md:text-xl text-foreground/70 mb-8 max-w-2xl mx-auto leading-relaxed">
          Upload your resume once, and let our intelligent agent fill out job applications for you. 
          Apply to hundreds of positions in minutes, not hours.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <Link 
            href="/register"
            className="group relative px-8 py-4 bg-primary text-primary-foreground rounded-xl font-semibold hover:bg-primary/90 transition overflow-hidden"
          >
            <span className="relative flex items-center justify-center gap-2">
              Start Free Trial
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition" />
            </span>
          </Link>
          
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
          <div className="p-4 rounded-lg bg-card/50 border border-border/40">
            <div className="text-2xl font-bold text-primary mb-1">10,000+</div>
            <p className="text-sm text-foreground/60">Applications Automated</p>
          </div>
          <div className="p-4 rounded-lg bg-card/50 border border-border/40">
            <div className="text-2xl font-bold text-accent mb-1">95%</div>
            <p className="text-sm text-foreground/60">Success Rate</p>
          </div>
          <div className="p-4 rounded-lg bg-card/50 border border-border/40">
            <div className="text-2xl font-bold text-primary mb-1">40hrs</div>
            <p className="text-sm text-foreground/60">Saved Per Month</p>
          </div>
          <div className="p-4 rounded-lg bg-card/50 border border-border/40">
            <div className="text-2xl font-bold text-accent mb-1">24/7</div>
            <p className="text-sm text-foreground/60">Active Agent</p>
          </div>
        </div>
      </div>
    </section>
  );
}
