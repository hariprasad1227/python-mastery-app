"use client";

import React, { useState, useEffect } from "react";
import {
  Award,
  Shield,
  TrendingUp,
  Flame,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Calendar,
  Sparkles,
  ChevronRight,
  History,
  FileText,
  Activity,
  Code2,
  Lock,
  ArrowUpRight
} from "lucide-react";
import {
  api,
  RankProfile,
  RankHistoryItem,
  PeriodicTestItem,
  PeriodicTestSubmitResult
} from "@/lib/api";
import PeriodicTestCockpit from "./PeriodicTestCockpit";

interface RankDashboardProps {
  onRefreshProfile?: () => void;
}

const RANK_DETAILS = {
  GOLD: {
    label: "GOLD TIER",
    icon: "🥇",
    color: "from-amber-500 to-yellow-600",
    textColor: "text-amber-400",
    borderColor: "border-amber-500/40",
    bgColor: "bg-amber-500/10",
    range: "60 – 74",
    badgeDesc: "Solid foundation in Python fundamentals."
  },
  PLATINUM: {
    label: "PLATINUM TIER",
    icon: "💎",
    color: "from-cyan-500 to-blue-600",
    textColor: "text-cyan-400",
    borderColor: "border-cyan-500/40",
    bgColor: "bg-cyan-500/10",
    range: "75 – 84",
    badgeDesc: "Proficient problem solver with strong algorithmic consistency."
  },
  DIAMOND: {
    label: "DIAMOND TIER",
    icon: "💠",
    color: "from-indigo-500 to-purple-600",
    textColor: "text-indigo-400",
    borderColor: "border-indigo-500/40",
    bgColor: "bg-indigo-500/10",
    range: "85 – 94",
    badgeDesc: "High-accuracy developer with advanced architectural grasp."
  },
  MASTER: {
    label: "MASTER TIER",
    icon: "👑",
    color: "from-emerald-500 via-amber-400 to-yellow-500",
    textColor: "text-yellow-400",
    borderColor: "border-yellow-500/50",
    bgColor: "bg-yellow-500/10",
    range: "95 – 100",
    badgeDesc: "Elite Python engineer: flawless execution, tests, and capstone."
  }
};

export default function RankDashboard({ onRefreshProfile }: RankDashboardProps) {
  const [profile, setProfile] = useState<RankProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [periodicTests, setPeriodicTests] = useState<PeriodicTestItem[]>([]);
  const [activeTestId, setActiveTestId] = useState<string | null>(null);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [rankHistory, setRankHistory] = useState<RankHistoryItem[]>([]);
  const [showTestsModal, setShowTestsModal] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rankData, testsData] = await Promise.all([
        api.getRankProfile(),
        api.getPeriodicTests().catch(() => [])
      ]);
      setProfile(rankData);
      setPeriodicTests(testsData);
    } catch (err) {
      console.error("Failed to load rank profile", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenHistory = async () => {
    try {
      const hist = await api.getRankHistory();
      setRankHistory(hist);
      setShowHistoryModal(true);
    } catch (err) {
      console.error("Failed to fetch rank history", err);
    }
  };

  const handleTestFinished = (res: PeriodicTestSubmitResult) => {
    loadData();
    if (onRefreshProfile) onRefreshProfile();
  };

  if (loading && !profile) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 text-center animate-pulse">
        <div className="h-6 w-48 bg-slate-800 rounded mx-auto mb-4" />
        <div className="h-20 w-full bg-slate-800 rounded" />
      </div>
    );
  }

  if (!profile) return null;

  const currentRankKey = profile.current_rank as keyof typeof RANK_DETAILS || "GOLD";
  const rankMeta = RANK_DETAILS[currentRankKey] || RANK_DETAILS.GOLD;

  return (
    <div className="space-y-6">
      {/* Top Banner Card: Rank & Performance Score */}
      <div className={`relative overflow-hidden rounded-2xl border ${rankMeta.borderColor} bg-slate-900/90 backdrop-blur-md p-6 sm:p-8 shadow-xl`}>
        {/* Glow effect */}
        <div className={`absolute -right-20 -top-20 w-64 h-64 rounded-full blur-3xl opacity-20 bg-gradient-to-br ${rankMeta.color}`} />

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          {/* Left: Rank Tier */}
          <div className="flex items-center gap-5">
            <div className={`w-20 h-20 rounded-2xl flex items-center justify-center text-4xl border ${rankMeta.borderColor} ${rankMeta.bgColor} shadow-inner`}>
              {rankMeta.icon}
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold tracking-widest text-slate-400 uppercase">
                  Performance Rank
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${rankMeta.bgColor} ${rankMeta.textColor} border ${rankMeta.borderColor}`}>
                  Tier {profile.current_rank}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-2">
                {rankMeta.label}
              </h1>
              <p className="text-xs sm:text-sm text-slate-400 max-w-md leading-relaxed">
                {rankMeta.badgeDesc}
              </p>
            </div>
          </div>

          {/* Right: Performance Score Gauge */}
          <div className="flex items-center gap-4 bg-slate-950/70 border border-slate-800 rounded-2xl p-4 sm:p-5 w-full md:w-auto">
            <div className="text-right space-y-0.5">
              <div className="text-xs text-slate-400 font-medium">Performance Score</div>
              <div className="text-3xl sm:text-4xl font-black text-white flex items-baseline justify-end gap-1">
                <span>{profile.performance_score.toFixed(1)}</span>
                <span className="text-sm font-semibold text-slate-500">/ 100</span>
              </div>
              <div className="text-[11px] text-slate-400">
                Target: {rankMeta.range} pts
              </div>
            </div>

            {/* Circular score gauge */}
            <div className="relative w-16 h-16 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-slate-800"
                  strokeWidth="3.5"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className={rankMeta.textColor}
                  strokeDasharray={`${profile.performance_score}, 100`}
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <Activity className={`w-6 h-6 absolute ${rankMeta.textColor}`} />
            </div>
          </div>
        </div>

        {/* 5-Component Performance Score Breakdown */}
        <div className="mt-8 pt-6 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {/* 1. Topic Exam Avg */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Topic Exams</span>
              <span className="font-semibold text-indigo-400">30%</span>
            </div>
            <div className="text-lg font-bold text-white">
              {profile.components.topic_exam_avg.toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Best score across topics</div>
          </div>

          {/* 2. Coding Performance */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Coding Ratio</span>
              <span className="font-semibold text-emerald-400">30%</span>
            </div>
            <div className="text-lg font-bold text-white">
              {profile.components.coding_performance.toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Accuracy & pass rate</div>
          </div>

          {/* 3. Weekly Tests Avg */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Weekly Tests</span>
              <span className="font-semibold text-amber-400">15%</span>
            </div>
            <div className="text-lg font-bold text-white">
              {profile.components.weekly_test_avg.toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Periodic test average</div>
          </div>

          {/* 4. Monthly Tests Avg */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Monthly Exams</span>
              <span className="font-semibold text-purple-400">15%</span>
            </div>
            <div className="text-lg font-bold text-white">
              {profile.components.monthly_test_avg.toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Deep milestone tests</div>
          </div>

          {/* 5. Consistency Score */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1 col-span-2 sm:col-span-1">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Consistency</span>
              <span className="font-semibold text-rose-400">10%</span>
            </div>
            <div className="text-lg font-bold text-white">
              {profile.components.consistency_score.toFixed(1)}%
            </div>
            <div className="text-[10px] text-slate-500">Daily learning streak</div>
          </div>
        </div>

        {/* Action Row */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-400">
            <Shield className="w-4 h-4 text-slate-400" />
            <span>
              Demotion Guardrail: <strong className="text-slate-300">{profile.consecutive_low_count}/3</strong> consecutive low periods
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowTestsModal(true)}
              className="px-3 py-1.5 rounded-lg bg-indigo-600/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-600/30 transition-colors flex items-center gap-1.5 font-medium"
            >
              <Calendar className="w-3.5 h-3.5" />
              Periodic Tests ({periodicTests.length})
            </button>
            <button
              onClick={handleOpenHistory}
              className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-colors flex items-center gap-1.5 font-medium"
            >
              <History className="w-3.5 h-3.5" />
              Rank History
            </button>
          </div>
        </div>
      </div>

      {/* Promotion Criteria Checklist Card */}
      {profile.next_rank && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <TrendingUp className="w-5 h-5 text-indigo-400" />
              <h3 className="text-base font-bold text-white">
                Promotion Path &rarr; Next Tier: <span className="text-indigo-400">{profile.next_rank}</span>
              </h3>
            </div>
            <span className="text-xs text-slate-400">
              All criteria must be satisfied simultaneously
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {profile.promotion_criteria.map((crit, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-xl border flex items-start gap-3 transition-all ${
                  crit.met
                    ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-300"
                    : "bg-slate-950/60 border-slate-800 text-slate-400"
                }`}
              >
                <div className="mt-0.5">
                  {crit.met ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  ) : (
                    <div className="w-5 h-5 rounded-full border border-slate-700 flex items-center justify-center text-[10px] font-bold text-slate-500 shrink-0">
                      {idx + 1}
                    </div>
                  )}
                </div>
                <div className="space-y-1">
                  <div className={`text-xs font-semibold ${crit.met ? "text-emerald-200" : "text-white"}`}>
                    {crit.name}
                  </div>
                  <div className="text-[11px] text-slate-400 font-mono">
                    Current: <strong className={crit.met ? "text-emerald-400" : "text-amber-400"}>
                      {typeof crit.current === "number" ? crit.current.toFixed(1) : crit.current}
                    </strong> / Required: {crit.target}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Periodic Tests Modal */}
      {showTestsModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="bg-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Calendar className="w-5 h-5 text-indigo-400" />
                <h3 className="text-lg font-bold text-white">Periodic Assessments</h3>
              </div>
              <button
                onClick={() => setShowTestsModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                &times;
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4">
              <p className="text-xs text-slate-400 leading-relaxed">
                Take weekly assessments (+200 XP) and monthly milestone exams (+500 XP) to raise your Periodic Test averages and unlock higher performance rank tiers.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                {periodicTests.map((t) => (
                  <div
                    key={t.id}
                    className="p-5 rounded-xl border border-slate-800 bg-slate-950/80 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4"
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                          t.test_type === "weekly"
                            ? "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                            : "bg-purple-500/10 text-purple-400 border border-purple-500/30"
                        }`}>
                          {t.test_type === "weekly" ? "Weekly Test" : "Monthly Exam"}
                        </span>
                        {t.passed && (
                          <span className="flex items-center gap-1 text-emerald-400 text-xs font-semibold">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            Passed ({t.best_score}%)
                          </span>
                        )}
                      </div>
                      <h4 className="text-sm font-bold text-white">{t.title}</h4>
                      <p className="text-xs text-slate-400 line-clamp-2">{t.description}</p>
                    </div>

                    <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                      <span className="text-slate-400 flex items-center gap-1">
                        <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                        +{t.xp_reward} XP
                      </span>
                      <button
                        onClick={() => {
                          setShowTestsModal(false);
                          setActiveTestId(t.id);
                        }}
                        className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-colors flex items-center gap-1"
                      >
                        {t.attempts_count > 0 ? "Retake" : "Start Test"}
                        <ArrowUpRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Rank History Modal */}
      {showHistoryModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="bg-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <History className="w-5 h-5 text-indigo-400" />
                <h3 className="text-lg font-bold text-white">Rank Transition History</h3>
              </div>
              <button
                onClick={() => setShowHistoryModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg text-lg"
              >
                &times;
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-3">
              {rankHistory.length === 0 ? (
                <div className="text-center py-8 text-slate-500 text-sm">
                  No rank transition events recorded yet. You are currently in GOLD tier.
                </div>
              ) : (
                rankHistory.map((h) => (
                  <div
                    key={h.id}
                    className="p-4 rounded-xl border border-slate-800 bg-slate-950/60 space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-indigo-300">
                        {h.old_rank} &rarr; {h.new_rank}
                      </span>
                      <span className="text-slate-500 font-mono">
                        {h.changed_at ? new Date(h.changed_at).toLocaleDateString() : ""}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300">{h.reason}</p>
                    <div className="text-[11px] text-slate-500 font-mono">
                      Performance Score at change: {h.performance_score}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Active Periodic Test Cockpit */}
      {activeTestId && (
        <PeriodicTestCockpit
          testId={activeTestId}
          onClose={() => setActiveTestId(null)}
          onTestSubmitted={handleTestFinished}
        />
      )}
    </div>
  );
}
