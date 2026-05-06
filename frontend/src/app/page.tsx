import Link from "next/link";
import { Mic } from "lucide-react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-white px-4">
      <Mic className="h-16 w-16 text-[#9333EA] mb-6" />
      <h1 className="text-4xl font-bold text-[#9333EA] mb-4">DClaw Meet</h1>
      <p className="text-lg text-gray-600 mb-8">Transcription, action items & summaries</p>
      <Link
        href="/dashboard"
        className="rounded-md bg-[#9333EA] px-6 py-3 text-white font-medium hover:bg-[#7e22ce] transition-colors"
      >
        Open Dashboard
      </Link>
    </main>
  );
}
