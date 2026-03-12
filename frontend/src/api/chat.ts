import axios from "axios";
import { ChatRequest, ChatResponse } from "../types/chat";

const API_BASE_URL = "http://localhost:8000/api";

export const chatApi = {
    sendMessage: async (question: string): Promise<string> => {
        try {
            const response = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, {
                question,
            });
            return response.data.answer;
        } catch (error) {
            console.error("Error sending message:", error);
            throw error;
        }
    },
    resetSession: async (): Promise<void> => {
        try {
            await axios.post(`${API_BASE_URL}/reset`);
        } catch (error) {
            console.error("Error resetting session:", error);
            throw error;
        }
    },
};
