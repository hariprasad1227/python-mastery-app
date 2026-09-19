"use client";

import React, { useState } from "react";
import {
  BookOpen,
  Lightbulb,
  CheckCircle2,
  XCircle,
  Code,
  ChevronDown,
  ChevronRight,
  Sparkles,
  HelpCircle,
  Award,
  ArrowRight,
  Check,
  Copy,
  AlertTriangle
} from "lucide-react";
import {
  StructuredLesson,
  Subtopic,
  QuizEvaluationResponse,
  api
} from "@/lib/api";

interface LessonViewerProps {
  lesson: StructuredLesson;
  onStartCoding?: () => void;
  onQuizPassed?: (xp: number) => void;
  isCompact?: boolean;
}

export default function LessonViewer({
  lesson,
  onStartCoding,
  onQuizPassed,
  isCompact = false
}: LessonViewerProps) {
  // Accordion state: open subtopics
  const [openSubtopics, setOpenSubtopics] = useState<Record<string, boolean>>({
    [lesson.subtopics[0]?.id || ""]: true
  });

  // Quiz state
  const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({});
  const [quizSubmitting, setQuizSubmitting] = useState(false);
  const [quizResult, setQuizResult] = useState<QuizEvaluationResponse | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const toggleSubtopic = (subId: string) => {
    setOpenSubtopics((prev) => ({
      ...prev,
      [subId]: !prev[subId]
    }));
  };

  const handleCopy = (codeText: string, id: string) => {
    navigator.clipboard.writeText(codeText);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const handleSelectOption = (questionId: string, optionIndex: number) => {
    setQuizAnswers((prev) => ({
      ...prev,
      [questionId]: optionIndex
    }));
  };

  const handleQuizSubmit = async () => {
    if (!lesson.quiz || lesson.quiz.length === 0) return;
    setQuizSubmitting(true);
    try {
      const res = await api.submitLessonQuiz(lesson.id, quizAnswers);
      setQuizResult(res);
      if (res.passed && onQuizPassed) {
        onQuizPassed(res.xp_awarded);
      }
    } catch (err: any) {
      // Local fallback evaluation if network issue
      const results = lesson.quiz.map((q) => {
        const userAns = quizAnswers[q.id];
        const isCorrect = userAns === q.correct_index;
        return {
          question_id: q.id,
          question: q.question,
          user_answer: userAns,
          correct_answer: q.correct_index ?? 0,
          is_correct: isCorrect,
          explanation: q.explanation || ""
        };
      });
      const correctCount = results.filter((r) => r.is_correct).length;
      const passed = correctCount === lesson.quiz.length;
      const fakeRes: QuizEvaluationResponse = {
        lesson_id: lesson.id,
        total: lesson.quiz.length,
        correct: correctCount,
        score_percent: Math.round((correctCount / lesson.quiz.length) * 100),
        passed,
        xp_awarded: passed ? lesson.xp_reward : 0,
        results
      };
      setQuizResult(fakeRes);
      if (passed && onQuizPassed) {
        onQuizPassed(fakeRes.xp_awarded);
      }
    } finally {
      setQuizSubmitting(false);
    }
  };

  const allQuestionsAnswered =
    lesson.quiz &&
    lesson.quiz.length > 0 &&
    lesson.quiz.every((q) => quizAnswers[q.id] !== undefined);

  return (
    <div className={`space-y-6 ${isCompact ? "text-sm" : "text-base"} text-slate-100`}>
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-blue-900/40 via-indigo-900/30 to-purple-900/40 border border-blue-500/20 rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 bg-blue-500/20 border border-blue-400/30 text-blue-300 font-semibold text-xs rounded-full uppercase tracking-wider">
              Track {lesson.track_number}: {lesson.track_title}
            </span>
            <span className="px-2.5 py-0.5 bg-slate-800 border border-slate-700 text-slate-300 font-medium text-xs rounded-full">
              Level {lesson.level_number}
            </span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 rounded-full text-xs font-semibold">
            <Award className="w-3.5 h-3.5 text-emerald-400" />
            <span>+{lesson.xp_reward} Lesson XP</span>
          </div>
        </div>

        <h1 className="text-xl md:text-2xl font-bold text-white mb-2 flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-blue-400 shrink-0" />
          {lesson.title}
        </h1>
        <p className="text-slate-300 leading-relaxed text-sm">
          {lesson.introduction}
        </p>

        {/* Learning Objectives */}
        {lesson.learning_objectives && lesson.learning_objectives.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-700/50">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              What You Will Master:
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {lesson.learning_objectives.map((obj, i) => (
                <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{obj}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Educational Pipeline Steps Navigator */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 text-xs text-slate-400">
        <span className="px-2.5 py-1 bg-blue-500/20 text-blue-300 rounded-md font-medium shrink-0">
          1. Concept
        </span>
        <span className="text-slate-600">→</span>
        <span className="px-2.5 py-1 bg-amber-500/20 text-amber-300 rounded-md font-medium shrink-0">
          2. Analogy
        </span>
        <span className="text-slate-600">→</span>
        <span className="px-2.5 py-1 bg-indigo-500/20 text-indigo-300 rounded-md font-medium shrink-0">
          3. Syntax
        </span>
        <span className="text-slate-600">→</span>
        <span className="px-2.5 py-1 bg-emerald-500/20 text-emerald-300 rounded-md font-medium shrink-0">
          4. Examples
        </span>
        <span className="text-slate-600">→</span>
        <span className="px-2.5 py-1 bg-rose-500/20 text-rose-300 rounded-md font-medium shrink-0">
          5. Pitfalls
        </span>
        <span className="text-slate-600">→</span>
        <span className="px-2.5 py-1 bg-purple-500/20 text-purple-300 rounded-md font-medium shrink-0">
          6. Concept Quiz
        </span>
      </div>

      {/* Expandable Subtopics List */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-white flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Code className="w-5 h-5 text-indigo-400" />
            Core Subtopics & Explanations ({lesson.subtopics.length})
          </span>
          <button
            onClick={() => {
              const allOpen = lesson.subtopics.every((s) => openSubtopics[s.id]);
              const newState: Record<string, boolean> = {};
              lesson.subtopics.forEach((s) => {
                newState[s.id] = !allOpen;
              });
              setOpenSubtopics(newState);
            }}
            className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            {lesson.subtopics.every((s) => openSubtopics[s.id])
              ? "Collapse All"
              : "Expand All"}
          </button>
        </h2>

        {lesson.subtopics.map((sub: Subtopic) => {
          const isOpen = !!openSubtopics[sub.id];

          return (
            <div
              key={sub.id}
              className="bg-slate-900/70 border border-slate-800 hover:border-slate-700/80 rounded-xl overflow-hidden transition-all shadow-md"
            >
              {/* Subtopic Header Accordion Button */}
              <button
                onClick={() => toggleSubtopic(sub.id)}
                className="w-full flex items-center justify-between p-4 text-left hover:bg-slate-800/40 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs transition-colors ${
                      isOpen
                        ? "bg-indigo-600 text-white shadow-indigo-500/20 shadow-md"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {sub.order}
                  </div>
                  <span className="font-semibold text-slate-200 hover:text-white">
                    {sub.title}
                  </span>
                </div>
                {isOpen ? (
                  <ChevronDown className="w-5 h-5 text-indigo-400 shrink-0" />
                ) : (
                  <ChevronRight className="w-5 h-5 text-slate-500 shrink-0" />
                )}
              </button>

              {/* Subtopic Expanded Content */}
              {isOpen && (
                <div className="px-5 pb-5 space-y-4 border-t border-slate-800/60 bg-slate-950/40">
                  {/* Conceptual Explanation */}
                  <div className="pt-3">
                    <p className="text-slate-300 leading-relaxed text-sm">
                      {sub.explanation}
                    </p>
                  </div>

                  {/* Real-Life Analogy Box */}
                  {sub.analogy && (
                    <div className="bg-amber-950/20 border border-amber-500/30 rounded-xl p-4 flex items-start gap-3">
                      <div className="w-7 h-7 rounded-lg bg-amber-500/20 flex items-center justify-center shrink-0 mt-0.5">
                        <Lightbulb className="w-4 h-4 text-amber-400" />
                      </div>
                      <div>
                        <div className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-1">
                          Real-Life Analogy
                        </div>
                        <p className="text-slate-300 text-xs leading-relaxed">
                          {sub.analogy}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Syntax Breakdown */}
                  {sub.syntax && (
                    <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-4">
                      <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <Code className="w-3.5 h-3.5 text-indigo-400" />
                        Syntax Pattern
                      </div>
                      <div className="bg-slate-950 p-2.5 rounded-lg font-mono text-xs text-indigo-300 mb-3 border border-slate-800">
                        {sub.syntax.code}
                      </div>
                      {sub.syntax.breakdown && sub.syntax.breakdown.length > 0 && (
                        <div className="space-y-1.5">
                          {sub.syntax.breakdown.map((item, idx) => (
                            <div
                              key={idx}
                              className="flex items-start gap-2 text-xs bg-slate-800/40 px-3 py-1.5 rounded-md"
                            >
                              <code className="font-mono text-indigo-300 font-semibold shrink-0">
                                {item.part}
                              </code>
                              <span className="text-slate-400">:</span>
                              <span className="text-slate-300">{item.meaning}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Code Examples & Walkthrough */}
                  {sub.examples && sub.examples.length > 0 && (
                    <div className="space-y-3">
                      {sub.examples.map((ex, exIdx) => (
                        <div
                          key={exIdx}
                          className="bg-slate-900 border border-slate-800 rounded-xl p-4"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                              <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                              {ex.title}
                            </span>
                            <button
                              onClick={() => handleCopy(ex.code, `${sub.id}-${exIdx}`)}
                              className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1 bg-slate-800 px-2 py-0.5 rounded transition-colors"
                            >
                              {copiedCode === `${sub.id}-${exIdx}` ? (
                                <>
                                  <Check className="w-3 h-3 text-emerald-400" /> Copied
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" /> Copy
                                </>
                              )}
                            </button>
                          </div>

                          {/* Code Block */}
                          <pre className="bg-slate-950 text-slate-200 p-3 rounded-lg font-mono text-xs overflow-x-auto border border-slate-800 leading-relaxed">
                            {ex.code}
                          </pre>

                          {/* Expected Output */}
                          {ex.expected_output && (
                            <div className="mt-2.5">
                              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                                Output:
                              </div>
                              <pre className="bg-black/60 text-emerald-400 font-mono text-xs p-2 rounded border border-emerald-950/40">
                                {ex.expected_output}
                              </pre>
                            </div>
                          )}

                          {/* Line-by-Line Explanation */}
                          {ex.line_by_line && ex.line_by_line.length > 0 && (
                            <div className="mt-3 pt-2.5 border-t border-slate-800">
                              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                                Line-by-Line Breakdown:
                              </div>
                              <div className="space-y-1">
                                {ex.line_by_line.map((lbl, lineIdx) => (
                                  <div
                                    key={lineIdx}
                                    className="text-xs flex items-start gap-2 bg-slate-800/30 p-1.5 rounded"
                                  >
                                    <code className="text-indigo-300 font-mono shrink-0">
                                      {lbl.line}
                                    </code>
                                    <span className="text-slate-500">→</span>
                                    <span className="text-slate-300">
                                      {lbl.explanation}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Common Mistakes (Don't Do This) */}
                  {sub.common_mistakes && sub.common_mistakes.length > 0 && (
                    <div className="space-y-3">
                      <div className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                        Common Mistakes to Avoid
                      </div>

                      {sub.common_mistakes.map((mistake, mIdx) => (
                        <div
                          key={mIdx}
                          className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 space-y-2.5"
                        >
                          <div className="text-xs font-semibold text-slate-200">
                            {mistake.description}
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                            {/* Incorrect */}
                            <div className="bg-rose-950/30 border border-rose-900/50 rounded-lg p-2.5">
                              <div className="text-rose-400 font-bold mb-1 flex items-center gap-1">
                                <XCircle className="w-3.5 h-3.5 text-rose-400" />
                                ❌ Incorrect
                              </div>
                              <pre className="font-mono text-[11px] text-rose-200 whitespace-pre-wrap">
                                {mistake.incorrect_code}
                              </pre>
                            </div>

                            {/* Correct */}
                            <div className="bg-emerald-950/30 border border-emerald-900/50 rounded-lg p-2.5">
                              <div className="text-emerald-400 font-bold mb-1 flex items-center gap-1">
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                                ✅ Correct
                              </div>
                              <pre className="font-mono text-[11px] text-emerald-200 whitespace-pre-wrap">
                                {mistake.correct_code}
                              </pre>
                            </div>
                          </div>

                          <div className="text-xs text-slate-400 italic">
                            <span className="font-semibold text-slate-300">Why it fails: </span>
                            {mistake.why_it_fails}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Concept Check Quiz Section */}
      {lesson.quiz && lesson.quiz.length > 0 && (
        <div className="bg-gradient-to-br from-slate-900 via-purple-950/20 to-slate-900 border border-purple-500/30 rounded-2xl p-5 space-y-4 shadow-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center">
                <HelpCircle className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <h3 className="font-bold text-white text-base">
                  Concept Check Quiz ({lesson.quiz.length} Questions)
                </h3>
                <p className="text-xs text-slate-400">
                  Verify your understanding before starting the code challenge.
                </p>
              </div>
            </div>
            {quizResult && quizResult.passed && (
              <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-full text-xs font-semibold flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Passed (+{quizResult.xp_awarded} XP)
              </span>
            )}
          </div>

          <div className="space-y-4">
            {lesson.quiz.map((q, qIndex) => {
              const selectedOpt = quizAnswers[q.id];
              const questionEval = quizResult?.results?.find(
                (r) => r.question_id === q.id
              );

              return (
                <div
                  key={q.id}
                  className={`p-4 rounded-xl border transition-all ${
                    questionEval
                      ? questionEval.is_correct
                        ? "bg-emerald-950/20 border-emerald-800/50"
                        : "bg-rose-950/20 border-rose-800/50"
                      : "bg-slate-900/60 border-slate-800"
                  }`}
                >
                  <div className="font-semibold text-slate-200 text-sm mb-3">
                    <span className="text-purple-400 mr-1.5">Q{qIndex + 1}.</span>
                    {q.question}
                  </div>

                  <div className="space-y-2">
                    {q.options.map((opt, optIndex) => {
                      const isSelected = selectedOpt === optIndex;
                      const isCorrectAnswer =
                        questionEval && questionEval.correct_answer === optIndex;
                      const isWrongSelection =
                        questionEval && isSelected && !questionEval.is_correct;

                      let optClass =
                        "bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800 hover:border-slate-600";

                      if (questionEval) {
                        if (isCorrectAnswer) {
                          optClass =
                            "bg-emerald-900/40 border-emerald-500/60 text-emerald-200 font-semibold";
                        } else if (isWrongSelection) {
                          optClass =
                            "bg-rose-900/40 border-rose-500/60 text-rose-200";
                        }
                      } else if (isSelected) {
                        optClass =
                          "bg-purple-900/40 border-purple-500 text-purple-200 font-semibold";
                      }

                      return (
                        <label
                          key={optIndex}
                          onClick={() => handleSelectOption(q.id, optIndex)}
                          className={`flex items-center gap-3 p-3 rounded-lg border text-xs cursor-pointer transition-all ${optClass}`}
                        >
                          <input
                            type="radio"
                            name={q.id}
                            checked={isSelected}
                            onChange={() => handleSelectOption(q.id, optIndex)}
                            className="text-purple-600 focus:ring-purple-500 h-3.5 w-3.5"
                          />
                          <span className="flex-1">{opt}</span>
                          {questionEval && isCorrectAnswer && (
                            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                          )}
                          {questionEval && isWrongSelection && (
                            <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                          )}
                        </label>
                      );
                    })}
                  </div>

                  {/* Question Explanation Feedback */}
                  {questionEval && (
                    <div
                      className={`mt-3 p-3 rounded-lg text-xs flex items-start gap-2 ${
                        questionEval.is_correct
                          ? "bg-emerald-950/40 text-emerald-300 border border-emerald-800/40"
                          : "bg-rose-950/40 text-rose-300 border border-rose-800/40"
                      }`}
                    >
                      {questionEval.is_correct ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                      )}
                      <div>
                        <span className="font-bold">
                          {questionEval.is_correct ? "Correct! " : "Incorrect. "}
                        </span>
                        {questionEval.explanation}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <button
              onClick={handleQuizSubmit}
              disabled={!allQuestionsAnswered || quizSubmitting}
              className={`px-5 py-2.5 rounded-xl font-semibold text-xs transition-all shadow-md flex items-center gap-2 ${
                allQuestionsAnswered
                  ? "bg-purple-600 hover:bg-purple-500 text-white shadow-purple-500/20 cursor-pointer"
                  : "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
              }`}
            >
              {quizSubmitting ? (
                <span>Evaluating...</span>
              ) : (
                <>
                  <Award className="w-4 h-4" />
                  <span>Check Answers & Claim XP</span>
                </>
              )}
            </button>

            {quizResult && (
              <div className="text-xs">
                Score:{" "}
                <span
                  className={`font-bold ${
                    quizResult.passed ? "text-emerald-400" : "text-rose-400"
                  }`}
                >
                  {quizResult.correct} / {quizResult.total} ({quizResult.score_percent}%)
                </span>
                {quizResult.passed && (
                  <span className="text-emerald-400 ml-2 font-medium">
                    🎉 Concept Mastered!
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Launch Code Challenge CTA */}
      {onStartCoding && (
        <div className="pt-2">
          <button
            onClick={onStartCoding}
            className="w-full py-3.5 px-6 bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 hover:from-emerald-500 hover:to-teal-600 text-white font-bold rounded-xl shadow-lg shadow-emerald-900/30 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 text-sm"
          >
            <span>Proceed to Coding Practice & Sandbox</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
