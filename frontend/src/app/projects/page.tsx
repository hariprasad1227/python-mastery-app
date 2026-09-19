"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api, ProjectItem, UserProfile } from "@/lib/api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [projData, profData] = await Promise.all([
          api.getProjects(),
          api.getProfile()
        ]);
        setProjects(projData);
        setProfile(profData);
      } catch (err) {
        console.error("Failed to load projects:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const difficultyColors = {
    beginner: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    intermediate: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    advanced: "bg-purple-500/10 text-purple-400 border-purple-500/20"
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Top Nav */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-3">
              <span className="text-2xl font-black bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Python Mastery
              </span>
              <span className="text-[11px] font-semibold bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded-full border border-purple-500/30">
                Projects Track
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
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-white font-semibold transition"
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

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* Banner */}
        <section className="bg-gradient-to-r from-purple-950/40 via-indigo-950/30 to-slate-900 border border-slate-800 rounded-2xl p-8 mb-10 shadow-xl">
          <div className="max-w-3xl">
            <span className="text-xs font-bold uppercase tracking-wider text-purple-400">
              Real-World Engineering
            </span>
            <h1 className="text-3xl font-extrabold text-white mt-1 mb-3">
              Practical Python Software Projects
            </h1>
            <p className="text-slate-300 text-sm leading-relaxed">
              Transition from individual algorithms to building complete, maintainable software systems. Each project includes production specifications, architectural guidance, and automated sandbox validation tests.
            </p>
          </div>
        </section>

        {/* Projects Grid */}
        {loading ? (
          <div className="text-center py-20 text-slate-400">Loading practical projects...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {projects.map((proj, idx) => (
              <div
                key={proj.id}
                className="bg-slate-900/60 border border-slate-800 hover:border-purple-500/40 rounded-xl p-6 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-slate-400">
                      PROJECT #{idx + 1}
                    </span>
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-xs px-2.5 py-0.5 rounded-full border capitalize font-semibold ${
                          difficultyColors[proj.difficulty]
                        }`}
                      >
                        {proj.difficulty}
                      </span>
                      <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full font-bold">
                        +{proj.xp_reward} XP
                      </span>
                    </div>
                  </div>

                  <h2 className="text-xl font-bold text-white mb-2">{proj.title}</h2>
                  <p className="text-slate-400 text-xs leading-relaxed mb-4">
                    {proj.description}
                  </p>

                  {/* Requirements List */}
                  <div className="space-y-1.5 mb-5 bg-slate-950/60 p-3.5 rounded-lg border border-slate-800/80">
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">
                      Key Deliverables
                    </div>
                    {proj.requirements.map((req, rIdx) => (
                      <div key={rIdx} className="text-xs text-slate-300 flex items-start gap-2">
                        <span className="text-purple-400 text-xs">•</span>
                        <span>{req}</span>
                      </div>
                    ))}
                  </div>

                  {/* Tech Stack Tags */}
                  <div className="flex flex-wrap gap-1.5 mb-6">
                    {proj.tech_stack.map((tag) => (
                      <span
                        key={tag}
                        className="text-[11px] font-mono bg-slate-800/80 text-slate-300 px-2 py-0.5 rounded border border-slate-700/60"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                  <span className="text-xs text-slate-400">⏱️ Est. {proj.estimated_hours} Hours</span>
                  <Link
                    href={`/projects/${proj.id}`}
                    className="bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-md flex items-center gap-1"
                  >
                    <span>Open Workbench</span>
                    <span>→</span>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
