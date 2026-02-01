'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';
import { BarChart3, ArrowLeft, ArrowRight, CheckCircle } from 'lucide-react';
import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';
import { Pencil } from 'lucide-react';


const questions = [
  'Tell me about yourself.',
  'What are your strongest technical skills?',
  'What technologies are you most comfortable with?',
  'Describe a challenging project you worked on.',
  'How do you handle tight deadlines?',
  'Explain a time you failed and what you learned.',
  'How do you approach problem-solving?',
  'Describe your experience with teamwork.',
  'How do you handle conflicts in a team?',
  'What motivates you at work?',
  'What kind of role are you looking for?',
  'How do you stay updated with new technologies?',
  'Describe a time you showed leadership.',
  'What are your career goals for the next 3–5 years?',
  'Why should we hire you?'
];

export default function AnalyticsPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<string[]>(Array(questions.length).fill(''));
  const [savedAnswers, setSavedAnswers] = useState<string[] | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);

    useEffect(() => {
  if (!user) return;

  const fetchSaved = async () => {
    const ref = doc(db, 'users', user.uid, 'interviewAnalytics', 'responses');
    const snap = await getDoc(ref);
    if (snap.exists()) {
      setSavedAnswers(snap.data().answers || []);
    }
  };

  fetchSaved();
}, [user]);

const saveAnswers = async () => {
  if (!user) return;

  const ref = doc(db, 'users', user.uid, 'interviewAnalytics', 'responses');
  await setDoc(ref, {
    answers,
    updatedAt: new Date()
  });

  setSavedAnswers(answers);
};

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return null;
  }

  const handleAnswerChange = (value: string) => {
    const updated = [...answers];
    updated[current] = value;
    setAnswers(updated);
  };

  const progress = Math.round(((current + 1) / questions.length) * 100);

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <div className="flex h-[calc(100vh-60px)]">
        <DashboardSidebar />

        <main className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto p-6 space-y-8">
            {/* Header */}
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <BarChart3 className="w-6 h-6 text-primary" />
                Interview Analytics
              </h1>
              <p className="text-foreground/60 mt-1">
                Answer interview questions to analyze and improve your responses
              </p>
            </div>

            {/* Progress */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-foreground/60">
                <span>
                  Question {current + 1} of {questions.length}
                </span>
                <span>{progress}% complete</span>
              </div>
              <div className="w-full h-2 bg-border/40 rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {/* Question Card */}
            <div className="bg-card/50 border border-border/40 rounded-2xl p-6 space-y-6">
              <h2 className="text-xl font-semibold">
                {questions[current]}
              </h2>

              <textarea
                value={answers[current]}
                onChange={(e) => handleAnswerChange(e.target.value)}
                placeholder="Type your answer here..."
                rows={6}
                className="w-full px-4 py-3 bg-input border border-border/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/40 transition resize-none"
              />

              {/* Navigation */}
              <div className="flex items-center justify-between">
                <button
                  onClick={() => setCurrent((c) => Math.max(0, c - 1))}
                  disabled={current === 0}
                  className="flex items-center gap-2 px-4 py-2 border border-border/40 rounded-lg hover:bg-card/80 transition disabled:opacity-40"
                >
                  <ArrowLeft className="w-4 h-4" />
                  Previous
                </button>

                {current === questions.length - 1 ? (
                  <button
                    onClick={saveAnswers}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg"
                    >
                    <CheckCircle className="w-5 h-5" />
                    Save Responses
                    </button>

                ) : (
                  <button
                    onClick={() => setCurrent((c) => Math.min(questions.length - 1, c + 1))}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition"
                  >
                    Next
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>

            {/* Info */}
            <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg text-sm text-foreground/70">
              💡 Tip: Be honest and detailed. These responses will help generate personalized feedback and interview insights later.
            </div>
            {savedAnswers && (
                <div className="space-y-6">
                    <h2 className="text-2xl font-semibold">Your Saved Responses</h2>

                    {questions.map((q, index) => (
                    <div
                        key={index}
                        className="bg-card/50 border border-border/40 rounded-xl p-5 space-y-3"
                    >
                        <div className="flex justify-between items-start">
                        <h3 className="font-medium">{q}</h3>
                        <button
                            onClick={() => setEditingIndex(index)}
                            className="text-primary hover:underline flex items-center gap-1 text-sm"
                        >
                            <Pencil className="w-4 h-4" />
                            Edit
                        </button>
                        </div>

                        {editingIndex === index ? (
                        <textarea
                            value={savedAnswers[index]}
                            onChange={(e) => {
                            const updated = [...savedAnswers];
                            updated[index] = e.target.value;
                            setSavedAnswers(updated);
                            }}
                            onBlur={async () => {
                            if (!user) return;
                            const ref = doc(db, 'users', user.uid, 'interviewAnalytics', 'responses');
                            await updateDoc(ref, { answers: savedAnswers });
                            setEditingIndex(null);
                            }}
                            rows={4}
                            className="w-full bg-input border border-border/40 rounded-lg p-3"
                        />
                        ) : (
                        <p className="text-foreground/70 whitespace-pre-wrap">
                            {savedAnswers[index] || '—'}
                        </p>
                        )}
                    </div>
                    ))}
                </div>
                )}

          </div>
        </main>
      </div>
    </div>
  );
}
