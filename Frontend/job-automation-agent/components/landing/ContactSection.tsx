'use client';

import React from 'react';

export function ContactSection() {
  return (
    <section id="contact" className="py-20 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-bold mb-4">
          Contact Us
        </h2>
        <p className="text-lg text-foreground/60 mb-10">
          Have questions or feedback? We’d love to hear from you.
        </p>

        <div className="bg-card/50 border border-border/40 rounded-xl p-8">
          <p className="text-foreground/70">
            📧 Email: <span className="text-primary">support@jobagent.ai</span>
          </p>
          <p className="text-foreground/70 mt-2">
            💬 We usually respond within 24 hours.
          </p>
        </div>
      </div>
    </section>
  );
}
