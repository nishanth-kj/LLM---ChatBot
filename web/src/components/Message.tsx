import { Message as MessageType } from "../types/chat";

interface MessageProps {
    message: MessageType;
}

export const Message = ({ message }: MessageProps) => {
    const isBot = message.sender === "bot";

    return isBot ? (
        <div className="profile">
            <div className="bot-avatar-placeholder">🤖</div>
            <div className="text">
                <p style={{ margin: 0 }}>
                    {message.text}
                </p>
            </div>
        </div>
    ) : (
        <div className="message-wrapper">
            <div className="user-message">
                <p style={{ margin: 0 }}>
                    {message.text}
                </p>
            </div>
        </div>
    );
};
