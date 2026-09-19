"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api, TrackLesson, UserProfile, StructuredLesson } from "@/lib/api";
import LessonViewer from "@/components/LessonViewer";
import { BookOpen, Award, CheckCircle2, ChevronRight, Sparkles } from "lucide-react";

export default function LessonsHubPage() {
  const [lessons, setLessons] = useState<TrackLesson[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTrack, setSelectedTrack] = useState<number>(1);
  const [structuredLesson, setStructuredLesson] = useState<StructuredLesson | null>(null);
  const [loadingStructured, setLoadingStructured] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [lessData, profData] = await Promise.all([
          api.getTrackLessons(),
          api.getProfile()
        ]);
        setLessons(lessData);
        setProfile(profData);
      } catch (err) {
        console.error("Failed to load lessons:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // When selected track changes, fetch structured lesson
  useEffect(() => {
    async function loadTrackStructured() {
      setLoadingStructured(true);
      try {
        const startChalId = `chal-${(selectedTrack - 1) * 10 + 1}`;
        const sLesson = await api.getStructuredLessonByChallenge(startChalId);
        setStructuredLesson(sLesson);
      } catch (err) {
        console.error("Failed to load structured lesson for track:", err);
      } finally {
        setLoadingStructured(false);
      }
    }
    loadTrackStructured();
  }, [selectedTrack]);

  const currentLesson = lessons.find((l) => l.track_number === selectedTrack) || lessons[0];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-3">
              <span className="text-2xl font-black bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Python Mastery
              </span>
              <span className="text-[11px] font-semibold bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-500/30">
                Educational Lessons
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-1 text-sm font-medium">
              <Link
                href="/"
                className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition"
              >
                Curriculum
              </Link>
              <Link
                href="/lessons"
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-white font-semibold transition"
              >
                Lessons & Theory
              </Link>
              <Link
                href="/projects"
                className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition"
              >
                Practical Projects
              </Link>
              <Link
                href="/interview"
                className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition"
              >
                Interview Arena
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-6">
            <div className="text-sm font-semibold text-orange-400">🔥 {profile?.current_streak || 0} Day Streak</div>
            <div className="text-sm font-semibold text-emerald-400">⚡ {profile?.total_xp || 0} XP</div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* Banner */}
        <section className="bg-gradient-to-r from-emerald-950/40 via-indigo-950/30 to-slate-900 border border-slate-800 rounded-2xl p-8 mb-8 shadow-xl">
          <div className="max-w-3xl">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
              Structured Educational Platform
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-1 mb-3">
              Python Lessons & Interactive Theory
            </h1>
            <p className="text-slate-300 text-sm leading-relaxed">
              Every topic is broken down systematically: understand the concept, connect with real-life analogies, examine the syntax, inspect line-by-line code examples, avoid common pitfalls, and master the concept check quiz.
            </p>
          </div>
        </section>

        {loading ? (
          <div className="text-center py-20 text-slate-400">Loading lessons library...</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Sidebar: Tracks Navigation */}
            <div className="lg:col-span-4 space-y-2">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 px-1">
                10 Learning Modules
              </div>
              <div className="space-y-1.5">
                {lessons.map((less) => (
                  <button
                    key={less.track_number}
                    onClick={() => setSelectedTrack(less.track_number)}
                    className={`w-full text-left p-3.5 rounded-xl border transition flex items-start justify-between ${
                      selectedTrack === less.track_number
                        ? "bg-indigo-600/20 border-indigo-500/60 text-white shadow-md"
                        : "bg-slate-900/50 border-slate-800/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                    }`}
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-[11px] font-bold text-indigo-400 uppercase">
                          Track {less.track_number}
                        </span>
                        <span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-slate-400">
                          ⏱️ {less.reading_time_minutes} min
                        </span>
                      </div>
                      <div className="text-sm font-bold text-slate-200">{less.title}</div>
                      <div className="text-xs text-slate-400 mt-0.5 line-clamp-1">{less.subtitle}</div>
                    </div>
                    <span className="text-slate-500 text-sm font-bold">
                      {selectedTrack === less.track_number ? "→" : ""}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Right Main Panel: Selected Track Deep Dive */}
            <div className="lg:col-span-8 space-y-6">
              {loadingStructured ? (
                <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
                  Loading lesson details...
                </div>
              ) : structuredLesson ? (
                <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8">
                  <LessonViewer
                    lesson={structuredLesson}
                    onStartCoding={() => {
                      window.location.href = `/learn/chal-${(selectedTrack - 1) * 10 + 1}`;
                    }}
                    onQuizPassed={(xp) => {
                      if (profile) {
                        setProfile({ ...profile, total_xp: profile.total_xp + xp });
                      }
                    }}
                  />
                </div>
              ) : currentLesson ? (
                <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                        Track {currentLesson.track_number} Guide
                      </span>
                      <span className="text-slate-600">•</span>
                      <span className="text-xs text-slate-400">{currentLesson.reading_time_minutes} min read</span>
                    </div>
                    <h2 className="text-2xl font-black text-white">{currentLesson.title}</h2>
                    <div className="text-sm text-indigo-300 font-medium mt-1">{currentLesson.subtitle}</div>
                    <p className="text-sm text-slate-300 mt-3 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                      {currentLesson.overview}
                    </p>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
