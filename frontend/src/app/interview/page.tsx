"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api, InterviewProblem, UserProfile } from "@/lib/api";

export default function InterviewArenaPage() {
  const [problems, setProblems] = useState<InterviewProblem[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [filterDifficulty, setFilterDifficulty] = useState<string>("All");

  useEffect(() => {
    async function load() {
      try {
        const [probData, profData] = await Promise.all([
          api.getInterviewProblems(),
          api.getProfile()
        ]);
        setProblems(probData);
        setProfile(profData);
      } catch (err) {
        console.error("Failed to load interview problems:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const difficultyBadge = {
    Easy: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    Medium: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    Hard: "bg-rose-500/10 text-rose-400 border-rose-500/20"
  };

  const filtered = problems.filter(
    (p) => filterDifficulty === "All" || p.difficulty === filterDifficulty
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-3">
              <span className="text-2xl font-black bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
                Python Mastery
              </span>
              <span className="text-[11px] font-semibold bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded-full border border-pink-500/30">
                Interview Arena
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
                href="/projects"
                className="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition"
              >
                Practical Projects
              </Link>
              <Link
                href="/interview"
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-white font-semibold transition"
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

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* Banner */}
        <section className="bg-gradient-to-r from-pink-950/40 via-purple-950/30 to-slate-900 border border-slate-800 rounded-2xl p-8 mb-8 shadow-xl">
          <div className="max-w-3xl">
            <span className="text-xs font-bold uppercase tracking-wider text-pink-400">
              Technical Interview Simulation
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-1 mb-3">
              Algorithms & Data Structures Arena
            </h1>
            <p className="text-slate-300 text-sm leading-relaxed">
              Practice classic technical interview problems under realistic timed constraints. Every problem is evaluated against exhaustive hidden edge cases and includes Socratic interviewer prompts.
            </p>
          </div>
        </section>

        {/* Filter Pills */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            {["All", "Easy", "Medium", "Hard"].map((lvl) => (
              <button
                key={lvl}
                onClick={() => setFilterDifficulty(lvl)}
                className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition ${
                  filterDifficulty === lvl
                    ? "bg-pink-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {lvl} ({lvl === "All" ? problems.length : problems.filter((p) => p.difficulty === lvl).length})
              </button>
            ))}
          </div>

          <span className="text-xs text-slate-400 font-medium">
            10 Top Tier FAANG / Technical Interview Problems
          </span>
        </div>

        {/* Problems List */}
        {loading ? (
          <div className="text-center py-20 text-slate-400">Loading interview problems...</div>
        ) : (
          <div className="space-y-3">
            {filtered.map((prob, idx) => (
              <div
                key={prob.id}
                className="bg-slate-900/60 border border-slate-800 hover:border-pink-500/40 rounded-xl p-4 sm:p-5 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="flex items-start sm:items-center gap-4 flex-1 min-w-0">
                  <span className="text-xs font-mono font-bold text-slate-500 bg-slate-950 px-2.5 py-1 rounded border border-slate-800">
                    #{idx + 1}
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <h2 className="text-base font-bold text-white truncate">{prob.title}</h2>
                      <span
                        className={`text-[11px] px-2 py-0.5 rounded-full border font-semibold ${
                          difficultyBadge[prob.difficulty as keyof typeof difficultyBadge] || ""
                        }`}
                      >
                        {prob.difficulty}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="text-pink-400 font-medium">{prob.category}</span>
                      <span>•</span>
                      <span>⏱️ {prob.time_limit_minutes} Min Limit</span>
                    </div>
                  </div>
                </div>

                <Link
                  href={`/interview/${prob.id}`}
                  className="bg-pink-600 hover:bg-pink-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-md whitespace-nowrap self-start sm:self-center"
                >
                  Start Mock Interview →
                </Link>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
