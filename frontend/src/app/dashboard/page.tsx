"use client";

import { useState } from "react";
import { Mic } from "lucide-react";

export default function Dashboard() {
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState<{
    actionItems: string[];
    keyDecisions: string[];
    sentiment: string;
  } | null>(null);

  const handleSummarize = () => {
    setResults({
      actionItems: [
        "Schedule follow-up for next Tuesday",
        "Share design mockups with the team",
        "Review budget proposal by EOD",
      ],
      keyDecisions: [
        "Adopt the new component library",
        "Delay launch by one sprint",
        "Hire two additional backend engineers",
      ],
      sentiment: "Positive",
    });
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="bg-[#9333EA] px-6 py-4 flex items-center gap-3">
        <Mic className="h-6 w-6 text-white" />
        <h1 className="text-xl font-semibold text-white">DClaw Meet</h1>
      </header>

      <div className="mx-auto max-w-6xl px-4 py-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Meeting Transcript</h2>
          <textarea
            className="w-full h-96 rounded-lg border border-gray-300 p-4 text-sm focus:border-[#9333EA] focus:ring-1 focus:ring-[#9333EA] outline-none resize-none"
            placeholder="Paste transcript..."
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
          />
          <button
            onClick={handleSummarize}
            className="rounded-md bg-[#9333EA] px-6 py-3 text-white font-medium hover:bg-[#7e22ce] transition-colors"
          >
            Summarize
          </button>
        </div>

        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900">Results</h2>
          {results ? (
            <div className="space-y-6">
              <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-200">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">Action Items</h3>
                <ul className="space-y-2">
                  {results.actionItems.map((item, i) => (
                    <li key={i} className="text-gray-800 text-sm">• {item}</li>
                  ))}
                </ul>
              </div>

              <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-200">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">Key Decisions</h3>
                <ul className="space-y-2">
                  {results.keyDecisions.map((dec, i) => (
                    <li key={i} className="text-gray-800 text-sm">• {dec}</li>
                  ))}
                </ul>
              </div>

              <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-200">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">Sentiment</h3>
                <p className="text-2xl font-bold text-[#9333EA]">{results.sentiment}</p>
              </div>
            </div>
          ) : (
            <div className="rounded-lg bg-white p-12 shadow-sm border border-gray-200 text-center text-gray-500">
              Paste a transcript and summarize to see results
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
