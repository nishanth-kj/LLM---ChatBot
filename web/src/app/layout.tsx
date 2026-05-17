import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LLM Chatbot | Local LLM Playground",
  description: "A premium local LLM Chatbot powered by Mistral and FAISS Vector Database with RAG document uploading capabilities.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link href="https://fonts.googleapis.com/css2?family=Rubik+Mono+One&display=swap" rel="stylesheet" />
      </head>
      <body className="main">
        {children}
      </body>
    </html>
  );
}
