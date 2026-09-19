"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api, InterviewProblem, ExecuteResult } from "@/lib/api";

export default function InterviewCockpit() {
  const params = useParams();
  const problemId = (params?.problemId as string) || "interview-1";

  const [problem, setProblem] = useState<InterviewProblem | null>(null);
  const [code, setCode] = useState("");
  const [terminalOutput, setTerminalOutput] = useState("Ready for technical evaluation.");
  const [isRunning, setIsRunning] = useState(false);
  const [isPassed, setIsPassed] = useState(false);
  const [activeHintIndex, setActiveHintIndex] = useState<number | null>(null);

  // Timed interview state
  const [timeRemainingSeconds, setTimeRemainingSeconds] = useState(20 * 60);
  const [timerActive, setTimerActive] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getInterviewProblemDetail(problemId);
        setProblem(data);
        setCode(data.starter_code);
        setTimeRemainingSeconds(data.time_limit_minutes * 60);
      } catch (err) {
        console.error("Failed to load interview problem:", err);
      }
    }
    load();
  }, [problemId]);

  useEffect(() => {
    if (!timerActive || timeRemainingSeconds <= 0) return;
    const interval = setInterval(() => {
      setTimeRemainingSeconds((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [timerActive, timeRemainingSeconds]);

  const formatTimer = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const remaining = secs % 60;
    return `${mins}:${remaining < 10 ? "0" : ""}${remaining}`;
  };

  async function handleSubmit() {
    setIsRunning(true);
    setTerminalOutput("Interviewer is evaluating your code against edge cases & stress tests...");

    try {
      const res: ExecuteResult = await api.submitInterview(problemId, code);
      let out = "";
      if (res.stdout) out += res.stdout + "\n";
      if (res.stderr) out += "Traceback / Test Error:\n" + res.stderr + "\n";
      out += `\nRuntime: ${res.execution_time_ms}ms | Interview Verdict: ${res.status.toUpperCase()}`;
      setTerminalOutput(out.trim());

      if (res.passed) {
        setIsPassed(true);
        setTimerActive(false);
      }
    } catch (err: any) {
      setTerminalOutput("Submission error: " + err.message);
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Top Cockpit Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/interview"
            className="text-xs font-semibold text-pink-400 hover:text-pink-300 transition flex items-center gap-1"
          >
            ← Back to Interview Arena
          </Link>
          <span className="text-slate-700">|</span>
          <span className="text-sm font-bold text-white flex items-center gap-2">
            <span className="text-xs bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded font-mono">
              {problem?.difficulty || "Medium"}
            </span>
            {problem?.title || "Loading Problem..."}
          </span>
        </div>

        <div className="flex items-center gap-5">
          {/* Countdown Clock */}
          <div
            className={`font-mono text-xs px-3 py-1.5 rounded-lg border flex items-center gap-2 font-bold ${
              timeRemainingSeconds < 300
                ? "bg-rose-500/10 border-rose-500/30 text-rose-400 animate-pulse"
                : "bg-slate-800 border-slate-700 text-slate-200"
            }`}
          >
            <span>⏳</span>
            <span>{formatTimer(timeRemainingSeconds)}</span>
          </div>

          <button
            onClick={handleSubmit}
            disabled={isRunning}
            className="bg-pink-600 hover:bg-pink-500 text-white font-semibold text-xs px-5 py-2 rounded-lg transition shadow-md flex items-center gap-2 disabled:opacity-50"
          >
            <span>▶</span> {isRunning ? "Evaluating..." : "Submit to Interviewer (Ctrl+Enter)"}
          </button>
        </div>
      </header>

      {/* Main Split Interface */}
      <div className="flex-1 grid grid-cols-12 overflow-hidden">
        {/* Left: Problem Details, Constraints, Examples & Hints */}
        <div className="col-span-5 border-r border-slate-800 bg-slate-900/40 p-6 flex flex-col gap-5 overflow-y-auto">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-pink-400 uppercase tracking-wider">
                {problem?.category}
              </span>
            </div>
            <h1 className="text-2xl font-black text-white mb-2">{problem?.title}</h1>
            <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
              {problem?.description}
            </div>
          </div>

          {/* Examples */}
          <div className="space-y-3">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Example Test Cases
            </div>
            {problem?.examples.map((ex, idx) => (
              <div
                key={idx}
                className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs space-y-1 font-mono"
              >
                <div>
                  <span className="text-slate-500">Input: </span>
                  <span className="text-amber-300">{ex.input}</span>
                </div>
                <div>
                  <span className="text-slate-500">Output: </span>
                  <span className="text-emerald-300">{ex.output}</span>
                </div>
                {ex.explanation && (
                  <div className="text-slate-400 text-[11px] font-sans pt-1">
                    {ex.explanation}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Constraints */}
          {problem?.constraints && problem.constraints.length > 0 && (
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                Constraints
              </div>
              <ul className="list-disc list-inside text-xs text-slate-300 space-y-1 font-mono">
                {problem.constraints.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Socratic Interviewer Hints */}
          {problem?.hints && problem.hints.length > 0 && (
            <div className="mt-auto bg-slate-900/80 border border-pink-500/30 rounded-xl p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="text-xs font-bold text-pink-300 flex items-center gap-1.5">
                  <span>💡</span> Interviewer Clues
                </div>
                <div className="flex gap-1">
                  {problem.hints.map((_, hIdx) => (
                    <button
                      key={hIdx}
                      onClick={() =>
                        setActiveHintIndex(activeHintIndex === hIdx ? null : hIdx)
                      }
                      className={`text-[11px] px-2 py-0.5 rounded font-semibold transition ${
                        activeHintIndex === hIdx
                          ? "bg-pink-600 text-white"
                          : "bg-slate-800 text-slate-400 hover:text-white"
                      }`}
                    >
                      Hint {hIdx + 1}
                    </button>
                  ))}
                </div>
              </div>

              {activeHintIndex !== null && (
                <div className="text-xs text-slate-200 bg-slate-950 p-2.5 rounded border border-slate-800 leading-relaxed">
                  {problem.hints[activeHintIndex]}
                </div>
              )}
            </div>
          )}

          {isPassed && (
            <div className="p-4 bg-emerald-950/40 border border-emerald-500/40 rounded-xl text-emerald-300 text-xs flex items-center gap-3">
              <span className="text-2xl">🎯</span>
              <div>
                <div className="font-bold">Interview Problem Cleared!</div>
                <div className="opacity-90">Solution passed all edge case tests with optimal complexity.</div>
              </div>
            </div>
          )}
        </div>

        {/* Right: Code Editor & Evaluation Console */}
        <div className="col-span-7 flex flex-col overflow-hidden bg-slate-950">
          <div className="border-b border-slate-800 bg-slate-900 px-6 py-2.5 flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-slate-400">solution.py</span>
            <div className="text-[11px] text-slate-500 font-mono">
              Press Ctrl+Enter to Submit
            </div>
          </div>

          <div className="flex-1 p-4 bg-slate-950 overflow-hidden">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
              spellCheck={false}
              className="w-full h-full bg-slate-950 text-slate-100 font-mono text-sm leading-relaxed p-4 border border-slate-800 rounded-lg outline-none resize-none focus:border-pink-500"
            />
          </div>

          {/* Terminal Console */}
          <div className="h-56 border-t border-slate-800 bg-slate-900/60 p-4 flex flex-col gap-2 overflow-hidden">
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
              <span>Interviewer Feedback Console</span>
              <span className="font-mono text-slate-500 text-[11px]">Strict Edge-Case Verification</span>
            </div>
            <div className="flex-1 bg-slate-950 border border-slate-800 rounded p-3 font-mono text-xs text-pink-300 overflow-y-auto whitespace-pre-wrap">
              {terminalOutput}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
