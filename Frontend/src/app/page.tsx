"use client";

import { ChatWindow } from "../components/ChatWindow";

export default function Home() {
  return (
    <>
      <header>
        <div className="Neuro">
          <p>Neuro Kode</p>
          <div className="account"></div>
        </div>
      </header>
      <main>
        <div className="ayur">
          <center>
            <p className="ayur-text">Ayur Bot 🤖</p>
          </center>
        </div>
        <ChatWindow />
      </main>
      <footer className="footer">
        <p style={{ fontSize: "15px", fontFamily: "Arial", margin: 0 }}>
          Copyright © 2024 Health Bot | Powered by Neuro Kode
        </p>
      </footer>
    </>
  );
}
