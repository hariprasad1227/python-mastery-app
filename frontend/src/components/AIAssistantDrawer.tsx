"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Bot,
  X,
  Send,
  Sparkles,
  RotateCcw,
  Copy,
  Check,
  Code2,
  ChevronDown,
  Languages,
  HelpCircle,
  Bug,
  Lightbulb,
  Maximize2,
  Minimize2
} from "lucide-react";
import { api, ChatMessage, MentorChatResponse } from "../lib/api";

export default function AIAssistantDrawer() {
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [language, setLanguage] = useState<"auto" | "en" | "te">("auto");
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [activeContext, setActiveContext] = useState<{
    topic?: string;
    code?: string;
    error?: string;
  }>({});

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "### 👋 Hello! I am your AI Python Mentor.\n\nI can explain concepts, help you debug errors, break down algorithms, and guide you in **English** or **తెలుగు (Telugu)**!\n\nHow can I help your Python learning journey today?"
    }
  ]);

  const [suggestions, setSuggestions] = useState<string[]>([
    "💡 Variables & Types in Python",
    "🗣️ తెలుగులో పైథాన్ వివరించు",
    "🔄 How do Loops & Range work?",
    "🐛 Explain common Python errors"
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      inputRef.current?.focus();
    }
  }, [isOpen, messages, isLoading]);

  // Listen for custom events to trigger AI Mentor from anywhere in the app
  useEffect(() => {
    const handleTrigger = (e: any) => {
      const { topic, code, error, initialQuestion } = e.detail || {};
      setActiveContext({ topic, code, error });
      setIsOpen(true);

      if (initialQuestion) {
        handleSendMessage(initialQuestion, { topic, code, error });
      }
    };

    window.addEventListener("open-ai-mentor", handleTrigger);
    return () => window.removeEventListener("open-ai-mentor", handleTrigger);
  }, []);

  const handleSendMessage = async (
    textToSend?: string,
    overrideContext?: { topic?: string; code?: string; error?: string }
  ) => {
    const messageText = (textToSend || input).trim();
    if (!messageText || isLoading) return;

    const ctx = overrideContext || activeContext;
    const newMessages: ChatMessage[] = [
      ...messages,
      { role: "user", content: messageText }
    ];

    setMessages(newMessages);
    if (!textToSend) setInput("");
    setIsLoading(true);

    try {
      const response: MentorChatResponse = await api.chatWithMentor({
        messages: newMessages,
        current_topic: ctx.topic,
        code_context: ctx.code,
        error_context: ctx.error,
        language: language
      });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.reply }
      ]);

      if (response.suggestions && response.suggestions.length > 0) {
        setSuggestions(response.suggestions);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ Sorry, I encountered a connection glitch. Please ensure the backend server is running and try again."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content:
          "✨ Chat reset! Ask me any Python question, request code debugging, or ask in తెలుగు."
      }
    ]);
    setActiveContext({});
    setSuggestions([
      "💡 Variables & Data Types",
      "🗣️ తెలుగులో నేర్పించు",
      "🔄 For & While Loops",
      "⚡ Functions & *args"
    ]);
  };

  // Render markdown with code snippets
  const renderMessageContent = (content: string, msgIndex: number) => {
    const parts = content.split(/(```[\s\S]*?```)/g);

    return (
      <div className="space-y-2 text-sm leading-relaxed">
        {parts.map((part, i) => {
          if (part.startsWith("```") && part.endsWith("```")) {
            const lines = part.slice(3, -3).trim().split("\n");
            let lang = "python";
            let code = part.slice(3, -3).trim();
            if (lines[0] && !lines[0].includes(" ") && lines[0].length < 15) {
              lang = lines[0];
              code = lines.slice(1).join("\n");
            }
            const snippetId = msgIndex * 100 + i;

            return (
              <div
                key={i}
                className="my-3 rounded-lg overflow-hidden border border-slate-700/80 bg-slate-950 font-mono text-xs shadow-inner"
              >
                <div className="flex items-center justify-between px-3 py-1.5 bg-slate-900 border-b border-slate-800 text-slate-400">
                  <span className="flex items-center gap-1.5 font-semibold text-slate-300">
                    <Code2 className="w-3.5 h-3.5 text-violet-400" />
                    {lang || "python"}
                  </span>
                  <button
                    onClick={() => copyToClipboard(code, snippetId)}
                    className="flex items-center gap-1 px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition text-[11px]"
                  >
                    {copiedIndex === snippetId ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-400" />
                        <span className="text-emerald-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>Copy Code</span>
                      </>
                    )}
                  </button>
                </div>
                <pre className="p-3 overflow-x-auto text-emerald-300/90 whitespace-pre">
                  <code>{code}</code>
                </pre>
              </div>
            );
          }

          // Plain text / Markdown headers
          return (
            <div key={i} className="whitespace-pre-wrap">
              {part.split("\n").map((line, lineIdx) => {
                if (line.startsWith("### ")) {
                  return (
                    <h4
                      key={lineIdx}
                      className="font-bold text-base text-violet-300 mt-2 mb-1"
                    >
                      {line.replace("### ", "")}
                    </h4>
                  );
                }
                if (line.startsWith("## ")) {
                  return (
                    <h3
                      key={lineIdx}
                      className="font-bold text-lg text-white mt-3 mb-1"
                    >
                      {line.replace("## ", "")}
                    </h3>
                  );
                }
                if (line.startsWith("- ") || line.startsWith("* ")) {
                  return (
                    <div key={lineIdx} className="flex items-start gap-2 ml-2">
                      <span className="text-violet-400 mt-1">•</span>
                      <span>{line.replace(/^[-*]\s+/, "")}</span>
                    </div>
                  );
                }
                return <p key={lineIdx}>{line}</p>;
              })}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <>
      {/* Floating Trigger Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-violet-600 via-indigo-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-semibold rounded-full shadow-2xl shadow-indigo-500/40 border border-violet-400/40 transition-all duration-300 hover:scale-105 group"
          title="Open AI Python Assistant"
        >
          <div className="relative">
            <Bot className="w-6 h-6 text-white group-hover:rotate-12 transition-transform" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-slate-950 animate-pulse" />
          </div>
          <div className="text-left">
            <div className="text-xs font-bold leading-tight tracking-wide flex items-center gap-1">
              AI Python Mentor
              <Sparkles className="w-3 h-3 text-amber-300" />
            </div>
            <div className="text-[10px] text-violet-200 font-normal leading-none">
              Online · English &amp; తెలుగు
            </div>
          </div>
        </button>
      )}

      {/* Slide-Over Drawer / Floating Assistant Window */}
      {isOpen && (
        <div
          className={`fixed bottom-6 right-6 z-50 flex flex-col bg-slate-900 border border-violet-500/30 rounded-2xl shadow-2xl shadow-violet-950/80 overflow-hidden transition-all duration-300 backdrop-blur-xl ${
            isExpanded
              ? "w-[720px] max-w-[95vw] h-[820px] max-h-[92vh]"
              : "w-[440px] max-w-[92vw] h-[640px] max-h-[85vh]"
          }`}
        >
          {/* Header */}
          <div className="px-4 py-3.5 bg-gradient-to-r from-slate-900 via-violet-950/60 to-indigo-950/70 border-b border-violet-800/40 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative p-2 rounded-xl bg-violet-600/30 border border-violet-500/40 text-violet-300">
                <Bot className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                    AI Python Mentor
                    <span className="px-1.5 py-0.2 text-[9px] font-semibold bg-violet-500/20 text-violet-300 border border-violet-500/30 rounded">
                      24/7
                    </span>
                  </h3>
                </div>
                <p className="text-[11px] text-slate-400">
                  Concept guide · Code debugger · English &amp; తెలుగు
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              {/* Language Switcher */}
              <button
                onClick={() =>
                  setLanguage((l) => (l === "te" ? "en" : l === "en" ? "auto" : "te"))
                }
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition text-xs flex items-center gap-1 font-medium"
                title={`Language Mode: ${language.toUpperCase()}`}
              >
                <Languages className="w-3.5 h-3.5 text-violet-400" />
                <span className="text-[10px] uppercase font-bold text-violet-300">
                  {language === "te" ? "తెలుగు" : language === "en" ? "EN" : "AUTO"}
                </span>
              </button>

              {/* Clear Chat */}
              <button
                onClick={clearChat}
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800/80 transition"
                title="Clear conversation"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              {/* Expand/Collapse Toggle */}
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition"
                title={isExpanded ? "Collapse width" : "Expand width"}
              >
                {isExpanded ? (
                  <Minimize2 className="w-3.5 h-3.5" />
                ) : (
                  <Maximize2 className="w-3.5 h-3.5" />
                )}
              </button>

              {/* Close */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition ml-1"
                title="Close AI Assistant"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Active Context Banner if loaded from code editor */}
          {(activeContext.topic || activeContext.error) && (
            <div className="px-4 py-2 bg-indigo-950/40 border-b border-indigo-800/30 flex items-center justify-between text-xs text-indigo-300">
              <span className="truncate max-w-[280px]">
                📌 {activeContext.topic || "Active Challenge"}
                {activeContext.error && " · Error Detected"}
              </span>
              <button
                onClick={() => setActiveContext({})}
                className="text-[10px] text-indigo-400 hover:text-indigo-200 underline"
              >
                Detach
              </button>
            </div>
          )}

          {/* Messages Container */}
          <div className="flex-1 p-4 overflow-y-auto space-y-4 text-slate-200 scrollbar-thin scrollbar-thumb-slate-700">
            {messages.map((msg, index) => {
              const isUser = msg.role === "user";
              return (
                <div
                  key={index}
                  className={`flex items-start gap-2.5 ${
                    isUser ? "justify-end" : "justify-start"
                  }`}
                >
                  {!isUser && (
                    <div className="w-7 h-7 rounded-lg bg-violet-600/30 border border-violet-500/40 flex items-center justify-center text-violet-300 flex-shrink-0 mt-0.5">
                      <Bot className="w-4 h-4" />
                    </div>
                  )}

                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                      isUser
                        ? "bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-tr-none shadow-md shadow-violet-900/30"
                        : "bg-slate-800/80 border border-slate-700/60 rounded-tl-none text-slate-200 shadow"
                    }`}
                  >
                    {renderMessageContent(msg.content, index)}
                  </div>
                </div>
              );
            })}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex items-start gap-2.5 justify-start">
                <div className="w-7 h-7 rounded-lg bg-violet-600/30 border border-violet-500/40 flex items-center justify-center text-violet-300 flex-shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl rounded-tl-none px-4 py-3 text-slate-400 text-xs flex items-center gap-2">
                  <Sparkles className="w-3.5 h-3.5 text-violet-400 animate-spin" />
                  <span>AI Mentor is crafting an explanation...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestions */}
          {suggestions.length > 0 && !isLoading && (
            <div className="px-3 py-2 bg-slate-950/40 border-t border-slate-800/60 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
              <span className="text-[10px] font-semibold text-violet-400 uppercase tracking-wider pl-1 flex-shrink-0">
                Prompts:
              </span>
              {suggestions.map((sug, i) => (
                <button
                  key={i}
                  onClick={() => handleSendMessage(sug)}
                  className="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-violet-950/60 text-slate-300 hover:text-violet-200 border border-slate-700 hover:border-violet-600/50 rounded-full whitespace-nowrap transition flex-shrink-0"
                >
                  {sug}
                </button>
              ))}
            </div>
          )}

          {/* Input Box */}
          <div className="p-3 bg-slate-950 border-t border-slate-800 flex items-center gap-2">
            <textarea
              ref={inputRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about Python or request help in Telugu..."
              className="flex-1 bg-slate-900 border border-slate-800 focus:border-violet-500 text-white text-xs rounded-xl px-3.5 py-2.5 focus:outline-none resize-none placeholder-slate-500 transition max-h-24"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={!input.trim() || isLoading}
              className="p-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition shadow-lg shadow-violet-950/50"
              title="Send message"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}