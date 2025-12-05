import React from 'react';
import { User, Bot } from 'lucide-react';

interface ChatBubbleProps {
    type: 'user' | 'bot';
    text: string;
    images?: string[];
}

export function ChatBubble({ type, text, images }: ChatBubbleProps) {
    const isUser = type === 'user';

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-3`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-blue-600' : 'bg-emerald-600'}`}>
                    {isUser ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
                </div>

                <div className={`flex flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>
                    <div className={`p-4 rounded-2xl ${isUser
                            ? 'bg-blue-600 text-white rounded-tr-none'
                            : 'bg-white text-gray-800 shadow-sm rounded-tl-none border border-gray-100'
                        }`}>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{text}</p>
                    </div>

                    {images && images.length > 0 && (
                        <div className="flex gap-2 overflow-x-auto max-w-full pb-2">
                            {images.map((img, idx) => (
                                <img
                                    key={idx}
                                    src={`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}${img}`}
                                    alt="Market visual"
                                    className="h-32 w-auto rounded-lg object-cover shadow-sm border border-gray-200"
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
