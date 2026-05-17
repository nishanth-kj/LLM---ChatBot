"use client";

import { useState, useRef, useEffect } from "react";
import { Message as MessageComponent } from "./Message";
import { Message as MessageType } from "../types/chat";
import { apiClient } from "../lib/api-client";

interface PresetModel {
    name: string;
    filename: string;
    url: string;
}

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
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [documents, setDocuments] = useState<string[]>([]);
    
    // Model download states
    const [selectedPresetIdx, setSelectedPresetIdx] = useState<number>(0);
    const [downloadProgress, setDownloadProgress] = useState<number | null>(null);
    const [downloadingFilename, setDownloadingFilename] = useState<string | null>(null);

    const presets: PresetModel[] = [
        { 
            name: "Phi-3 Mini (3.8B Q4)", 
            filename: "Phi-3-mini-4k-instruct-q4.gguf", 
            url: "https://huggingface.co/Microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf" 
        },
        { 
            name: "Llama 3 Instruct (8B Q4)", 
            filename: "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf", 
            url: "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf" 
        },
        { 
            name: "Mistral Instruct (7B Q4)", 
            filename: "mistral-7b-instruct-v0.2.Q4_K_M.gguf", 
            url: "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf" 
        }
    ];

    const outputRef = useRef<HTMLDivElement>(null);

    // Load available models and documents on component load
    const loadModels = async () => {
        try {
            const response = await apiClient.get<any>("/models");
            if (response && response.status === 1) {
                const data = response.data;
                setModels(data.models || []);
                setCurrentModel(data.current_model);
            }
        } catch (err) {
            console.error("Failed to load models:", err);
        }
    };

    const loadDocuments = async () => {
        try {
            const response = await apiClient.get<any>("/documents");
            if (response && response.status === 1) {
                setDocuments(response.data || []);
            }
        } catch (err) {
            console.error("Failed to load documents list:", err);
        }
    };

    useEffect(() => {
        loadModels();
        loadDocuments();
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
                if (response && response.status === 1) {
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
            await loadDocuments();
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

    const handleDeleteDocument = async (filename: string) => {
        if (!confirm(`Are you sure you want to delete "${filename}" and rebuild the RAG index?`)) return;
        setChatStatus(`Deleting ${filename}...`);
        try {
            const response = await fetch(`http://localhost:8000/api/documents/${filename}`, {
                method: "DELETE"
            });
            if (!response.ok) {
                throw new Error("Failed to delete document");
            }
            setMessages((prev) => [
                ...prev,
                { text: `🗑️ Successfully removed "${filename}" from RAG index. Vector database rebuilt.`, sender: "bot" }
            ]);
            await loadDocuments();
        } catch (err) {
            console.error("Error deleting document:", err);
            alert(`Failed to delete document: ${(err as Error).message}`);
        } finally {
            setChatStatus(null);
        }
    };

    const handleDownloadModel = async () => {
        const preset = presets[selectedPresetIdx];
        setDownloadingFilename(preset.filename);
        setDownloadProgress(0);
        setChatStatus(`Starting download for ${preset.filename}...`);
        
        try {
            const response = await fetch("http://localhost:8000/api/models/download", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url: preset.url,
                    filename: preset.filename
                })
            });
            
            if (!response.ok) {
                throw new Error("Download request failed");
            }
            
            // Poll download status every 2 seconds
            const interval = setInterval(async () => {
                try {
                    const statusRes = await fetch("http://localhost:8000/api/models/download/status");
                    const data = await statusRes.json();
                    if (data && data.status === 1) {
                        const progress = data.data;
                        if (progress.active) {
                            setDownloadProgress(progress.percentage);
                            setChatStatus(`Downloading model: ${progress.percentage}%`);
                        } else {
                            clearInterval(interval);
                            setDownloadProgress(null);
                            setDownloadingFilename(null);
                            setChatStatus(null);
                            
                            if (progress.error) {
                                alert(`Download failed: ${progress.error}`);
                            } else {
                                setMessages((prev) => [
                                    ...prev,
                                    { text: `✅ Model "${preset.filename}" has been successfully downloaded and placed in the models directory! You can now select it in the model switcher.`, sender: "bot" }
                                ]);
                                await loadModels();
                            }
                        }
                    }
                } catch (err) {
                    console.error("Error polling status:", err);
                }
            }, 2000);
            
        } catch (err) {
            console.error("Error downloading model:", err);
            alert(`Failed to start download: ${(err as Error).message}`);
            setDownloadProgress(null);
            setDownloadingFilename(null);
            setChatStatus(null);
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
        <div className={`app-layout ${isSidebarOpen ? "sidebar-open" : "sidebar-closed"}`}>
            {/* Collapsible Left Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-header">
                    <span className="sidebar-brand">🤖 LLM Chatbot</span>
                    <button 
                        onClick={() => setIsSidebarOpen(false)}
                        className="sidebar-close-btn"
                        title="Close Sidebar"
                    >
                        ✕
                    </button>
                </div>

                <div className="sidebar-content">
                    {/* Active LLM Model Switcher */}
                    <div className="sidebar-section">
                        <span className="sidebar-section-title">Select Active Model</span>
                        <select
                            id="model-select"
                            value={currentModel || ""}
                            onChange={(e) => handleModelChange(e.target.value)}
                            disabled={isSwitchingModel || isLoading || isUploadingFile || downloadProgress !== null}
                            className="sidebar-select-dropdown"
                        >
                            <option value="" disabled>-- Select Model --</option>
                            {models.length === 0 ? (
                                <option value="" disabled>No models found</option>
                            ) : (
                                models.map((model) => (
                                    <option key={model} value={model}>
                                        {model}
                                    </option>
                                ))
                            )}
                        </select>
                    </div>

                    {/* Download Local Model Group */}
                    <div className="sidebar-section">
                        <span className="sidebar-section-title">Download Preset Models</span>
                        <select
                            value={selectedPresetIdx}
                            onChange={(e) => setSelectedPresetIdx(Number(e.target.value))}
                            disabled={downloadProgress !== null}
                            className="sidebar-select-dropdown"
                        >
                            {presets.map((preset, idx) => (
                                <option key={idx} value={idx}>
                                    {preset.name}
                                </option>
                            ))}
                        </select>
                        <button
                            onClick={handleDownloadModel}
                            disabled={downloadProgress !== null || isSwitchingModel || isLoading}
                            className="sidebar-upload-label"
                            style={{ 
                                marginTop: "0.5rem",
                                background: "#000",
                                color: "#fff",
                                border: "none",
                                width: "100%",
                                opacity: (downloadProgress !== null) ? 0.5 : 1
                            }}
                        >
                            {downloadProgress !== null ? `⏳ Down: ${downloadProgress}%` : "⬇️ Download Model"}
                        </button>
                    </div>

                    {/* RAG PDF File Uploader */}
                    <div className="sidebar-section">
                        <span className="sidebar-section-title">RAG PDF Uploader</span>
                        <label 
                            htmlFor="rag-upload" 
                            className="sidebar-upload-label" 
                            style={{ cursor: (isSwitchingModel || isLoading || isUploadingFile || downloadProgress !== null) ? "not-allowed" : "pointer" }}
                        >
                            {isUploadingFile ? "⏳ Indexing PDF..." : "📁 Upload PDF for RAG"}
                        </label>
                        <input
                            type="file"
                            id="rag-upload"
                            accept=".pdf"
                            onChange={handleFileUpload}
                            disabled={isSwitchingModel || isLoading || isUploadingFile || downloadProgress !== null}
                            style={{ display: "none" }}
                        />
                    </div>

                    {/* Manage RAG Documents (View and delete) */}
                    <div className="sidebar-section">
                        <span className="sidebar-section-title">Manage Documents ({documents.length})</span>
                        {documents.length === 0 ? (
                            <span style={{ fontSize: "0.8rem", color: "var(--accent)", fontStyle: "italic" }}>
                                No PDFs uploaded yet.
                            </span>
                        ) : (
                            <div className="documents-list-box" style={{ 
                                display: "flex", 
                                flexDirection: "column", 
                                gap: "0.4rem",
                                maxHeight: "150px",
                                overflowY: "auto",
                                border: "1px solid var(--border-color)",
                                borderRadius: "8px",
                                padding: "0.5rem",
                                background: "#fff"
                            }}>
                                {documents.map((doc) => (
                                    <div key={doc} style={{ 
                                        display: "flex", 
                                        justifyContent: "space-between", 
                                        alignItems: "center",
                                        fontSize: "0.8rem",
                                        padding: "0.2rem 0",
                                        borderBottom: "1px solid #f4f4f5",
                                        color: "var(--foreground)"
                                    }}>
                                        <span title={doc} style={{ 
                                            textOverflow: "ellipsis", 
                                            overflow: "hidden", 
                                            whiteSpace: "nowrap",
                                            maxWidth: "180px"
                                        }}>
                                            📄 {doc}
                                        </span>
                                        <button 
                                            onClick={() => handleDeleteDocument(doc)}
                                            style={{ 
                                                background: "none", 
                                                border: "none", 
                                                cursor: "pointer", 
                                                fontSize: "0.8rem" 
                                            }}
                                            title="Delete Document"
                                        >
                                            🗑️
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Chat Operations */}
                    <div className="sidebar-section" style={{ marginTop: "auto" }}>
                        <button
                            onClick={handleClearMemory}
                            className="sidebar-reset-button"
                            disabled={isSwitchingModel || isLoading || isUploadingFile || downloadProgress !== null}
                        >
                            🧹 Clear Chat Memory
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main Chat Screen Area */}
            <div className="chat-container">
                {/* Minimal Top Header for Chat Area */}
                <div className="chat-header-bar">
                    {!isSidebarOpen && (
                        <button 
                            onClick={() => setIsSidebarOpen(true)}
                            className="sidebar-open-btn"
                            title="Open Sidebar"
                        >
                            ☰
                        </button>
                    )}
                    <span className="active-model-display">
                        {currentModel ? `Model: ${currentModel}` : "No model loaded. Select/Download sidebar model"}
                    </span>
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
                        placeholder={currentModel ? "Ask the chatbot a question..." : "Please load or download a model from the sidebar to begin chatting..."}
                        className="input"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        disabled={isLoading || isSwitchingModel || isUploadingFile || downloadProgress !== null || !currentModel}
                    />
                    <button 
                        onClick={handleSend} 
                        className="send-button" 
                        disabled={isLoading || isSwitchingModel || isUploadingFile || downloadProgress !== null || !currentModel}
                    >
                        {isLoading ? "..." : "Send"}
                    </button>
                </div>
            </div>
        </div>
    );
};
