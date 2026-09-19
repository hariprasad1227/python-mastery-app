"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api, ProjectItem, ExecuteResult } from "@/lib/api";

export default function ProjectWorkbench() {
  const params = useParams();
  const projectId = (params?.projectId as string) || "proj-1";

  const [project, setProject] = useState<ProjectItem | null>(null);
  const [code, setCode] = useState("");
  const [terminalOutput, setTerminalOutput] = useState("Ready to verify project code.");
  const [isRunning, setIsRunning] = useState(false);
  const [isPassed, setIsPassed] = useState(false);
  const [activeTab, setActiveTab] = useState<"requirements" | "terminal">("requirements");

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getProjectDetail(projectId);
        setProject(data);
        setCode(data.starter_code);
      } catch (err) {
        console.error("Failed to load project details:", err);
      }
    }
    load();
  }, [projectId]);

  async function handleVerify() {
    setIsRunning(true);
    setActiveTab("terminal");
    setTerminalOutput("Running isolated verification test harness against your project implementation...");

    try {
      const res: ExecuteResult = await api.verifyProject(projectId, code);
      let out = "";
      if (res.stdout) out += res.stdout + "\n";
      if (res.stderr) out += "Errors:\n" + res.stderr + "\n";
      out += `\nVerification Execution Time: ${res.execution_time_ms}ms | Status: ${res.status}`;
      setTerminalOutput(out.trim());

      if (res.passed) {
        setIsPassed(true);
      }
    } catch (err: any) {
      setTerminalOutput("Verification error: " + err.message);
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/projects"
            className="text-xs font-semibold text-purple-400 hover:text-purple-300 transition flex items-center gap-1"
          >
            ← Back to Projects
          </Link>
          <span className="text-slate-700">|</span>
          <span className="text-sm font-bold text-white flex items-center gap-2">
            <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-mono">
              Capstone
            </span>
            {project?.title || "Loading Project..."}
          </span>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full font-bold">
            +{project?.xp_reward || 0} XP
          </span>
          <button
            onClick={handleVerify}
            disabled={isRunning}
            className="bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs px-5 py-2 rounded-lg transition shadow-md flex items-center gap-2 disabled:opacity-50"
          >
            <span>▶</span> {isRunning ? "Testing..." : "Verify Implementation (Ctrl+Enter)"}
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex-1 grid grid-cols-12 overflow-hidden">
        {/* Left Side: Requirements & Specs */}
        <div className="col-span-5 border-r border-slate-800 bg-slate-900/40 p-6 flex flex-col gap-5 overflow-y-auto">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">
                Engineering Specification
              </span>
              <span className="text-xs text-slate-400 capitalize">• {project?.difficulty}</span>
            </div>
            <h1 className="text-2xl font-black text-white mb-2">{project?.title}</h1>
            <p className="text-sm text-slate-300 leading-relaxed">{project?.description}</p>
          </div>

          {/* Architecture Requirements */}
          <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="text-xs font-bold text-purple-400 uppercase tracking-wider">
              Functional Requirements
            </div>
            <div className="space-y-2">
              {project?.requirements.map((req, idx) => (
                <div key={idx} className="text-xs text-slate-300 flex items-start gap-2.5 leading-relaxed">
                  <span className="text-purple-400 font-bold">{idx + 1}.</span>
                  <span>{req}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tech Stack Box */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
              Technologies & Modules
            </div>
            <div className="flex flex-wrap gap-1.5">
              {project?.tech_stack.map((t) => (
                <span
                  key={t}
                  className="text-xs font-mono bg-slate-800 text-slate-300 px-2.5 py-1 rounded border border-slate-700"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>

          {isPassed && (
            <div className="p-4 bg-emerald-950/40 border border-emerald-500/40 rounded-xl text-emerald-300 text-xs flex items-center gap-3">
              <span className="text-2xl">🎉</span>
              <div>
                <div className="font-bold">Project Verified Successfully!</div>
                <div className="opacity-90">All functional specifications and edge cases passed.</div>
              </div>
            </div>
          )}
        </div>

        {/* Right Side: Code Editor & Test Console */}
        <div className="col-span-7 flex flex-col overflow-hidden bg-slate-950">
          <div className="border-b border-slate-800 bg-slate-900 px-6 py-2.5 flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-slate-400">main.py</span>
            <div className="text-[11px] text-slate-500 font-mono">
              Ctrl+Enter to Run Verification Harness
            </div>
          </div>

          <div className="flex-1 p-4 bg-slate-950 overflow-hidden">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={(e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                  e.preventDefault();
                  handleVerify();
                }
              }}
              spellCheck={false}
              className="w-full h-full bg-slate-950 text-slate-100 font-mono text-sm leading-relaxed p-4 border border-slate-800 rounded-lg outline-none resize-none focus:border-purple-500"
            />
          </div>

          {/* Verification Console */}
          <div className="h-60 border-t border-slate-800 bg-slate-900/60 p-4 flex flex-col gap-2 overflow-hidden">
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
              <span>Verification Harness Console</span>
              <span className="font-mono text-slate-500 text-[11px]">Sandboxed Python 3.11</span>
            </div>
            <div className="flex-1 bg-slate-950 border border-slate-800 rounded p-3 font-mono text-xs text-purple-300 overflow-y-auto whitespace-pre-wrap">
              {terminalOutput}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
