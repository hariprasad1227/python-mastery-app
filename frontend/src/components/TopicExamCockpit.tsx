"use client";

import React, { useState, useEffect, useMemo } from "react";
import {
  HelpCircle,
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
  ShieldAlert,
  BookOpen,
  Code2,
  Bug,
  Terminal,
  Send
} from "lucide-react";
import {
  api,
  TopicExam,
  ExamQuestionItem,
  ExamSubmitResult
} from "@/lib/api";

interface TopicExamCockpitProps {
  topicId: string;
  topicTitle: string;
  onClose: () => void;
  onExamPassed: (nextTopicId?: string | null, xpAwarded?: number) => void;
  onReviewLesson?: () => void;
}

export default function TopicExamCockpit({
  topicId,
  topicTitle,
  onClose,
  onExamPassed,
  onReviewLesson
}: TopicExamCockpitProps) {
  const [exam, setExam] = useState<TopicExam | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Exam taking state
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [timeLeftSeconds, setTimeLeftSeconds] = useState<number>(15 * 60);
  const [isCompleted, setIsCompleted] = useState(false);
  const [submitResult, setSubmitResult] = useState<ExamSubmitResult | null>(null);

  // Load exam questions
  useEffect(() => {
    async function loadExam() {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getTopicExam(topicId);
        setExam(data);
        setTimeLeftSeconds((data.time_limit_minutes || 15) * 60);
      } catch (err: any) {
        setError(err.message || "Failed to load topic exam questions.");
      } finally {
        setLoading(false);
      }
    }
    loadExam();
  }, [topicId]);

  // Countdown timer
  useEffect(() => {
    if (isCompleted || loading || !exam) return;
    const interval = setInterval(() => {
      setTimeLeftSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleSubmitExam(); // Auto-submit when time expires
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [isCompleted, loading, exam, answers]);

  const currentQuestion: ExamQuestionItem | undefined = exam?.questions[currentIndex];

  const handleSelectOption = (questionId: string, value: string) => {
    if (isCompleted) return;
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value
    }));
  };

  const answeredCount = useMemo(() => {
    return Object.keys(answers).length;
  }, [answers]);

  const totalQuestions = exam?.questions.length || 0;

  const handleSubmitExam = async () => {
    if (!exam || submitting) return;

    // Check if unanswered
    if (answeredCount < totalQuestions) {
      const confirmSubmit = window.confirm(
        `You have answered ${answeredCount} of ${totalQuestions} questions. Do you want to submit now?`
      );
      if (!confirmSubmit) return;
    }

    setSubmitting(true);
    try {
      const result = await api.submitTopicExam(exam.id, answers);
      setSubmitResult(result);
      setIsCompleted(true);
      if (result.passed) {
        onExamPassed(result.next_unlocked_topic_id, result.xp_awarded);
      }
    } catch (err: any) {
      alert("Error submitting exam: " + (err.message || "Please try again"));
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetryExam = () => {
    setAnswers({});
    setCurrentIndex(0);
    setIsCompleted(false);
    setSubmitResult(null);
    if (exam) {
      setTimeLeftSeconds((exam.time_limit_minutes || 15) * 60);
    }
  };

  // Format time remaining
  const minutes = Math.floor(timeLeftSeconds / 60);
  const seconds = timeLeftSeconds % 60;
  const timeFormatted = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;

  const renderQuestionTypeBadge = (type: string) => {
    switch (type) {
      case "output_prediction":
        return (
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20 flex items-center gap-1">
            <Terminal className="w-3 h-3" /> Predict Output
          </span>
        );
      case "debugging":
        return (
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center gap-1">
            <Bug className="w-3 h-3" /> Debugging Question
          </span>
        );
      case "short_answer":
        return (
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 flex items-center gap-1">
            <Code2 className="w-3 h-3" /> Short Answer
          </span>
        );
      default:
        return (
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center gap-1">
            <HelpCircle className="w-3 h-3" /> Multiple Choice
          </span>
        );
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-4xl rounded-2xl shadow-2xl flex flex-col max-h-[92vh] overflow-hidden my-auto">
        {/* Exam Header */}
        <div className="border-b border-slate-800 bg-slate-950/70 p-4 sm:p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-600/20 text-white font-bold">
              📝
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                  Topic Examination
                </span>
                <span className="text-slate-600">•</span>
                <span className="text-xs text-amber-400 font-semibold">
                  Pass Mark: 70% Required
                </span>
              </div>
              <h2 className="text-base sm:text-lg font-black text-white">
                {exam?.title || `${topicTitle} Mastery Exam`}
              </h2>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {!isCompleted && !loading && exam && (
              <div
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border font-mono text-xs font-bold ${
                  timeLeftSeconds < 120
                    ? "bg-rose-500/20 border-rose-500/40 text-rose-300 animate-pulse"
                    : "bg-slate-800/80 border-slate-700 text-slate-300"
                }`}
              >
                <Clock className="w-3.5 h-3.5" />
                <span>{timeFormatted}</span>
              </div>
            )}
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition"
              title="Close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Body Content */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {loading ? (
            <div className="py-20 text-center space-y-3">
              <div className="w-10 h-10 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <div className="text-sm font-semibold text-slate-300">
                Preparing topic exam questions...
              </div>
              <div className="text-xs text-slate-500">
                Server is verifying topic prerequisites and loading exam items.
              </div>
            </div>
          ) : error ? (
            <div className="py-12 px-6 text-center space-y-4 max-w-md mx-auto">
              <div className="w-12 h-12 rounded-full bg-rose-500/20 border border-rose-500/40 text-rose-400 flex items-center justify-center mx-auto text-xl">
                ⚠️
              </div>
              <h3 className="text-base font-bold text-white">Exam Unavailable</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{error}</p>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold transition"
              >
                Return to Classroom
              </button>
            </div>
          ) : !isCompleted ? (
            /* ACTIVE EXAM TAKING VIEW */
            <div className="space-y-6">
              {/* Question Stepper Indicator */}
              <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-3 flex items-center justify-between gap-4">
                <div className="flex items-center gap-1.5 flex-wrap">
                  {exam?.questions.map((q, idx) => {
                    const isAnswered = answers[q.id] !== undefined && answers[q.id] !== "";
                    const isCurrent = idx === currentIndex;
                    return (
                      <button
                        key={q.id}
                        onClick={() => setCurrentIndex(idx)}
                        className={`w-7 h-7 rounded-lg text-xs font-bold transition flex items-center justify-center ${
                          isCurrent
                            ? "bg-indigo-600 text-white ring-2 ring-indigo-400/50 shadow-md"
                            : isAnswered
                            ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30"
                            : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white"
                        }`}
                      >
                        {idx + 1}
                      </button>
                    );
                  })}
                </div>

                <div className="text-xs font-semibold text-slate-400 shrink-0">
                  <span className="text-emerald-400 font-bold">{answeredCount}</span> of{" "}
                  <span className="text-white font-bold">{totalQuestions}</span> Answered
                </div>
              </div>

              {/* Current Question Body */}
              {currentQuestion && (
                <div className="bg-slate-950 border border-slate-800 rounded-2xl p-5 sm:p-6 space-y-5">
                  <div className="flex items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-black text-slate-300">
                        Question {currentIndex + 1} of {totalQuestions}
                      </span>
                      {renderQuestionTypeBadge(currentQuestion.question_type)}
                    </div>
                    <span className="text-[11px] font-bold text-slate-500">
                      {currentQuestion.points} Point{currentQuestion.points > 1 ? "s" : ""}
                    </span>
                  </div>

                  {/* Question Prompt */}
                  <div className="text-sm sm:text-base font-semibold text-white leading-relaxed">
                    {currentQuestion.prompt}
                  </div>

                  {/* Code Snippet if present */}
                  {currentQuestion.code_snippet && (
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 font-mono text-xs text-emerald-300 overflow-x-auto shadow-inner">
                      <div className="text-[10px] text-slate-500 uppercase tracking-wider mb-2 font-sans font-bold">
                        Python Code Reference
                      </div>
                      <pre className="whitespace-pre leading-relaxed font-mono">
                        {currentQuestion.code_snippet}
                      </pre>
                    </div>
                  )}

                  {/* Answer Options */}
                  <div className="space-y-2.5 pt-2">
                    {currentQuestion.options && currentQuestion.options.length > 0 ? (
                      currentQuestion.options.map((opt, optIdx) => {
                        const optLetter = String.fromCharCode(65 + optIdx);
                        const isSelected = answers[currentQuestion.id] === opt;
                        return (
                          <button
                            key={optIdx}
                            onClick={() => handleSelectOption(currentQuestion.id, opt)}
                            className={`w-full text-left p-3.5 rounded-xl border transition flex items-start gap-3 text-xs sm:text-sm font-medium ${
                              isSelected
                                ? "bg-indigo-600/20 border-indigo-500 text-white shadow-md shadow-indigo-600/10"
                                : "bg-slate-900/60 border-slate-800 text-slate-300 hover:bg-slate-850 hover:border-slate-700"
                            }`}
                          >
                            <span
                              className={`w-6 h-6 rounded-lg text-xs font-bold flex items-center justify-center shrink-0 ${
                                isSelected
                                  ? "bg-indigo-600 text-white"
                                  : "bg-slate-800 text-slate-400"
                              }`}
                            >
                              {optLetter}
                            </span>
                            <span className="leading-relaxed pt-0.5">{opt}</span>
                          </button>
                        );
                      })
                    ) : (
                      /* Short Answer text input */
                      <div className="space-y-2">
                        <label className="text-xs text-slate-400">Your Python code or answer:</label>
                        <input
                          type="text"
                          value={answers[currentQuestion.id] || ""}
                          onChange={(e) => handleSelectOption(currentQuestion.id, e.target.value)}
                          placeholder="Type your exact answer here..."
                          className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white font-mono placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Navigation & Submit Bar */}
              <div className="flex items-center justify-between pt-2">
                <button
                  onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
                  disabled={currentIndex === 0}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:pointer-events-none text-xs font-semibold text-slate-200 transition flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>Previous</span>
                </button>

                <div className="flex items-center gap-2">
                  {currentIndex < totalQuestions - 1 ? (
                    <button
                      onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
                      className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white transition flex items-center gap-1.5"
                    >
                      <span>Next</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  ) : null}

                  <button
                    onClick={handleSubmitExam}
                    disabled={submitting}
                    className="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-emerald-900/20 disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>{submitting ? "Grading on Server..." : "Submit Exam"}</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            /* COMPLETED / RESULTS REVIEW SCREEN */
            submitResult && (
              <div className="space-y-6">
                {/* Result Hero Banner */}
                <div
                  className={`p-6 sm:p-8 rounded-2xl border text-center space-y-4 shadow-xl ${
                    submitResult.passed
                      ? "bg-gradient-to-b from-emerald-950/60 to-slate-900/90 border-emerald-500/40"
                      : "bg-gradient-to-b from-rose-950/60 to-slate-900/90 border-rose-500/40"
                  }`}
                >
                  <div className="inline-flex p-3 rounded-2xl bg-slate-950/60 border border-slate-800 shadow-inner">
                    {submitResult.passed ? (
                      <CheckCircle2 className="w-12 h-12 text-emerald-400" />
                    ) : (
                      <XCircle className="w-12 h-12 text-rose-400" />
                    )}
                  </div>

                  <div>
                    <h3 className="text-xl sm:text-2xl font-black text-white">
                      {submitResult.passed
                        ? "🎉 TOPIC EXAM PASSED!"
                        : "❌ TOPIC EXAM NOT PASSED"}
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-lg mx-auto leading-relaxed">
                      {submitResult.passed
                        ? `Congratulations! You scored ${submitResult.score}/${submitResult.total_points} (${submitResult.percentage}%). The next Python topic is now permanently unlocked!`
                        : `You scored ${submitResult.score}/${submitResult.total_points} (${submitResult.percentage}%). A minimum score of ${submitResult.passing_percentage}% is required to unlock the next topic.`}
                    </p>
                  </div>

                  {/* Score & XP Metric Badges */}
                  <div className="flex items-center justify-center gap-4 pt-2">
                    <div className="bg-slate-950/80 border border-slate-800 px-4 py-2 rounded-xl text-center">
                      <div className="text-[11px] text-slate-400 uppercase font-bold">Your Score</div>
                      <div className="text-lg font-black text-white">
                        {submitResult.percentage}%
                      </div>
                    </div>
                    <div className="bg-slate-950/80 border border-slate-800 px-4 py-2 rounded-xl text-center">
                      <div className="text-[11px] text-slate-400 uppercase font-bold">Pass Mark</div>
                      <div className="text-lg font-black text-amber-400">
                        {submitResult.passing_percentage}%
                      </div>
                    </div>
                    {submitResult.passed && (
                      <div className="bg-emerald-500/10 border border-emerald-500/30 px-4 py-2 rounded-xl text-center">
                        <div className="text-[11px] text-emerald-400 uppercase font-bold">Reward</div>
                        <div className="text-lg font-black text-emerald-400">
                          +{submitResult.xp_awarded} XP
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Action CTA Buttons */}
                  <div className="flex items-center justify-center gap-3 pt-3 flex-wrap">
                    {submitResult.passed ? (
                      <>
                        {submitResult.next_unlocked_topic_id && (
                          <button
                            onClick={() => {
                              onClose();
                              window.location.href = `/learn/${submitResult.next_unlocked_topic_id}`;
                            }}
                            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-emerald-900/30"
                          >
                            <span>Continue to Next Topic</span>
                            <ArrowRight className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={onClose}
                          className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition"
                        >
                          Return to Classroom
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={handleRetryExam}
                          className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-indigo-900/30"
                        >
                          <RotateCcw className="w-4 h-4" />
                          <span>Retry Exam Now</span>
                        </button>
                        {onReviewLesson && (
                          <button
                            onClick={() => {
                              onClose();
                              onReviewLesson();
                            }}
                            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition flex items-center gap-1.5"
                          >
                            <BookOpen className="w-3.5 h-3.5" />
                            <span>Review Topic Lesson</span>
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </div>

                {/* Question-by-Question Review */}
                <div className="space-y-4 pt-2">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <span>Detailed Answer Review</span>
                      <span className="text-xs text-slate-400 font-normal">
                        ({submitResult.results.length} questions)
                      </span>
                    </h4>
                    <span className="text-xs text-slate-400">
                      Server-verified grading
                    </span>
                  </div>

                  <div className="space-y-3">
                    {submitResult.results.map((resItem, idx) => (
                      <div
                        key={resItem.question_id}
                        className={`p-4 rounded-xl border space-y-3 ${
                          resItem.is_correct
                            ? "bg-emerald-950/20 border-emerald-900/50"
                            : "bg-rose-950/20 border-rose-900/50"
                        }`}
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-slate-400">
                              Q{idx + 1}.
                            </span>
                            <span className="text-xs sm:text-sm font-semibold text-white">
                              {resItem.prompt}
                            </span>
                          </div>
                          <span
                            className={`text-xs font-bold px-2 py-0.5 rounded shrink-0 ${
                              resItem.is_correct
                                ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                                : "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                            }`}
                          >
                            {resItem.is_correct ? "CORRECT (+1 pt)" : "INCORRECT (0 pt)"}
                          </span>
                        </div>

                        {resItem.code_snippet && (
                          <pre className="bg-slate-950 border border-slate-800/80 rounded-lg p-3 font-mono text-xs text-slate-300 overflow-x-auto">
                            {resItem.code_snippet}
                          </pre>
                        )}

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-2.5">
                            <span className="text-slate-400 block text-[10px] uppercase font-bold">
                              Your Answer
                            </span>
                            <span
                              className={`font-semibold ${
                                resItem.is_correct ? "text-emerald-400" : "text-rose-400"
                              }`}
                            >
                              {resItem.user_answer || "(No answer selected)"}
                            </span>
                          </div>

                          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-2.5">
                            <span className="text-slate-400 block text-[10px] uppercase font-bold">
                              Correct Answer
                            </span>
                            <span className="font-semibold text-emerald-400">
                              {resItem.correct_answer}
                            </span>
                          </div>
                        </div>

                        {resItem.explanation && (
                          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 leading-relaxed">
                            <span className="font-bold text-indigo-300">Explanation: </span>
                            {resItem.explanation}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}
