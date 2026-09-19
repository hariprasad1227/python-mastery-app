"use client";

import React, { useState, useEffect } from "react";
import {
  Clock,
  CheckCircle2,
  XCircle,
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  Sparkles,
  Award,
  X,
  Code2,
  Terminal,
  Send,
  Calendar,
  Flame
} from "lucide-react";
import {
  api,
  PeriodicTestDetail,
  PeriodicTestSubmitResult,
  LevelFinalTestQuestion
} from "@/lib/api";

interface PeriodicTestCockpitProps {
  testId: string;
  onClose: () => void;
  onTestSubmitted: (result: PeriodicTestSubmitResult) => void;
}

export default function PeriodicTestCockpit({
  testId,
  onClose,
  onTestSubmitted
}: PeriodicTestCockpitProps) {
  const [test, setTest] = useState<PeriodicTestDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Examination state
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<PeriodicTestSubmitResult | null>(null);

  // Timer state
  const [secondsRemaining, setSecondsRemaining] = useState<number>(20 * 60);
  const [timerActive, setTimerActive] = useState<boolean>(false);

  useEffect(() => {
    async function loadTest() {
      try {
        setLoading(true);
        const data = await api.getPeriodicTest(testId);
        setTest(data);
        setSecondsRemaining((data.time_limit_minutes || 20) * 60);
        setTimerActive(true);
      } catch (err: any) {
        setError(err.message || "Failed to load periodic test");
      } finally {
        setLoading(false);
      }
    }
    loadTest();
  }, [testId]);

  // Countdown timer
  useEffect(() => {
    if (!timerActive || result || secondsRemaining <= 0) return;
    const interval = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleAutoSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [timerActive, result, secondsRemaining]);

  const handleAutoSubmit = () => {
    if (!result && !submitting) {
      handleSubmit();
    }
  };

  const handleSelectOption = (questionId: string, answer: string) => {
    if (result) return;
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmit = async () => {
    if (!test || submitting) return;
    setSubmitting(true);
    setTimerActive(false);
    try {
      const submitRes = await api.submitPeriodicTest(test.id, answers);
      setResult(submitRes);
      onTestSubmitted(submitRes);
    } catch (err: any) {
      setError(err.message || "Failed to submit test");
      setTimerActive(true);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
        <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 max-w-md w-full text-center space-y-4">
          <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-slate-300 font-medium">Loading periodic assessment...</p>
        </div>
      </div>
    );
  }

  if (error && !test) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
        <div className="bg-slate-900 border border-rose-500/50 rounded-2xl p-8 max-w-md w-full text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-rose-400 mx-auto" />
          <h3 className="text-xl font-bold text-white">Assessment Error</h3>
          <p className="text-slate-400 text-sm">{error}</p>
          <button
            onClick={onClose}
            className="px-6 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  if (!test) return null;

  const currentQ = test.questions[currentIndex];
  const totalQuestions = test.questions.length;
  const answeredCount = Object.keys(answers).length;
  const isLastQuestion = currentIndex === totalQuestions - 1;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-2 sm:p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-4xl w-full max-h-[95vh] flex flex-col shadow-2xl overflow-hidden">
        
        {/* Header Bar */}
        <div className="bg-slate-950/80 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className={`px-2.5 py-1 rounded-md text-xs font-semibold uppercase tracking-wider ${
              test.test_type === "weekly"
                ? "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                : "bg-purple-500/10 text-purple-400 border border-purple-500/30"
            }`}>
              {test.test_type === "weekly" ? "Weekly Assessment" : "Monthly Milestone Exam"}
            </span>
            <h2 className="text-lg font-bold text-white hidden sm:block truncate max-w-md">
              {test.title}
            </h2>
          </div>

          <div className="flex items-center gap-4">
            {/* Timer */}
            {!result && (
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg font-mono text-sm font-semibold ${
                secondsRemaining < 180
                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40 animate-pulse"
                  : "bg-slate-800 text-slate-200 border border-slate-700"
              }`}>
                <Clock className="w-4 h-4" />
                <span>{formatTime(secondsRemaining)}</span>
              </div>
            )}

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {result ? (
            /* Results View */
            <div className="space-y-6">
              <div className={`p-6 rounded-2xl border text-center space-y-3 ${
                result.passed
                  ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300"
                  : "bg-rose-950/30 border-rose-500/40 text-rose-300"
              }`}>
                <div className="inline-flex p-3 rounded-full bg-slate-900 border border-current mb-1">
                  {result.passed ? (
                    <Award className="w-10 h-10 text-emerald-400" />
                  ) : (
                    <XCircle className="w-10 h-10 text-rose-400" />
                  )}
                </div>
                <h3 className="text-2xl font-bold text-white">
                  {result.passed ? "Assessment Passed! 🎉" : "Passing Threshold Not Met"}
                </h3>
                <p className="text-slate-300 text-sm max-w-lg mx-auto">
                  {result.passed
                    ? `Outstanding work! You scored ${result.percentage}% (Passing: ${result.pass_percentage}%). Your test scores have been updated in the performance engine.`
                    : `You scored ${result.percentage}%, which is below the ${result.pass_percentage}% requirement. Review your mistakes below and try again to improve your standing.`
                  }
                </p>

                {/* Score & XP Badges */}
                <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
                  <div className="px-4 py-2 rounded-xl bg-slate-900/80 border border-slate-700 text-sm font-semibold text-white">
                    Score: <span className="text-indigo-400">{result.score} / {result.max_score}</span> ({result.percentage}%)
                  </div>
                  {result.xp_awarded > 0 && (
                    <div className="px-4 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-sm font-semibold text-amber-400 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4" />
                      +{result.xp_awarded} XP Awarded
                    </div>
                  )}
                  <div className="px-4 py-2 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-sm font-semibold text-indigo-300 flex items-center gap-1.5">
                    <Award className="w-4 h-4" />
                    Current Rank: {result.current_rank} ({result.performance_score} Score)
                  </div>
                </div>

                {result.rank_changed && (
                  <div className="mt-3 p-3 rounded-xl bg-amber-500/20 border border-amber-500/50 text-amber-200 font-bold text-sm">
                    ⭐ Rank {result.change_type === "promotion" ? "Promoted" : "Updated"} to {result.current_rank}!
                  </div>
                )}
              </div>

              {/* Question-by-Question Breakdown */}
              <div className="space-y-4">
                <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
                  Question Evaluation & Explanations
                </h4>
                {result.results.map((q, idx) => (
                  <div
                    key={q.question_id}
                    className={`p-4 rounded-xl border ${
                      q.is_correct
                        ? "bg-slate-900/60 border-emerald-500/30"
                        : "bg-slate-900/60 border-rose-500/30"
                    } space-y-2`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-semibold text-white text-sm">
                        Q{idx + 1}. {q.question_text}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                        q.is_correct ? "bg-emerald-500/20 text-emerald-300" : "bg-rose-500/20 text-rose-300"
                      }`}>
                        {q.points_awarded} / {q.max_points} pts
                      </span>
                    </div>

                    <div className="text-xs space-y-1 pt-1">
                      <p className="text-slate-400">
                        Your answer: <span className={q.is_correct ? "text-emerald-400 font-medium" : "text-rose-400 font-medium"}>
                          {q.user_answer || "(No answer)"}
                        </span>
                      </p>
                      {!q.is_correct && (
                        <p className="text-emerald-400">
                          Correct answer: <span className="font-mono font-medium">{q.correct_answer}</span>
                        </p>
                      )}
                      {q.explanation && (
                        <p className="text-slate-300 pt-1 border-t border-slate-800 text-xs italic">
                          💡 {q.explanation}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            /* Active Test Questions View */
            <div className="space-y-6">
              {/* Question Navigation Bar */}
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-slate-400">
                    Question {currentIndex + 1} of {totalQuestions}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                    {currentQ.points} {currentQ.points === 1 ? "point" : "points"}
                  </span>
                </div>
                <div className="text-xs text-slate-400">
                  {answeredCount}/{totalQuestions} Answered
                </div>
              </div>

              {/* Question Content */}
              <div className="space-y-4">
                <h3 className="text-base sm:text-lg font-semibold text-white leading-relaxed">
                  {currentQ.question_text}
                </h3>

                {currentQ.code_snippet && (
                  <div className="rounded-xl overflow-hidden border border-slate-800 bg-slate-950 font-mono text-sm">
                    <div className="bg-slate-900/80 px-4 py-2 text-xs font-semibold text-slate-400 flex items-center gap-2 border-b border-slate-800">
                      <Terminal className="w-3.5 h-3.5 text-indigo-400" />
                      Python Snippet
                    </div>
                    <pre className="p-4 text-slate-200 overflow-x-auto text-xs sm:text-sm">
                      <code>{currentQ.code_snippet}</code>
                    </pre>
                  </div>
                )}

                {/* Answer Options */}
                {currentQ.options && currentQ.options.length > 0 ? (
                  <div className="space-y-2 pt-2">
                    {currentQ.options.map((opt, oIdx) => {
                      const isSelected = answers[currentQ.id] === opt || answers[currentQ.id] === String(oIdx);
                      return (
                        <button
                          key={oIdx}
                          onClick={() => handleSelectOption(currentQ.id, opt)}
                          className={`w-full text-left p-3.5 rounded-xl border text-sm font-medium transition-all flex items-center gap-3 ${
                            isSelected
                              ? "bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-500/10"
                              : "bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-900/60"
                          }`}
                        >
                          <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                            isSelected ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400"
                          }`}>
                            {String.fromCharCode(65 + oIdx)}
                          </span>
                          <span className="flex-1 font-mono text-xs sm:text-sm">{opt}</span>
                        </button>
                      );
                    })}
                  </div>
                ) : (
                  /* Short Answer input */
                  <div className="pt-2">
                    <label className="block text-xs font-medium text-slate-400 mb-2">
                      Type your exact answer or output:
                    </label>
                    <input
                      type="text"
                      value={answers[currentQ.id] || ""}
                      onChange={(e) => handleSelectOption(currentQ.id, e.target.value)}
                      placeholder="e.g. 42 or True"
                      className="w-full px-4 py-3 rounded-xl bg-slate-950 border border-slate-700 text-white font-mono text-sm focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer Navigation Bar */}
        <div className="bg-slate-950/80 border-t border-slate-800 px-6 py-4 flex items-center justify-between">
          {result ? (
            <div className="w-full flex items-center justify-between">
              <button
                onClick={() => {
                  setResult(null);
                  setAnswers({});
                  setCurrentIndex(0);
                  setSecondsRemaining((test.time_limit_minutes || 20) * 60);
                  setTimerActive(true);
                }}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium flex items-center gap-2 transition-colors"
              >
                <RotateCcw className="w-4 h-4" />
                Retry Assessment
              </button>
              <button
                onClick={onClose}
                className="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold transition-colors"
              >
                Done
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
                disabled={currentIndex === 0}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-white text-sm font-medium flex items-center gap-2 transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Previous
              </button>

              <div className="flex items-center gap-2">
                {isLastQuestion ? (
                  <button
                    onClick={handleSubmit}
                    disabled={submitting}
                    className="px-6 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-sm font-semibold flex items-center gap-2 transition-colors shadow-lg shadow-emerald-600/20"
                  >
                    {submitting ? (
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                    Submit Assessment
                  </button>
                ) : (
                  <button
                    onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
                    className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold flex items-center gap-2 transition-colors shadow-lg shadow-indigo-600/20"
                  >
                    Next
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </>
          )}
        </div>

      </div>
    </div>
  );
}
