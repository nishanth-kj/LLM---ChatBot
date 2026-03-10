import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import './ChatContainer.css'

function ChatContainer({ messages, isLoading }) {
    const containerRef = useRef(null)

    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight
        }
    }, [messages, isLoading])

    return (
        <div className="chat-container" ref={containerRef}>
            <div className="messages">
                {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                ))}
                {isLoading && (
                    <div className="loading-indicator">
                        <div className="typing-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default ChatContainer
