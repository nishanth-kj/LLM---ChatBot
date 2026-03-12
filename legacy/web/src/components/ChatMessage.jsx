import './ChatMessage.css'

function ChatMessage({ message }) {
    const { text, isUser, isError } = message

    return (
        <div className={`message-wrapper ${isUser ? 'user' : 'bot'}`}>
            {!isUser && <div className="message-avatar bot-avatar"></div>}
            <div className={`message-bubble ${isUser ? 'user-message' : 'bot-message'} ${isError ? 'error' : ''}`}>
                <p>{text}</p>
            </div>
            {isUser && <div className="message-avatar user-avatar"></div>}
        </div>
    )
}

export default ChatMessage
