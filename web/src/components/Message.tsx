import { Message as MessageType } from "../types/chat";

interface MessageProps {
    message: MessageType;
}

export const Message = ({ message }: MessageProps) => {
    const isBot = message.sender === "bot";

    return isBot ? (
        <div className="profile" style={{ marginBottom: 10 }}>
            <div className="text" style={{ display: "inline-block" }}>
                <p style={{ fontSize: "13px", fontFamily: "Arial", margin: 0, padding: "6px 3px 3px 3px" }}>
                    {message.text}
                </p>
            </div>
        </div>
    ) : (
        <div className="message-wrapper">
            <div className="user-message">
                <p style={{ fontSize: "13px", fontFamily: "Arial", margin: 0, padding: "6px 3px 3px 3px", color: "black" }}>
                    {message.text}
                </p>
            </div>
            <div className="profile"></div>
        </div>
    );
};
