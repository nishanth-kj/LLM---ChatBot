"use client";

import { useState, useRef, useEffect } from "react";
import { Message as MessageComponent } from "./Message";
import { Message as MessageType } from "../types/chat";
import { chatApi } from "../api/chat";

export const ChatWindow = () => {
    const [messages, setMessages] = useState<MessageType[]>([
        { text: "Hello, How can I help you?", sender: "bot" },
    ]);
    const [inputValue, setInputValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const outputRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (outputRef.current) {
            outputRef.current.scrollTop = outputRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (inputValue.trim() !== "" && !isLoading) {
            const userMessage = inputValue;
            setMessages((prev) => [...prev, { text: userMessage, sender: "user" }]);
            setInputValue("");
            setIsLoading(true);

            try {
                const botResponse = await chatApi.sendMessage(userMessage);
                setMessages((prev) => [...prev, { text: botResponse, sender: "bot" }]);
            } catch (error) {
                setMessages((prev) => [
                    ...prev,
                    { text: "Error: Could not connect to the backend.", sender: "bot" },
                ]);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div style={{ flexGrow: 1, display: "flex", flexDirection: "column" }}>
            <div className="output" id="output" ref={outputRef}>
                {messages.map((msg, idx) => (
                    <MessageComponent key={idx} message={msg} />
                ))}
                {isLoading && (
                    <div className="profile" style={{ marginBottom: 10 }}>
                        <div className="text" style={{ display: "inline-block" }}>
                            <p style={{ fontSize: "13px", fontFamily: "Arial", margin: 0, padding: "6px 3px 3px 3px" }}>
                                Typing...
                            </p>
                        </div>
                    </div>
                )}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    placeholder="Type your message here..."
                    className="input"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    disabled={isLoading}
                />
                <button onClick={handleSend} className="send-button" disabled={isLoading}>
                    {isLoading ? "..." : "Send"}
                </button>
            </div>
        </div>
    );
};
