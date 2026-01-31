'use client';

import React from 'react';
import { Upload, Brain, CheckCircle2, Zap, BarChart3, Lock } from 'lucide-react';

const features = [
  {
    icon: Upload,
    title: 'Smart Resume Upload',
    description: 'Upload your resume once. Our AI extracts all your information and keeps it secure.'
  },
  {
    icon: Brain,
    title: 'Intelligent Filling',
    description: 'AI understands context and fills forms accurately with your information.'
  },
  {
    icon: CheckCircle2,
    title: 'Multi-Form Support',
    description: 'Handles Google Forms, LinkedIn, Indeed, and custom website applications.'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Apply to jobs 50x faster. Automated form filling takes seconds, not hours.'
  },
  {
    icon: BarChart3,
    title: 'Application Tracking',
    description: 'Track all your applications in one place with real-time status updates.'
  },
  {
    icon: Lock,
    title: 'Privacy Secured',
    description: 'Your resume and data are encrypted and never shared with third parties.'
  }
];

export function FeaturesSection() {
  return (
    <section id="features" className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Everything You Need
          </h2>
          <p className="text-lg text-foreground/60 max-w-2xl mx-auto">
            Comprehensive features designed to make job hunting effortless and efficient.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div 
                key={idx}
                className="group p-6 rounded-xl bg-card/50 border border-border/40 hover:border-primary/40 transition duration-300 hover:bg-card/80 hover:shadow-lg hover:shadow-primary/10"
              >
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-foreground/60 text-sm">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
