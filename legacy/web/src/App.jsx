import { useState, useEffect, useRef } from 'react'
import ChatContainer from './components/ChatContainer'
import ChatInput from './components/ChatInput'
import { sendMessage } from './services/api'

function App() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            text: 'Hello! I am your Healthcare Assistant. How can I help you today?',
            isUser: false,
            timestamp: new Date()
        }
    ])
    const [isLoading, setIsLoading] = useState(false)

    const handleSendMessage = async (text) => {
        if (!text.trim()) return

        const userMessage = {
            id: Date.now(),
            text: text.trim(),
            isUser: true,
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setIsLoading(true)

        try {
            const response = await sendMessage(text.trim())

            const botMessage = {
                id: Date.now() + 1,
                text: response.answer,
                isUser: false,
                timestamp: new Date()
            }

            setMessages(prev => [...prev, botMessage])
        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                text: 'Sorry, I encountered an error. Please try again.',
                isUser: false,
                timestamp: new Date(),
                isError: true
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="app">
            <header className="header">
                <div className="header-content">
                    <h1 className="logo">Neuro Kode</h1>
                    <div className="avatar"></div>
                </div>
            </header>

            <main className="main-content">
                <div className="chat-title">
                    <h2>Ayur Bot 🤖</h2>
                </div>

                <ChatContainer messages={messages} isLoading={isLoading} />
                <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
            </main>

            <footer className="footer">
                <p>Copyright © 2024 Health Bot | Powered by Neuro Kode</p>
            </footer>
        </div>
    )
}

export default App
