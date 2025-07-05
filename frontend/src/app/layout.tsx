// Layout file for the Smart Todo Next.js app
// Sets up global metadata and the root HTML structure for all pages

import type { Metadata } from "next";
import "./globals.css";

// Metadata for the application (used by Next.js for SEO and browser info)
export const metadata: Metadata = {
  title: "Smart Todo - AI-Powered Task Management",
  description: "Intelligent task management with AI-powered prioritization, deadline suggestions, and context-aware recommendations.",
  keywords: "todo, task management, AI, productivity, smart todo",
  authors: [{ name: "Smart Todo Team" }],
  viewport: "width=device-width, initial-scale=1",
};

// RootLayout wraps all pages and provides the main HTML structure
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
