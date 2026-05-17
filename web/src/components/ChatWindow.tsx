"use client";

import { useState, useRef, useEffect } from "react";
import { Message as MessageComponent } from "./Message";
import { Message as MessageType } from "../types/chat";
import { apiClient } from "../lib/api-client";

export const ChatWindow = () => {
    const [messages, setMessages] = useState<MessageType[]>([
        { text: "Hello! Welcome to the LLM Playground. How can I assist you with your queries today?", sender: "bot" },
    ]);
    const [inputValue, setInputValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isUploadingFile, setIsUploadingFile] = useState(false);
    const [models, setModels] = useState<string[]>([]);
    const [currentModel, setCurrentModel] = useState<string | null>(null);
    const [isSwitchingModel, setIsSwitchingModel] = useState(false);
    const [chatStatus, setChatStatus] = useState<string | null>(null);
    const outputRef = useRef<HTMLDivElement>(null);

    // Fetch models on load directly from Python API using simple apiClient instance
    useEffect(() => {
        const loadModels = async () => {
            try {
                const response = await apiClient.get<any>("/models");
                if (response && response.success) {
                    const data = response.data;
                    setModels(data.models || []);
                    setCurrentModel(data.current_model);
                }
            } catch (err) {
                console.error("Failed to load models:", err);
            }
        };
        loadModels();
    }, []);

    useEffect(() => {
        if (outputRef.current) {
            outputRef.current.scrollTop = outputRef.current.scrollHeight;
        }
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (inputValue.trim() !== "" && !isLoading) {
            const userMessage = inputValue;
            setMessages((prev) => [...prev, { text: userMessage, sender: "user" }]);
            setInputValue("");
            setIsLoading(true);

            try {
                const response = await apiClient.post<any>("/chat", {
                    question: userMessage,
                });
                
                let answer = "Error generating response";
                if (response && response.success) {
                    answer = response.data.answer;
                } else if (response && response.answer) {
                    answer = response.answer;
                }

                setMessages((prev) => [...prev, { text: answer, sender: "bot" }]);
            } catch (error) {
                setMessages((prev) => [
                    ...prev,
                    { text: "Error: Could not connect to the backend or no model loaded.", sender: "bot" },
                ]);
            } finally {
                setIsLoading(false);
            }
        }
    };

    const handleModelChange = async (newModel: string) => {
        if (newModel && newModel !== currentModel) {
            setIsSwitchingModel(true);
            setChatStatus(`Loading model: ${newModel}...`);
            try {
                await apiClient.post("/models/switch", {
                    model_filename: newModel,
                });
                setCurrentModel(newModel);
                setMessages((prev) => [
                    ...prev,
                    { text: `🤖 Playgroup switched successfully to model: ${newModel}`, sender: "bot" },
                ]);
            } catch (err) {
                console.error("Error switching model:", err);
                setMessages((prev) => [
                    ...prev,
                    { text: `❌ Failed to switch to model: ${newModel}. Make sure the model exists.`, sender: "bot" },
                ]);
            } finally {
                setIsSwitchingModel(false);
                setChatStatus(null);
            }
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setIsUploadingFile(true);
        setChatStatus(`Uploading & Indexing ${file.name}...`);
        
        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("http://localhost:8000/api/documents/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed with status ${response.status}`);
            }

            setMessages((prev) => [
                ...prev,
                { text: `📚 Successfully uploaded and indexed document: "${file.name}" into RAG memory. The model can now answer questions about it.`, sender: "bot" }
            ]);
            setChatStatus("Document indexing complete.");
            setTimeout(() => setChatStatus(null), 3000);
        } catch (err) {
            console.error("Error uploading document:", err);
            setMessages((prev) => [
                ...prev,
                { text: `❌ Failed to upload document "${file.name}": ${(err as Error).message}`, sender: "bot" }
            ]);
        } finally {
            setIsUploadingFile(false);
            e.target.value = "";
        }
    };

    const handleClearMemory = async () => {
        try {
            await apiClient.post("/reset");
            setMessages([
                { text: "Chat history cleared. Start typing your new question below!", sender: "bot" }
            ]);
            setChatStatus("Conversation reset completed.");
            setTimeout(() => setChatStatus(null), 3000);
        } catch (err) {
            console.error("Error resetting chat memory:", err);
        }
    };

    return (
        <div className="chat-container">
            {/* Top Toolbar for LLM Playground Configuration */}
            <div className="playground-toolbar">
                <div className="model-selector-group">
                    <label htmlFor="model-select">Active LLM Model:</label>
                    <select
                        id="model-select"
                        value={currentModel || ""}
                        onChange={(e) => handleModelChange(e.target.value)}
                        disabled={isSwitchingModel || isLoading || isUploadingFile}
                        className="model-select-dropdown"
                    >
                        <option value="" disabled>-- Select Local GGUF/BIN Model --</option>
                        {models.length === 0 ? (
                            <option value="" disabled>No models found in root/models directory</option>
                        ) : (
                            models.map((model) => (
                                <option key={model} value={model}>
                                    {model}
                                </option>
                            ))
                        )}
                    </select>
                </div>

                {/* RAG PDF File Uploader */}
                <div className="upload-group">
                    <label 
                        htmlFor="rag-upload" 
                        className="upload-label" 
                        style={{ cursor: (isSwitchingModel || isLoading || isUploadingFile) ? "not-allowed" : "pointer" }}
                    >
                        {isUploadingFile ? "⏳ Indexing PDF..." : "📁 Upload PDF for RAG"}
                    </label>
                    <input
                        type="file"
                        id="rag-upload"
                        accept=".pdf"
                        onChange={handleFileUpload}
                        disabled={isSwitchingModel || isLoading || isUploadingFile}
                        style={{ display: "none" }}
                    />
                </div>

                <button
                    onClick={handleClearMemory}
                    className="reset-button"
                    disabled={isSwitchingModel || isLoading || isUploadingFile}
                    title="Clear Conversation Memory"
                >
                    🧹 Clear Memory
                </button>
            </div>

            {/* Chat Messages Log */}
            <div className="output" id="output" ref={outputRef}>
                {messages.map((msg, idx) => (
                    <MessageComponent key={idx} message={msg} />
                ))}
                
                {isLoading && (
                    <div className="typing-container">
                        <div className="bot-avatar-placeholder">🤖</div>
                        <div className="typing-bubble">
                            <span className="dot"></span>
                            <span className="dot"></span>
                            <span className="dot"></span>
                        </div>
                    </div>
                )}

                {chatStatus && (
                    <div className="status-toast">
                        <span className="spinner">⚙️</span> {chatStatus}
                    </div>
                )}
            </div>

            {/* Question Input form */}
            <div className="input-container">
                <input
                    type="text"
                    placeholder={currentModel ? "Ask the chatbot a question..." : "Please switch or load a model to begin chatting..."}
                    className="input"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    disabled={isLoading || isSwitchingModel || isUploadingFile || !currentModel}
                />
                <button 
                    onClick={handleSend} 
                    className="send-button" 
                    disabled={isLoading || isSwitchingModel || isUploadingFile || !currentModel}
                >
                    {isLoading ? "..." : "Send"}
                </button>
            </div>
        </div>
    );
};
