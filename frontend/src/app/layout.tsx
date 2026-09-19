import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Python Mastery · Interactive Classroom & Progression",
  description: "Master Python from fundamentals to advanced data structures with sandboxed execution and AI mentorship.",
};

import AIAssistantDrawer from "../components/AIAssistantDrawer";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-950 text-slate-100">
        {children}
        <AIAssistantDrawer />
      </body>
    </html>
  );
}
