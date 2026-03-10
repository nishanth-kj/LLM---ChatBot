export type Role = "user" | "bot";

export interface Message {
    text: string;
    sender: Role;
}

export interface ChatRequest {
    question: string;
}

export interface ChatResponse {
    answer: string;
    question: string;
}
