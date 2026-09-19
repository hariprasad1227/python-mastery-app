"use client";

import React, { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import {
  api,
  UserProfile,
  Module,
  ExecuteResult,
  LevelItem
} from "../lib/api";
import AuthModal from "@/components/AuthModal";
import RankDashboard from "@/components/RankDashboard";
import LevelFinalTestCockpit from "@/components/LevelFinalTestCockpit";
import {
  Sparkles,
  BookOpen,
  Code2,
  Terminal,
  Play,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Search,
  Award,
  Layers,
  Briefcase,
  Flame,
  ShieldCheck,
  ArrowRight,
  Check,
  User,
  LogOut,
  Cpu,
  BrainCircuit,
  GraduationCap,
  Lock
} from "lucide-react";

export default function HomePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [curriculum, setCurriculum] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTrack, setSelectedTrack] = useState<number | "all">("all");
  const [statusFilter, setStatusFilter] = useState<"all" | "unlocked" | "completed" | "locked">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedTracks, setExpandedTracks] = useState<Record<number, boolean>>({ 1: true });
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [levels, setLevels] = useState<LevelItem[]>([]);
  const [activeFinalTestLevel, setActiveFinalTestLevel] = useState<number | null>(null);

  // Live Homepage Playground state
  const playgroundPresets = [
    {
      name: "1. Variables & F-Strings",
      code: `learner_name = "Alex"\nskill_level = "Python Master"\nxp = 500\n\nmessage = f"Welcome {learner_name}! Level: {skill_level} (XP: {xp:,})"\nprint(message)\nprint(f"Type of learner_name: {type(learner_name).__name__}")`
    },
    {
      name: "2. Fibonacci Sequence",
      code: `def generate_fibonacci(n: int) -> list[int]:\n    sequence = [0, 1]\n    for _ in range(2, n):\n        sequence.append(sequence[-1] + sequence[-2])\n    return sequence[:n]\n\nprint("First 8 Fibonacci numbers:")\nprint(generate_fibonacci(8))`
    },
    {
      name: "3. OOP Bank Account",
      code: `class BankAccount:\n    def __init__(self, owner: str, balance: float = 0.0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount: float):\n        self.balance += amount\n        return f"Deposited \${amount:.2f}. Balance: \${self.balance:.2f}"\n\nacc = BankAccount("Sita", 150.0)\nprint(acc.deposit(75.50))`
    }
  ];

  const [playgroundCode, setPlaygroundCode] = useState(playgroundPresets[0].code);
  const [playgroundOutput, setPlaygroundOutput] = useState("Click \"Run Python Sandbox\" to execute code live.");
  const [playgroundRunning, setPlaygroundRunning] = useState(false);

  const loadData = async () => {
    try {
      const [profData, currData, levelsData] = await Promise.all([
        api.getProfile().catch(() => null),
        api.getCurriculum().catch(() => []),
        api.getLevels().catch(() => [])
      ]);
      if (profData) setProfile(profData);
      if (currData) setCurriculum(currData);
      if (levelsData) setLevels(levelsData);
    } catch (err) {
      console.error("Error loading homepage data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const toggleTrack = (trackNum: number) => {
    setExpandedTracks((prev) => ({
      ...prev,
      [trackNum]: !prev[trackNum]
    }));
  };

  const handleRunPlayground = async () => {
    setPlaygroundRunning(true);
    setPlaygroundOutput("Submitting to isolated Python sandbox...");
    try {
      // Execute through challenge 1 or sandbox runner
      const res: ExecuteResult = await api.executeCode({
        challenge_id: "chal-1",
        code: playgroundCode
      });
      let out = "";
      if (res.stdout) out += res.stdout;
      if (res.stderr) out += "\nErrors:\n" + res.stderr;
      out += `\n\n[Sandbox verified in ${res.execution_time_ms}ms | Memory & AST Protected]`;
      setPlaygroundOutput(out.trim());
    } catch (err: any) {
      setPlaygroundOutput("Execution Result:\n" + (err.message || "Sandbox completed execution."));
    } finally {
      setPlaygroundRunning(false);
    }
  };

  // Metrics calculations
  const totalChallenges = useMemo(() => {
    return curriculum.reduce((acc, mod) => acc + mod.challenges.length, 0) || 100;
  }, [curriculum]);

  const completedCount = useMemo(() => {
    return curriculum.reduce((acc, mod) => {
      return acc + mod.challenges.filter((c) => c.status === "completed").length;
    }, 0);
  }, [curriculum]);

  const completionPct = Math.round((completedCount / totalChallenges) * 100);

  // Filtered curriculum
  const filteredCurriculum = useMemo(() => {
    return curriculum
      .filter((mod) => selectedTrack === "all" || mod.level_number === selectedTrack)
      .map((mod) => {
        let matches = mod.challenges;
        if (statusFilter !== "all") {
          matches = matches.filter((c) => {
            if (statusFilter === "unlocked") return c.status !== "locked";
            return c.status === statusFilter;
          });
        }
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          matches = matches.filter(
            (c) => c.title.toLowerCase().includes(q) || c.instructions.toLowerCase().includes(q)
          );
        }
        return {
          ...mod,
          filteredChallenges: matches
        };
      })
      .filter((mod) => mod.filteredChallenges.length > 0 || (searchQuery === "" && statusFilter === "all"));
  }, [curriculum, selectedTrack, statusFilter, searchQuery]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">
      {/* Sticky Global Navigation Bar */}
      <header className="border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="text-xl font-black bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent">
                  Python Mastery
                </span>
                <span className="hidden sm:inline-block ml-2 text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded-full">
                  Learning Platform
                </span>
              </div>
            </Link>

            <nav className="hidden lg:flex items-center gap-1 text-xs font-medium">
              <a
                href="#curriculum"
                className="px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition"
              >
                10-Track Curriculum
              </a>
              <Link
                href="/lessons"
                className="px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition"
              >
                Lessons & Theory
              </Link>
              <Link
                href="/projects"
                className="px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition"
              >
                Practical Projects
              </Link>
              <Link
                href="/interview"
                className="px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/60 transition"
              >
                Interview Arena
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            {/* Streak & XP Indicator */}
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 text-xs font-semibold text-orange-400 bg-orange-950/30 border border-orange-500/20 px-2.5 py-1 rounded-full">
                <Flame className="w-3.5 h-3.5 text-orange-400" />
                <span>{profile?.current_streak || 0}d Streak</span>
              </div>
              <div className="flex items-center gap-1 text-xs font-semibold text-emerald-400 bg-emerald-950/30 border border-emerald-500/20 px-2.5 py-1 rounded-full">
                <Award className="w-3.5 h-3.5 text-emerald-400" />
                <span>{profile?.total_xp || 0} XP</span>
              </div>
            </div>

            {/* Auth Action */}
            {profile && profile.username !== "guest" ? (
              <div className="flex items-center gap-2 text-xs">
                <span className="font-semibold text-slate-200 hidden sm:inline">
                  {profile.display_name || profile.username}
                </span>
                <button
                  onClick={() => {
                    api.clearToken();
                    window.location.reload();
                  }}
                  title="Log out"
                  className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => setAuthModalOpen(true)}
                className="text-xs font-semibold px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm shadow-indigo-900/30 flex items-center gap-1.5"
              >
                <User className="w-3.5 h-3.5" />
                <span>Sign In / Register</span>
              </button>
            )}
          </div>
        </div>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="relative overflow-hidden pt-12 pb-20 border-b border-slate-800/60 bg-gradient-to-b from-slate-900/40 via-slate-950 to-slate-950">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.18),rgba(255,255,255,0))]" />

          <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              {/* Left Column: Headline & CTAs */}
              <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                  <span>The Complete 2026 Python Master Curriculum</span>
                </div>

                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-[1.1]">
                  Master Python. <br />
                  <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
                    From Day 1 to Senior Engineer.
                  </span>
                </h1>

                <p className="text-slate-300 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto lg:mx-0">
                  Stop passively watching videos. Master Python through <strong>structured lessons</strong>, real-world analogies, line-by-line code breakdowns, concept quizzes, <strong>100 guided challenges</strong>, 4 production capstones, and 10 FAANG-grade DSA mock interviews.
                </p>

                {/* Main Action Buttons */}
                <div className="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2">
                  <Link
                    href="/learn/chal-1"
                    className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/25 flex items-center gap-2 transform hover:-translate-y-0.5 transition-all"
                  >
                    <span>Start Learning Free (Level 1)</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                  <a
                    href="#curriculum"
                    className="px-5 py-3.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/60 text-slate-200 font-semibold text-sm transition flex items-center gap-2"
                  >
                    <span>Explore 100 Challenges</span>
                    <ChevronDown className="w-4 h-4 text-slate-400" />
                  </a>
                  <Link
                    href="/lessons"
                    className="px-5 py-3.5 rounded-xl bg-slate-900/60 border border-indigo-500/30 hover:border-indigo-500/60 text-indigo-300 font-semibold text-sm transition flex items-center gap-2"
                  >
                    <BookOpen className="w-4 h-4" />
                    <span>Lessons Library</span>
                  </Link>
                </div>

                {/* Badges / Highlights */}
                <div className="pt-4 flex flex-wrap items-center justify-center lg:justify-start gap-4 text-xs text-slate-400">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>100 Progressive Levels</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>12-Step Pedagogical Method</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>Server-Secured Python Sandbox</span>
                  </div>
                </div>
              </div>

              {/* Right Column: Live Python Playground Component */}
              <div className="lg:col-span-5">
                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden backdrop-blur-sm">
                  {/* Window Bar */}
                  <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                      <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                      <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                      <span className="text-xs font-mono text-slate-400 ml-2">sandbox_playground.py</span>
                    </div>

                    <button
                      onClick={handleRunPlayground}
                      disabled={playgroundRunning}
                      className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-md shadow-emerald-950 disabled:opacity-50"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      <span>{playgroundRunning ? "Running..." : "Run Code"}</span>
                    </button>
                  </div>

                  {/* Preset Selector */}
                  <div className="px-4 py-2 bg-slate-900/60 border-b border-slate-800/80 flex items-center gap-2 overflow-x-auto text-xs">
                    <span className="text-slate-500 font-semibold uppercase text-[10px]">Presets:</span>
                    {playgroundPresets.map((p, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setPlaygroundCode(p.code);
                          setPlaygroundOutput("Click \"Run Code\" to execute this preset.");
                        }}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[11px] whitespace-nowrap transition"
                      >
                        {p.name}
                      </button>
                    ))}
                  </div>

                  {/* Code Editor Area */}
                  <div className="p-4 bg-slate-950 font-mono text-xs text-emerald-300">
                    <textarea
                      value={playgroundCode}
                      onChange={(e) => setPlaygroundCode(e.target.value)}
                      rows={8}
                      spellCheck="false"
                      className="w-full bg-transparent resize-none focus:outline-none leading-relaxed text-emerald-400 font-mono"
                    />
                  </div>

                  {/* Output Terminal */}
                  <div className="border-t border-slate-800 p-3 bg-black/60">
                    <div className="text-[10px] font-mono text-slate-500 uppercase tracking-wider mb-1 flex items-center gap-1">
                      <Terminal className="w-3 h-3" />
                      Output Terminal:
                    </div>
                    <pre className="text-xs font-mono text-sky-300 whitespace-pre-wrap max-h-28 overflow-y-auto leading-relaxed">
                      {playgroundOutput}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* PLATFORM METRICS COUNTER */}
        <section className="border-b border-slate-800/80 bg-slate-900/30 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div className="space-y-1">
                <div className="text-3xl sm:text-4xl font-black text-indigo-400">10</div>
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Comprehensive Tracks
                </div>
              </div>
              <div className="space-y-1">
                <div className="text-3xl sm:text-4xl font-black text-purple-400">100</div>
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Curated Coding Levels
                </div>
              </div>
              <div className="space-y-1">
                <div className="text-3xl sm:text-4xl font-black text-emerald-400">4</div>
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Production Capstones
                </div>
              </div>
              <div className="space-y-1">
                <div className="text-3xl sm:text-4xl font-black text-pink-400">10</div>
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Technical Mock Arenas
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* RANK & PERFORMANCE PILLAR DASHBOARD */}
        <section className="py-12 border-b border-slate-800/80 bg-slate-950/90 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 border border-amber-500/20 px-3 py-1 rounded-full">
                  Skill Tier & Progression Cockpit
                </span>
                <h2 className="text-2xl sm:text-3xl font-black text-white mt-2">
                  Performance Rank & Evaluation Engine
                </h2>
                <p className="text-xs sm:text-sm text-slate-400 mt-1">
                  Three independent pillars: <strong>Level</strong> (curriculum roadmap), <strong>Rank</strong> (performance score 0–100), and <strong>XP</strong> (effort points).
                </p>
              </div>
            </div>

            <RankDashboard onRefreshProfile={loadData} />
          </div>
        </section>

        {/* THE 12-STEP EDUCATIONAL PEDAGOGY */}
        <section className="py-16 border-b border-slate-800/60 bg-slate-950">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-full">
                Learning-First Experience
              </span>
              <h2 className="text-3xl font-extrabold text-white mt-3 mb-3">
                How You Learn on Python Mastery
              </h2>
              <p className="text-sm text-slate-400 leading-relaxed">
                You are never thrown directly into a coding task. Every concept follows an empirically proven pedagogical pipeline designed to build rock-solid intuitions.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center text-amber-400 font-bold">
                  💡
                </div>
                <h3 className="font-bold text-white text-base">1. Real-Life Analogies</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Before touching syntax, connect abstract computer science ideas to familiar everyday things (labeled storage boxes, recipe cards, building blueprints).
                </p>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold">
                  🧩
                </div>
                <h3 className="font-bold text-white text-base">2. Syntax & Line-by-Line</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Break down language keywords token-by-token, then examine fully functioning code examples accompanied by detailed line-by-line annotations.
                </p>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-rose-500/20 flex items-center justify-center text-rose-400 font-bold">
                  ⚠️
                </div>
                <h3 className="font-bold text-white text-base">3. Pitfalls & Mistake Diffs</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Study side-by-side Incorrect vs Correct code blocks to see exactly why common traps fail and how to write clean, idiomatic PEP 8 Python.
                </p>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center text-purple-400 font-bold">
                  📝
                </div>
                <h3 className="font-bold text-white text-base">4. Concept Check Quizzes</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Validate conceptual retention with multiple-choice questions and instant explanations. Pass the quiz to unlock +25 bonus XP before coding!
                </p>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold">
                  🛡️
                </div>
                <h3 className="font-bold text-white text-base">5. Isolated Code Sandbox</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Implement solutions against rigorous public and hidden server assertions inside an AST-secured, timeout-protected Python execution runner.
                </p>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center text-pink-400 font-bold">
                  🤖
                </div>
                <h3 className="font-bold text-white text-base">6. Socratic AI Mentor</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Stuck on a tricky edge case? Request 3 tiers of Socratic hints that guide your thinking step-by-step without spoiling the answer.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CURRICULUM EXPLORER */}
        <section id="curriculum" className="py-16 bg-slate-900/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                  Full 100-Level Roadmap
                </span>
                <h2 className="text-3xl font-extrabold text-white mt-1">
                  10 Comprehensive Tracks
                </h2>
                <p className="text-xs sm:text-sm text-slate-400 mt-1">
                  Progressive difficulty from basic expressions to concurrency, algorithms, and metaprogramming.
                </p>
              </div>

              {/* Overall Progress Indicator */}
              <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl min-w-[240px]">
                <div className="flex items-center justify-between text-xs mb-1.5 font-semibold">
                  <span className="text-slate-300">Curriculum Progress</span>
                  <span className="text-emerald-400">{completedCount}/{totalChallenges} ({completionPct}%)</span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500"
                    style={{ width: `\${Math.max(completionPct, 1)}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Filter & Search Toolbar */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3.5 mb-6 flex flex-col md:flex-row gap-3 items-center justify-between">
              {/* Search */}
              <div className="relative w-full md:w-80">
                <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Search challenges, concepts, or keywords..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              {/* Status Filter Pills */}
              <div className="flex items-center gap-1 text-xs self-start md:self-auto overflow-x-auto">
                <button
                  onClick={() => setStatusFilter("all")}
                  className={`px-3 py-1 rounded-md transition font-medium \${
                    statusFilter === "all" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                  }`}
                >
                  All Status
                </button>
                <button
                  onClick={() => setStatusFilter("unlocked")}
                  className={`px-3 py-1 rounded-md transition font-medium \${
                    statusFilter === "unlocked" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Available
                </button>
                <button
                  onClick={() => setStatusFilter("completed")}
                  className={`px-3 py-1 rounded-md transition font-medium \${
                    statusFilter === "completed" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Completed
                </button>
              </div>
            </div>

            {/* Curriculum Modules Accordion List */}
            {loading ? (
              <div className="text-center py-16 text-slate-500 text-sm">
                Loading 10-Track Curriculum...
              </div>
            ) : filteredCurriculum.length === 0 ? (
              <div className="text-center py-16 bg-slate-900/40 rounded-2xl border border-slate-800 text-slate-400 text-sm">
                No challenges match your search or filter criteria.
              </div>
            ) : (
              <div className="space-y-4">
                {filteredCurriculum.map((moduleItem) => {
                  const isExpanded = !!expandedTracks[moduleItem.level_number];
                  const modCompleted = moduleItem.challenges.filter((c) => c.status === "completed").length;
                  const modTotal = moduleItem.challenges.length;

                  return (
                    <div
                      key={moduleItem.id}
                      className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden transition-all shadow-md"
                    >
                      {/* Track Header */}
                      <button
                        onClick={() => toggleTrack(moduleItem.level_number)}
                        className="w-full p-4 sm:p-5 flex items-center justify-between text-left hover:bg-slate-800/40 transition"
                      >
                        {(() => {
                          const lvlInfo = levels.find((l) => l.level_number === moduleItem.level_number);
                          return (
                            <>
                              <div className="flex items-center gap-4">
                                <div className={`w-11 h-11 rounded-xl flex items-center justify-center font-black text-sm shrink-0 border ${
                                  lvlInfo?.completed
                                    ? "bg-emerald-600/20 border-emerald-500/40 text-emerald-300"
                                    : lvlInfo?.unlocked
                                    ? "bg-indigo-600/20 border-indigo-500/40 text-indigo-300"
                                    : "bg-slate-900 border-slate-800 text-slate-500"
                                }`}>
                                  L{moduleItem.level_number}
                                </div>
                                <div>
                                  <div className="flex items-center gap-2 flex-wrap">
                                    <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                                      Level {moduleItem.level_number}
                                    </span>
                                    <span className="text-slate-600">•</span>
                                    <span className="text-xs text-slate-300">
                                      {lvlInfo ? `${lvlInfo.topics_completed}/${lvlInfo.topics_total} Topics Mastered` : `${modCompleted}/${modTotal} Completed`}
                                    </span>
                                    <span className="text-slate-600">•</span>
                                    <span className="text-[11px] text-slate-400 font-mono">
                                      XP Req: {lvlInfo ? lvlInfo.xp_required.toLocaleString() : 0} XP
                                    </span>

                                    {lvlInfo?.completed ? (
                                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                                        <CheckCircle2 className="w-3 h-3" /> Level Complete
                                      </span>
                                    ) : lvlInfo?.unlocked ? (
                                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                                        Active Level
                                      </span>
                                    ) : (
                                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400 border border-slate-700 flex items-center gap-1">
                                        <Lock className="w-3 h-3" /> Locked
                                      </span>
                                    )}
                                  </div>
                                  <h3 className="text-base sm:text-lg font-bold text-white mt-0.5">
                                    {moduleItem.title}
                                  </h3>
                                  <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">
                                    {moduleItem.description}
                                  </p>
                                </div>
                              </div>

                              <div className="flex items-center gap-3 shrink-0">
                                {/* Level Final Test Button */}
                                {lvlInfo?.final_test_passed ? (
                                  <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      setActiveFinalTestLevel(moduleItem.level_number);
                                    }}
                                    className="hidden sm:flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-lg bg-emerald-600/20 border border-emerald-500/40 text-emerald-300 hover:bg-emerald-600/30 transition"
                                  >
                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                                    <span>Final Test Passed ({lvlInfo.final_test_score || 100}%)</span>
                                  </button>
                                ) : lvlInfo?.can_take_final_test ? (
                                  <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      setActiveFinalTestLevel(moduleItem.level_number);
                                    }}
                                    className="hidden sm:flex items-center gap-1.5 text-xs font-bold px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-600/20 hover:brightness-110 transition animate-pulse"
                                  >
                                    <Award className="w-3.5 h-3.5 text-amber-300" />
                                    <span>Final Test Ready (+250 XP)</span>
                                  </button>
                                ) : lvlInfo?.unlocked ? (
                                  <span className="hidden sm:inline-block text-[11px] text-slate-500 bg-slate-900 border border-slate-800 px-2.5 py-1 rounded-lg">
                                    Final Test: Pass {lvlInfo?.topics_completed || 0}/10 Topics
                                  </span>
                                ) : null}

                                <Link
                                  href={`/lessons`}
                                  onClick={(e) => e.stopPropagation()}
                                  className="hidden sm:flex items-center gap-1 text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                                >
                                  <BookOpen className="w-3.5 h-3.5" />
                                  <span>Read Guide</span>
                                </Link>

                                {isExpanded ? (
                                  <ChevronDown className="w-5 h-5 text-slate-400" />
                                ) : (
                                  <ChevronRight className="w-5 h-5 text-slate-400" />
                                )}
                              </div>
                            </>
                          );
                        })()}
                      </button>

                      {/* Challenges Sub-List */}
                      {isExpanded && (
                        <div className="p-4 sm:p-5 pt-0 border-t border-slate-800/60 grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
                          {moduleItem.filteredChallenges.map((chal, cIndex) => {
                            const isDone = chal.status === "completed" || chal.status === "passed";
                            const isExamReady = chal.status === "exam_available";
                            const isInProgress = chal.status === "in_progress";
                            const isLocked = chal.status === "locked";

                            return (
                              <Link
                                key={chal.id}
                                href={`/learn/${chal.id}`}
                                className={`p-3.5 rounded-xl border transition flex items-start justify-between group ${
                                  isDone
                                    ? "bg-emerald-950/20 border-emerald-900/50 hover:border-emerald-700"
                                    : isExamReady
                                    ? "bg-indigo-950/30 border-indigo-500/50 hover:border-indigo-400 shadow-md shadow-indigo-950/30"
                                    : isInProgress
                                    ? "bg-sky-950/20 border-sky-800/50 hover:border-sky-600"
                                    : !isLocked
                                    ? "bg-slate-950/70 border-slate-800 hover:border-indigo-500/60 hover:bg-slate-900"
                                    : "bg-slate-950/40 border-slate-900 text-slate-500 hover:border-slate-800"
                                }`}
                              >
                                <div className="space-y-1 pr-2">
                                  <div className="flex items-center gap-2">
                                    <span className={`text-[11px] font-mono font-semibold ${
                                      isDone ? "text-emerald-400" : isExamReady ? "text-indigo-400" : "text-slate-400"
                                    }`}>
                                      L{chal.id.replace("chal-", "")}
                                    </span>
                                    <span className="text-xs font-bold text-slate-200 group-hover:text-white">
                                      {chal.title}
                                    </span>
                                  </div>
                                  <p className="text-[11px] text-slate-400 line-clamp-1">
                                    {chal.instructions}
                                  </p>
                                </div>

                                <div className="flex flex-col items-end gap-1.5 shrink-0">
                                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-emerald-400">
                                    +{chal.xp_reward} XP
                                  </span>
                                  {isDone ? (
                                    <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-0.5">
                                      <Check className="w-3 h-3" /> Passed
                                    </span>
                                  ) : isExamReady ? (
                                    <span className="text-[10px] text-indigo-300 font-bold bg-indigo-500/20 px-2 py-0.5 rounded flex items-center gap-1 animate-pulse">
                                      📝 Exam Ready
                                    </span>
                                  ) : isInProgress ? (
                                    <span className="text-[10px] text-sky-400 font-medium">
                                      In Progress
                                    </span>
                                  ) : isLocked ? (
                                    <span className="text-[10px] text-slate-500 font-medium flex items-center gap-1">
                                      <Lock className="w-3 h-3" /> Locked
                                    </span>
                                  ) : (
                                    <span className="text-[10px] text-indigo-400 font-medium">
                                      Available
                                    </span>
                                  )}
                                </div>
                              </Link>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>

        {/* PROJECTS & INTERVIEW PROMO */}
        <section className="py-16 border-t border-slate-800/60 bg-slate-950">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Practical Projects Card */}
              <div className="bg-gradient-to-br from-indigo-950/40 via-slate-900 to-slate-950 border border-indigo-500/30 rounded-2xl p-8 space-y-4 shadow-xl">
                <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                  <Briefcase className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold text-white">4 Practical Software Capstones</h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  Go beyond algorithms. Build end-to-end applications: a CLI Task Manager, a Weather API Client, a Log Analyzer, and a Lightweight Async ORM.
                </p>
                <div className="pt-2">
                  <Link
                    href="/projects"
                    className="inline-flex items-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-md"
                  >
                    <span>View Projects Workbench</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>

              {/* DSA Interview Arena Card */}
              <div className="bg-gradient-to-br from-purple-950/40 via-slate-900 to-slate-950 border border-purple-500/30 rounded-2xl p-8 space-y-4 shadow-xl">
                <div className="w-12 h-12 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
                  <BrainCircuit className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold text-white">10 Timed FAANG Mock Arenas</h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  Practice high-stakes coding interviews with hard time limits, hidden edge-case inputs, and runtime performance checks for Top-Tier tech companies.
                </p>
                <div className="pt-2">
                  <Link
                    href="/interview"
                    className="inline-flex items-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white transition shadow-md"
                  >
                    <span>Enter Interview Cockpit</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Global Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-12 text-slate-500 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-indigo-600 to-pink-500 flex items-center justify-center text-white font-bold text-xs">
              P
            </div>
            <span className="font-bold text-slate-300 text-sm">Python Mastery Platform</span>
          </div>

          <div className="flex flex-wrap items-center gap-6">
            <Link href="/" className="hover:text-slate-300 transition">Curriculum</Link>
            <Link href="/lessons" className="hover:text-slate-300 transition">Lessons & Theory</Link>
            <Link href="/projects" className="hover:text-slate-300 transition">Projects</Link>
            <Link href="/interview" className="hover:text-slate-300 transition">Interview Arena</Link>
          </div>

          <div>
            © 2026 Python Mastery. Built with FastAPI, Next.js, and Isolated Python Sandbox.
          </div>
        </div>
      </footer>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onSuccess={(newProf) => {
          setProfile(newProf);
        }}
      />

      {/* Level Final Test Cockpit Modal */}
      {activeFinalTestLevel && (
        <LevelFinalTestCockpit
          levelNumber={activeFinalTestLevel}
          onClose={() => setActiveFinalTestLevel(null)}
          onLevelCompleted={() => {
            loadData();
          }}
        />
      )}
    </div>
  );
}
