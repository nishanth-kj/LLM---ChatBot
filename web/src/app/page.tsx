"use client";

import { ChatWindow } from "../components/ChatWindow";

export default function Home() {
  return (
    <>
      <header>
        <div className="header-container">
          <p>LLM Playground</p>
          <div className="account">👤</div>
        </div>
      </header>
      <main>
        <div className="chatbot">
          <center>
            <p className="chatbot-text">LLM Chatbot 🤖</p>
          </center>
        </div>
        <ChatWindow />
      </main>
      <footer className="footer">
        <p style={{ fontSize: "15px", fontFamily: "Arial", margin: 0 }}>
          Copyright © 2026 LLM Chatbot | Local LLM Playground
        </p>
      </footer>
    </>
  );
}
