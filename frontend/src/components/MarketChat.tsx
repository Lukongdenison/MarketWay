import React, { useState, useRef, useEffect } from 'react';
import { useMarketApi } from '../hooks/useMarketApi';
import { ChatBubble } from './ChatBubble';
import { InputBar } from './InputBar';

interface Message {
    type: 'user' | 'bot';
    text: string;
    images?: string[];
}

export function MarketChat() {
    const [messages, setMessages] = useState<Message[]>([
        { type: 'bot', text: 'Hello! I can help you find products, locate lines, or navigate the market. What do you need?' }
    ]);
    const { loading, askMarket } = useMarketApi();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (text: string) => {
        setMessages(prev => [...prev, { type: 'user', text }]);

        try {
            const response = await askMarket(text);
            setMessages(prev => [...prev, {
                type: 'bot',
                text: response.answer,
                images: response.images
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                type: 'bot',
                text: 'Sorry, I encountered an error connecting to the market assistant. Please try again.'
            }]);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-50">
            <div className="flex-1 overflow-y-auto p-4 pb-24">
                <div className="max-w-3xl mx-auto">
                    {messages.map((msg, idx) => (
                        <ChatBubble
                            key={idx}
                            type={msg.type}
                            text={msg.text}
                            images={msg.images}
                        />
                    ))}
                    {loading && (
                        <div className="flex justify-start mb-4">
                            <div className="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm border border-gray-100">
                                <div className="flex gap-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            <div className="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-gray-50 via-gray-50 to-transparent">
                <div className="max-w-3xl mx-auto">
                    <InputBar onSend={handleSend} loading={loading} />
                </div>
            </div>
        </div>
    );
}
