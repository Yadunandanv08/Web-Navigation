'use client';

import React from 'react';
import { Upload, Brain, Zap } from 'lucide-react';

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-20 px-4">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-bold mb-4">
          How It Works
        </h2>
        <p className="text-lg text-foreground/60 mb-16">
          Three simple steps to automate your job applications.
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              icon: Upload,
              title: 'Upload Resume',
              desc: 'Upload your resume once. We securely store and understand it.'
            },
            {
              icon: Brain,
              title: 'AI Understands',
              desc: 'Our AI extracts and maps your details to job forms.'
            },
            {
              icon: Zap,
              title: 'Apply Faster',
              desc: 'Apply to multiple jobs automatically in seconds.'
            }
          ].map((step, i) => {
            const Icon = step.icon;
            return (
              <div
                key={i}
                className="p-6 rounded-xl bg-card/50 border border-border/40 hover:border-primary/40 transition"
              >
                <div className="w-12 h-12 mx-auto mb-4 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
                <p className="text-sm text-foreground/60">{step.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
