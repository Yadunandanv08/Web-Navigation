'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { AnimatedHeader } from '@/components/landing/AnimatedHeader';
import { HeroSection } from '@/components/landing/HeroSection';
import { FeaturesSection } from '@/components/landing/FeaturesSection';
import { HowItWorksSection } from '@/components/landing/HowItWorksSection';
import { ContactSection } from '@/components/landing/ContactSection';

export default function LandingPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <>
      <AnimatedHeader />
      <main>
        <HeroSection />
        <FeaturesSection />
        <HowItWorksSection />
      <ContactSection />
        
        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-primary/10 via-transparent to-accent/10">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Transform Your Job Search?</h2>
            <p className="text-lg text-foreground/70 mb-8">
              Join thousands of job seekers who are saving hours every week with JobAgent.
            </p>
            <a 
              href="/register"
              className="inline-flex items-center gap-2 px-8 py-4 bg-primary text-primary-foreground rounded-xl font-semibold hover:bg-primary/90 transition"
            >
              Start Your Free Trial Today
            </a>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-border/40 py-12 px-4 bg-card/30">
          <div className="max-w-6xl mx-auto grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold mb-4">Product</h3>
              <ul className="space-y-2 text-foreground/60 text-sm">
                <li><a href="#" className="hover:text-foreground transition">Features</a></li>
                <li><a href="#" className="hover:text-foreground transition">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground transition">Security</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Company</h3>
              <ul className="space-y-2 text-foreground/60 text-sm">
                <li><a href="#" className="hover:text-foreground transition">About</a></li>
                <li><a href="#" className="hover:text-foreground transition">Blog</a></li>
                <li><a href="#" className="hover:text-foreground transition">Careers</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Legal</h3>
              <ul className="space-y-2 text-foreground/60 text-sm">
                <li><a href="#" className="hover:text-foreground transition">Privacy</a></li>
                <li><a href="#" className="hover:text-foreground transition">Terms</a></li>
                <li><a href="#" className="hover:text-foreground transition">Contact</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4">Support</h3>
              <ul className="space-y-2 text-foreground/60 text-sm">
                <li><a href="#" className="hover:text-foreground transition">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground transition">Docs</a></li>
                <li><a href="#" className="hover:text-foreground transition">Email</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border/40 pt-8 text-center text-foreground/60 text-sm">
            <p>© 2024 JobAgent. All rights reserved.</p>
          </div>
        </footer>
      </main>
    </>
  );
}
