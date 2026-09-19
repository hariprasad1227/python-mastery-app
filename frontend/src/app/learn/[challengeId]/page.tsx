"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import {
  api,
  ExecuteResult,
  TestResultItem,
  ChallengeDetail,
  StructuredLesson,
  TopicUnlockStatus
} from "@/lib/api";
import LessonViewer from "@/components/LessonViewer";
import TopicExamCockpit from "@/components/TopicExamCockpit";
import {
  BookOpen,
  Columns,
  Code,
  Sparkles,
  Award,
  ArrowRight,
  Lock,
  CheckCircle2,
  AlertCircle,
  Clock,
  ShieldCheck,
  ShieldAlert,
  Play,
  RotateCcw,
  GraduationCap
} from "lucide-react";

export default function ChallengeClassroom() {
  const params = useParams();
  const router = useRouter();
  const challengeId = (params?.challengeId as string) || "chal-1";

  const currentNum = parseInt(challengeId.replace("chal-", ""), 10) || 1;
  const nextChallengeId = currentNum < 100 ? `chal-${currentNum + 1}` : null;
  const prevChallengeId = currentNum > 1 ? `chal-${currentNum - 1}` : null;

  // Gated Progression State
  const [isLocked, setIsLocked] = useState(false);
  const [lockData, setLockData] = useState<{
    message?: string;
    prerequisite_topic_id?: string;
    prerequisite_topic_title?: string;
    prerequisite_exam_id?: string;
  } | null>(null);
  const [topicStatus, setTopicStatus] = useState<
    "locked" | "available" | "in_progress" | "exam_available" | "passed"
  >("available");
  const [lessonCompleted, setLessonCompleted] = useState(false);
  const [practiceCompleted, setPracticeCompleted] = useState(false);
  const [examPassed, setExamPassed] = useState(false);
  const [showExamCockpit, setShowExamCockpit] = useState(false);

  // Challenge workspace state
  const [code, setCode] = useState("");
  const [challengeTitle, setChallengeTitle] = useState("Loading Challenge...");
  const [instructions, setInstructions] = useState("");
  const [xpReward, setXpReward] = useState(50);
  const [timeLimit, setTimeLimit] = useState(30);
  const [entryFn, setEntryFn] = useState<string | undefined>();
  const [publicTests, setPublicTests] = useState<any[]>([]);
  const [testResults, setTestResults] = useState<TestResultItem[]>([]);
  const [terminalOutput, setTerminalOutput] = useState("Ready to evaluate code.");
  const [isRunning, setIsRunning] = useState(false);
  const [activeTab, setActiveTab] = useState<"assertions" | "public_tests">("assertions");
  const [leftTab, setLeftTab] = useState<"lesson" | "instructions">("lesson");
  const [lesson, setLesson] = useState<ChallengeDetail["lesson"] | null>(null);
  const [structuredLesson, setStructuredLesson] = useState<StructuredLesson | null>(null);
  const [viewMode, setViewMode] = useState<"lesson" | "split" | "code">("split");

  // Mentor state
  const [mentorText, setMentorText] = useState("Need help? Request a Socratic hint below.");
  const [mentorQuestion, setMentorQuestion] = useState("");
  const [activeHintLevel, setActiveHintLevel] = useState<number | null>(null);

  // Gamification state
  const [totalXp, setTotalXp] = useState(0);
  const [streak, setStreak] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationText, setCelebrationText] = useState("");

  // Timer state
  const [attemptStartTime, setAttemptStartTime] = useState<number>(Date.now() / 1000);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);

  useEffect(() => {
    async function loadChallenge() {
      try {
        // 1. Check authoritative server-side unlock status
        try {
          const statusInfo: TopicUnlockStatus = await api.getTopicUnlockStatus(challengeId);
          if (!statusInfo.is_unlocked) {
            setIsLocked(true);
            setLockData({
              message: statusInfo.prerequisite_topic_title
                ? `You must pass the exam for '${statusInfo.prerequisite_topic_title}' first.`
                : "This topic is currently locked.",
              prerequisite_topic_id: statusInfo.prerequisite_exam_id?.replace("exam-", "") || prevChallengeId || undefined,
              prerequisite_topic_title: statusInfo.prerequisite_topic_title || `Topic ${currentNum - 1}`,
              prerequisite_exam_id: statusInfo.prerequisite_exam_id || undefined
            });
            return;
          }

          setIsLocked(false);
          setLessonCompleted(statusInfo.lesson_completed);
          setPracticeCompleted(statusInfo.practice_completed);
          setExamPassed(statusInfo.exam_passed);
          setTopicStatus(statusInfo.status as any);
        } catch (statusErr: any) {
          console.warn("Status check issue:", statusErr);
        }

        // 2. Fetch challenge details
        try {
          const detail: ChallengeDetail = await api.getChallengeDetail(challengeId);
          setChallengeTitle(detail.title);
          setInstructions(detail.instructions);
          setXpReward(detail.xp_reward);
          setCode(detail.starter_code);
          setEntryFn(detail.entry_function_name);
          setTimeLimit(detail.time_limit_seconds || 30);
          setPublicTests(detail.test_cases || []);
          if (detail.lesson) {
            setLesson(detail.lesson);
          }
        } catch (detailErr: any) {
          if (detailErr.status === 403 || detailErr.lockData?.locked) {
            setIsLocked(true);
            setLockData(detailErr.lockData || {
              message: detailErr.message,
              prerequisite_topic_id: prevChallengeId || undefined,
              prerequisite_topic_title: `Topic ${currentNum - 1}`
            });
            return;
          }

          // Fallback to curriculum lookup
          const curriculum = await api.getCurriculum();
          for (const mod of curriculum) {
            const found = mod.challenges.find((c) => c.id === challengeId);
            if (found) {
              if (found.status === "locked") {
                setIsLocked(true);
                setLockData({
                  message: "This topic is locked. Complete previous exams to unlock.",
                  prerequisite_topic_id: prevChallengeId || undefined,
                  prerequisite_topic_title: `Topic ${currentNum - 1}`
                });
                return;
              }
              setChallengeTitle(found.title);
              setInstructions(found.instructions);
              setXpReward(found.xp_reward);
              setCode(found.starter_code);
              setEntryFn(found.entry_function_name);
              break;
            }
          }
        }

        // 3. Fetch Structured Lesson
        try {
          const sLesson = await api.getStructuredLessonByChallenge(challengeId);
          setStructuredLesson(sLesson);
        } catch (sErr) {
          console.warn("Could not load structured lesson:", sErr);
        }

        // 4. Load user profile
        try {
          const profile = await api.getProfile();
          setTotalXp(profile.total_xp);
          setStreak(profile.current_streak);
        } catch (pErr) {
          console.warn("Profile load:", pErr);
        }
      } catch (err: any) {
        console.error("General classroom load error:", err);
      }
    }

    loadChallenge();
    setAttemptStartTime(Date.now() / 1000);
    setElapsedSeconds(0);
    setTestResults([]);
  }, [challengeId]);

  // Live timer tick
  useEffect(() => {
    if (isLocked) return;
    const timer = setInterval(() => {
      setElapsedSeconds(Math.floor(Date.now() / 1000 - attemptStartTime));
    }, 1000);
    return () => clearInterval(timer);
  }, [attemptStartTime, isLocked]);

  const handleCompleteLesson = async () => {
    try {
      await api.completeTopicLesson(challengeId);
      setLessonCompleted(true);
      if (practiceCompleted) {
        setTopicStatus("exam_available");
      }
    } catch (err) {
      console.warn("Lesson completion mark:", err);
      setLessonCompleted(true);
    }
  };

  async function handleRun() {
    setIsRunning(true);
    setTerminalOutput("Executing in isolated Python sandbox (server-enforced tests & timeout)...");

    try {
      const result: ExecuteResult = await api.executeCode({
        challenge_id: challengeId,
        code: code,
        attempt_started_at: attemptStartTime,
      });

      setTestResults(result.test_results || []);
      let out = "";
      if (result.stdout) out += result.stdout + "\n";
      if (result.stderr) out += "Error Trace:\n" + result.stderr + "\n";
      out += `\nExecution time: ${result.execution_time_ms}ms | Attempt duration: ${result.attempt_duration_seconds}s | Status: ${result.status}`;
      setTerminalOutput(out.trim());
      setActiveTab("assertions");

      if (result.passed) {
        setPracticeCompleted(true);
        if (lessonCompleted) {
          setTopicStatus("exam_available");
        }
        if (result.xp_earned) {
          setTotalXp((prev) => prev + result.xp_earned);
        }
        if (result.new_streak) {
          setStreak(result.new_streak);
        }

        setCelebrationText("Challenge Code Passed! Now take the Topic Exam to permanently unlock the next topic!");
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 6000);
      }
    } catch (err: any) {
      setTerminalOutput("Error connecting to runner: " + err.message);
    } finally {
      setIsRunning(false);
    }
  }

  async function handleHint(level: number) {
    setActiveHintLevel(level);
    setMentorText("Consulting Socratic AI Mentor...");
    setMentorQuestion("");

    try {
      const res = await api.getMentorHint({
        challenge_title: challengeTitle,
        challenge_instructions: instructions,
        learner_code: code,
        hint_level: level,
      });
      setMentorText(res.hint);
      setMentorQuestion(res.socratic_question || "");
    } catch (err) {
      setMentorText("Make sure to check your return types and function arguments.");
    }
  }

  const handleExamPassed = (nextId?: string | null, xpEarned?: number) => {
    setExamPassed(true);
    setTopicStatus("passed");
    if (xpEarned) {
      setTotalXp((prev) => prev + xpEarned);
    }
    setCelebrationText("Topic Exam Passed with >= 70%! Next topic is now unlocked!");
    setShowCelebration(true);
    setTimeout(() => setShowCelebration(false), 6000);
  };

  // LOCKED BARRIER SCREEN
  if (isLocked) {
    const prereqId = lockData?.prerequisite_topic_id || prevChallengeId || "chal-1";
    const prereqTitle = lockData?.prerequisite_topic_title || `Level ${currentNum - 1}`;

    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        {/* Minimal Header */}
        <header className="border-b border-slate-800 bg-slate-900/80 px-6 py-3 flex items-center justify-between">
          <Link
            href="/"
            className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1"
          >
            ← Back to Curriculum
          </Link>
          <span className="text-xs text-slate-500 font-mono">Topic Gated Progression</span>
        </header>

        {/* Lock Barrier Center Card */}
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="max-w-lg w-full bg-slate-900/90 border border-slate-800 rounded-3xl p-8 text-center space-y-6 shadow-2xl relative overflow-hidden">
            <div className="absolute -top-24 -left-24 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl" />
            <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-rose-500/10 rounded-full blur-3xl" />

            {/* Lock Icon */}
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-amber-500/20 to-rose-500/20 border border-amber-500/30 flex items-center justify-center mx-auto shadow-lg text-amber-400">
              <Lock className="w-10 h-10" />
            </div>

            <div className="space-y-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-wider">
                <ShieldAlert className="w-3.5 h-3.5" />
                Topic Locked
              </div>
              <h2 className="text-2xl font-black text-white">
                Prerequisite Exam Required
              </h2>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-md mx-auto">
                Python Mastery strictly enforces server-side topic unlocking. To access{" "}
                <span className="text-white font-bold">{challengeTitle || `Topic ${currentNum}`}</span>,
                you must first pass the topic examination for:
              </p>
            </div>

            {/* Prerequisite Card */}
            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 text-left flex items-center justify-between gap-4">
              <div className="space-y-1">
                <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">
                  Required Prerequisite
                </span>
                <div className="text-sm font-bold text-white">{prereqTitle}</div>
                <div className="text-xs text-slate-400">
                  Pass Mark: <span className="text-amber-400 font-semibold">≥ 70%</span> on Topic Exam
                </div>
              </div>

              <Link
                href={`/learn/${prereqId}`}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shrink-0 shadow-md shadow-indigo-600/20"
              >
                <span>Go to Exam</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Navigation links */}
            <div className="pt-2 flex items-center justify-center gap-3">
              <Link
                href="/"
                className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
              >
                Return to Curriculum Roadmap
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Header with Topic Progression Pipeline */}
      <header className="border-b border-slate-800 bg-slate-900/80 px-4 sm:px-6 py-2 flex flex-col gap-2 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition flex items-center gap-1"
            >
              ← Curriculum
            </Link>
            <span className="text-slate-700">|</span>
            <span className="text-sm font-bold text-white flex items-center gap-2">
              <span className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded font-mono">
                L{currentNum}/100
              </span>
              <span className="truncate max-w-xs sm:max-w-md">{challengeTitle}</span>
            </span>
          </div>

          {/* Center View Mode Switcher */}
          <div className="hidden lg:flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <button
              onClick={() => setViewMode("lesson")}
              className={`px-3 py-1 rounded-md transition flex items-center gap-1.5 font-medium ${
                viewMode === "lesson"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Full Lesson</span>
            </button>
            <button
              onClick={() => setViewMode("split")}
              className={`px-3 py-1 rounded-md transition flex items-center gap-1.5 font-medium ${
                viewMode === "split"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <Columns className="w-3.5 h-3.5" />
              <span>Split View</span>
            </button>
            <button
              onClick={() => setViewMode("code")}
              className={`px-3 py-1 rounded-md transition flex items-center gap-1.5 font-medium ${
                viewMode === "code"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              <span>Editor Only</span>
            </button>
          </div>

          <div className="flex items-center gap-4">
            {/* Live Attempt Timer */}
            <div className="flex items-center gap-1.5 text-xs bg-slate-800 px-2.5 py-1 rounded-lg font-mono text-slate-300 border border-slate-700">
              <Clock className="w-3 h-3 text-slate-400" />
              <span>{elapsedSeconds}s</span>
            </div>

            <div className="text-xs font-semibold text-orange-400">🔥 {streak}d</div>
            <div className="text-xs font-semibold text-emerald-400">⚡ {totalXp} XP</div>
          </div>
        </div>

        {/* TOPIC PROGRESSION STEPPER BAR */}
        <div className="flex items-center justify-between border-t border-slate-800/80 pt-1.5 text-xs">
          <div className="flex items-center gap-2 sm:gap-4 overflow-x-auto">
            {/* Step 1: Lesson */}
            <div
              onClick={() => {
                setViewMode("lesson");
                handleCompleteLesson();
              }}
              className={`cursor-pointer flex items-center gap-1.5 px-2.5 py-1 rounded-lg border transition ${
                lessonCompleted
                  ? "bg-emerald-950/30 border-emerald-500/30 text-emerald-300"
                  : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {lessonCompleted ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <span className="w-3.5 h-3.5 rounded-full border border-slate-500 text-[9px] flex items-center justify-center">1</span>
              )}
              <span className="font-semibold">1. Learn Lesson</span>
            </div>

            <span className="text-slate-700">→</span>

            {/* Step 2: Practice Challenge */}
            <div
              onClick={() => setViewMode("split")}
              className={`cursor-pointer flex items-center gap-1.5 px-2.5 py-1 rounded-lg border transition ${
                practiceCompleted
                  ? "bg-emerald-950/30 border-emerald-500/30 text-emerald-300"
                  : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {practiceCompleted ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <span className="w-3.5 h-3.5 rounded-full border border-slate-500 text-[9px] flex items-center justify-center">2</span>
              )}
              <span className="font-semibold">2. Coding Task</span>
            </div>

            <span className="text-slate-700">→</span>

            {/* Step 3: Topic Exam */}
            <div
              onClick={() => setShowExamCockpit(true)}
              className={`cursor-pointer flex items-center gap-1.5 px-2.5 py-1 rounded-lg border transition ${
                examPassed
                  ? "bg-emerald-950/30 border-emerald-500/30 text-emerald-300"
                  : practiceCompleted || lessonCompleted
                  ? "bg-indigo-950/40 border-indigo-500/40 text-indigo-300 hover:bg-indigo-900/40 animate-pulse"
                  : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {examPassed ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <span className="w-3.5 h-3.5 rounded-full border border-indigo-400 text-[9px] flex items-center justify-center text-indigo-300">3</span>
              )}
              <span className="font-semibold">
                3. Topic Exam {examPassed ? "(Passed)" : "(Gated Unlock)"}
              </span>
            </div>
          </div>

          {/* Exam Trigger CTA */}
          <div className="flex items-center gap-2">
            {examPassed ? (
              <div className="flex items-center gap-1.5 text-emerald-400 font-bold text-xs bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-lg">
                <Award className="w-3.5 h-3.5" />
                <span>Exam Passed</span>
                {nextChallengeId && (
                  <Link
                    href={`/learn/${nextChallengeId}`}
                    className="ml-2 text-indigo-400 hover:text-indigo-300 underline font-semibold"
                  >
                    Next Topic →
                  </Link>
                )}
              </div>
            ) : (
              <button
                onClick={() => setShowExamCockpit(true)}
                className="px-3 py-1 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-lg font-bold text-xs transition flex items-center gap-1.5 shadow-md shadow-indigo-600/20"
              >
                <GraduationCap className="w-3.5 h-3.5" />
                <span>Take Topic Exam</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Workspace Body */}
      {viewMode === "lesson" && structuredLesson ? (
        /* Fullscreen Educational Lesson First Mode */
        <div className="flex-1 overflow-y-auto bg-slate-950 px-4 py-8">
          <div className="max-w-4xl mx-auto space-y-6">
            <LessonViewer
              lesson={structuredLesson}
              onStartCoding={() => {
                handleCompleteLesson();
                setViewMode("split");
              }}
              onQuizPassed={(xp) => {
                handleCompleteLesson();
                setTotalXp((prev) => prev + xp);
              }}
            />

            {/* Exam Launcher Box at end of Lesson */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 text-center space-y-3">
              <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                Topic Mastery Gate
              </div>
              <h3 className="text-base font-bold text-white">
                Ready to prove mastery and unlock the next topic?
              </h3>
              <p className="text-xs text-slate-300 max-w-md mx-auto">
                Passing the Topic Exam (&ge; 70%) permanently unlocks the next Python topic in your curriculum.
              </p>
              <div className="pt-2 flex items-center justify-center gap-3">
                <button
                  onClick={() => setShowExamCockpit(true)}
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-indigo-900/30"
                >
                  <GraduationCap className="w-4 h-4" />
                  <span>Launch Topic Exam</span>
                </button>
                <button
                  onClick={() => setViewMode("split")}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition"
                >
                  Go to Coding Sandbox
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Split or Code Workspace */
        <div className="flex-1 grid grid-cols-12 overflow-hidden">
          {/* Left Column: Lesson / Instructions / AI Mentor (Hidden if viewMode === "code") */}
          {viewMode !== "code" && (
            <div className="col-span-5 border-r border-slate-800 bg-slate-900/40 p-5 flex flex-col gap-4 overflow-y-auto">
              {/* Tab Switcher: Lesson vs Task */}
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800">
                  <button
                    onClick={() => setLeftTab("lesson")}
                    className={`text-xs font-bold px-3 py-1.5 rounded-md transition flex items-center gap-1.5 ${
                      leftTab === "lesson"
                        ? "bg-indigo-600 text-white shadow-sm"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    <span>📘</span>
                    <span>Structured Lesson</span>
                  </button>
                  <button
                    onClick={() => setLeftTab("instructions")}
                    className={`text-xs font-bold px-3 py-1.5 rounded-md transition flex items-center gap-1.5 ${
                      leftTab === "instructions"
                        ? "bg-indigo-600 text-white shadow-sm"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    <span>🎯</span>
                    <span>Challenge Task</span>
                  </button>
                </div>

                <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                  +{xpReward} XP
                </span>
              </div>

              {/* Tab Content: LESSON */}
              {leftTab === "lesson" ? (
                structuredLesson ? (
                  <LessonViewer
                    lesson={structuredLesson}
                    isCompact={true}
                    onStartCoding={() => {
                      handleCompleteLesson();
                      setLeftTab("instructions");
                    }}
                    onQuizPassed={(xp) => {
                      handleCompleteLesson();
                      setTotalXp((prev) => prev + xp);
                    }}
                  />
                ) : (
                  <div className="space-y-4">
                    <div>
                      <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                        Track {lesson?.track_number || 1}: {lesson?.track_title || "Fundamentals"}
                      </span>
                      <h2 className="text-lg font-black text-white mt-1 mb-2">
                        {lesson?.concept_headline || `Lesson: ${challengeTitle}`}
                      </h2>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {lesson?.theory_overview}
                      </p>
                    </div>

                    {/* Core Concepts Breakdown */}
                    <div className="space-y-3">
                      {lesson?.core_concepts?.map((concept, idx) => (
                        <div
                          key={idx}
                          className="bg-slate-950/80 border border-slate-800/90 rounded-xl p-3.5 space-y-2"
                        >
                          <div className="text-xs font-bold text-indigo-300">{concept.name}</div>
                          <div className="text-[12px] text-slate-300 leading-relaxed">
                            {concept.explanation}
                          </div>
                          {concept.example_code && (
                            <div className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 font-mono text-[11px] text-emerald-300 overflow-x-auto whitespace-pre">
                              {concept.example_code}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>

                    {/* Switch to Challenge Task CTA */}
                    <button
                      onClick={() => {
                        handleCompleteLesson();
                        setLeftTab("instructions");
                      }}
                      className="w-full py-2.5 rounded-lg bg-indigo-600/30 border border-indigo-500/50 hover:bg-indigo-600/50 text-indigo-200 text-xs font-bold transition flex items-center justify-center gap-1.5"
                    >
                      <span>Understood the concepts? Open Challenge Task</span>
                      <span>→</span>
                    </button>
                  </div>
                )
              ) : (
                /* Tab Content: INSTRUCTIONS & MENTOR */
                <div className="space-y-4">
                  {/* Task Instructions */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider">
                      Instructions
                    </h3>
                    <div className="text-xs text-slate-200 leading-relaxed whitespace-pre-wrap bg-slate-950 p-3 rounded-lg border border-slate-800">
                      {instructions}
                    </div>
                  </div>

                  {/* Function Signature Guideline */}
                  {entryFn && (
                    <div className="text-xs bg-indigo-950/30 border border-indigo-500/30 p-2.5 rounded-lg text-indigo-200">
                      Target Entry Function: <code className="font-mono text-indigo-400 font-bold">{entryFn}</code>
                    </div>
                  )}

                  {/* Exam Gating Notice */}
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-amber-400 flex items-center gap-1">
                        <Lock className="w-3.5 h-3.5" /> Topic Progression
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        examPassed
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                      }`}>
                        {examPassed ? "EXAM PASSED" : "EXAM REQUIRED"}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-relaxed">
                      Pass code tests and complete the Topic Exam with ≥ 70% to unlock the next level.
                    </p>
                    <button
                      onClick={() => setShowExamCockpit(true)}
                      className="w-full py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/40 text-indigo-200 text-xs font-bold transition flex items-center justify-center gap-1"
                    >
                      <GraduationCap className="w-3.5 h-3.5" />
                      <span>{examPassed ? "Review Topic Exam" : "Take Topic Exam (Unlock Next)"}</span>
                    </button>
                  </div>

                  {/* AI Mentor Socratic Hint System */}
                  <div className="border-t border-slate-800 pt-3 space-y-2">
                    <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                      <span>🤖</span>
                      <span>Socratic AI Mentor</span>
                    </div>

                    <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2">
                      <p className="text-xs text-slate-300 italic leading-relaxed">
                        "{mentorText}"
                      </p>
                      {mentorQuestion && (
                        <p className="text-xs text-indigo-300 font-medium">
                          Question to ponder: {mentorQuestion}
                        </p>
                      )}
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => handleHint(1)}
                        className={`flex-1 py-1.5 rounded text-xs font-medium border transition ${
                          activeHintLevel === 1
                            ? "bg-indigo-600 border-indigo-500 text-white"
                            : "bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700"
                        }`}
                      >
                        Hint 1: Direction
                      </button>
                      <button
                        onClick={() => handleHint(2)}
                        className={`flex-1 py-1.5 rounded text-xs font-medium border transition ${
                          activeHintLevel === 2
                            ? "bg-indigo-600 border-indigo-500 text-white"
                            : "bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700"
                        }`}
                      >
                        Hint 2: Structure
                      </button>
                      <button
                        onClick={() => handleHint(3)}
                        className={`flex-1 py-1.5 rounded text-xs font-medium border transition ${
                          activeHintLevel === 3
                            ? "bg-indigo-600 border-indigo-500 text-white"
                            : "bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700"
                        }`}
                      >
                        Hint 3: Solution
                      </button>
                    </div>

                    <button
                      onClick={() => {
                        window.dispatchEvent(
                          new CustomEvent("open-ai-mentor", {
                            detail: {
                              topic: challengeTitle,
                              code: code,
                              error: terminalOutput.includes("Error") ? terminalOutput : undefined,
                              initialQuestion: `Can you help me understand '${challengeTitle}' and give me a gentle clue on how to write the solution?`
                            }
                          })
                        );
                      }}
                      className="w-full py-2 px-3 rounded-lg bg-gradient-to-r from-violet-700/80 to-indigo-700/80 hover:from-violet-600 hover:to-indigo-600 text-white text-xs font-semibold flex items-center justify-center gap-1.5 border border-violet-500/40 shadow-sm transition"
                    >
                      <span>✨ Chat with AI Assistant about this code</span>
                    </button>
                  </div>

                </div>
              )}
            </div>
          )}

          {/* Right Column: Code Editor & Execution Sandbox */}
          <div className={`${viewMode === "code" ? "col-span-12" : "col-span-7"} flex flex-col bg-slate-950 overflow-hidden`}>
            {/* Editor Toolbar */}
            <div className="bg-slate-900/60 border-b border-slate-800 px-4 py-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-400">solution.py</span>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={handleRun}
                  disabled={isRunning}
                  className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition flex items-center gap-2 shadow-lg shadow-emerald-900/20 disabled:opacity-50"
                >
                  <span>{isRunning ? "Running Sandbox..." : "Run & Evaluate"}</span>
                  <span>▶</span>
                </button>

                {examPassed && nextChallengeId ? (
                  <Link
                    href={`/learn/${nextChallengeId}`}
                    className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition flex items-center gap-1 shadow-lg shadow-indigo-900/20"
                  >
                    <span>Next Level</span>
                    <span>→</span>
                  </Link>
                ) : (
                  <button
                    onClick={() => setShowExamCockpit(true)}
                    className="px-3 py-1.5 bg-purple-600/80 hover:bg-purple-600 text-white text-xs font-bold rounded-lg transition flex items-center gap-1 shadow-lg shadow-purple-900/20"
                  >
                    <span>Topic Exam</span>
                    <span>📝</span>
                  </button>
                )}
              </div>
            </div>

            {/* Code Input Area */}
            <div className="flex-1 relative bg-slate-950 font-mono text-sm">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck="false"
                className="w-full h-full bg-slate-950 text-emerald-400 p-4 font-mono text-xs md:text-sm resize-none focus:outline-none focus:ring-0 leading-relaxed"
                placeholder="# Write your Python code here..."
              />
            </div>

            {/* Bottom Panel: Test Results & Terminal */}
            <div className="h-64 border-t border-slate-800 bg-slate-900/50 flex flex-col">
              {/* Bottom Panel Tabs */}
              <div className="flex items-center border-b border-slate-800 px-4 py-1.5 bg-slate-900 text-xs">
                <button
                  onClick={() => setActiveTab("assertions")}
                  className={`px-3 py-1 rounded font-medium transition mr-2 ${
                    activeTab === "assertions"
                      ? "bg-slate-800 text-white"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Server Assertions ({testResults.length})
                </button>
                <button
                  onClick={() => setActiveTab("public_tests")}
                  className={`px-3 py-1 rounded font-medium transition ${
                    activeTab === "public_tests"
                      ? "bg-slate-800 text-white"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Public Test Cases ({publicTests.length})
                </button>
              </div>

              {/* Panel Content: Side-by-side Results & Console */}
              <div className="flex-1 p-3 flex gap-3 overflow-hidden">
                {/* Test Results List */}
                <div className="w-1/2 overflow-y-auto space-y-2">
                  {activeTab === "assertions" ? (
                    testResults.length === 0 ? (
                      <div className="text-xs text-slate-500 italic p-3 border border-slate-800 rounded bg-slate-950">
                        No tests evaluated yet. Press "Run & Evaluate" to run against visible & hidden test cases.
                      </div>
                    ) : (
                      testResults.map((tr) => (
                        <div
                          key={tr.test_index}
                          className={`p-2 rounded border text-xs flex items-center justify-between ${
                            tr.passed
                              ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                              : "bg-rose-500/10 border-rose-500/30 text-rose-300"
                          }`}
                        >
                          <span className="font-medium truncate pr-2">{tr.description}</span>
                          <span className="font-bold flex-shrink-0">{tr.passed ? "PASS" : "FAIL"}</span>
                        </div>
                      ))
                    )
                  ) : (
                    publicTests.length === 0 ? (
                      <div className="text-xs text-slate-500 italic p-3 border border-slate-800 rounded bg-slate-950">
                        No public test cases registered for this challenge.
                      </div>
                    ) : (
                      publicTests.map((pt, idx) => (
                        <div
                          key={idx}
                          className="p-2 rounded border border-slate-800 bg-slate-950 text-xs space-y-1"
                        >
                          <div className="font-bold text-slate-300">{pt.description}</div>
                          <div className="font-mono text-[11px] text-slate-400">
                            Input: <span className="text-amber-300">{JSON.stringify(pt.input)}</span>
                          </div>
                          <div className="font-mono text-[11px] text-slate-400">
                            Expected: <span className="text-emerald-300">{JSON.stringify(pt.expected)}</span>
                          </div>
                        </div>
                      ))
                    )
                  )}
                </div>

                {/* Console Output */}
                <div className="w-1/2 bg-slate-950 border border-slate-800 rounded p-3 font-mono text-xs text-sky-300 overflow-y-auto whitespace-pre-wrap">
                  {terminalOutput}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success Celebration Toast */}
      {showCelebration && (
        <div className="fixed bottom-6 right-6 bg-emerald-600 text-white font-bold px-6 py-3 rounded-xl shadow-2xl animate-bounce flex items-center gap-3 z-50">
          <span className="text-2xl">🏆</span>
          <div className="space-y-1">
            <div className="text-sm">{celebrationText}</div>
            {!examPassed && (
              <button
                onClick={() => {
                  setShowCelebration(false);
                  setShowExamCockpit(true);
                }}
                className="text-xs bg-white text-emerald-800 px-3 py-1 rounded font-bold hover:bg-emerald-100 transition inline-block"
              >
                Launch Topic Exam Now →
              </button>
            )}
          </div>
        </div>
      )}

      {/* Interactive Topic Exam Cockpit Modal */}
      {showExamCockpit && (
        <TopicExamCockpit
          topicId={challengeId}
          topicTitle={challengeTitle}
          onClose={() => setShowExamCockpit(false)}
          onExamPassed={handleExamPassed}
          onReviewLesson={() => setViewMode("lesson")}
        />
      )}
    </div>
  );
}
