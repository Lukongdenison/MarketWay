import React, { useState } from 'react';
import { Send, Mic } from 'lucide-react';

interface InputBarProps {
    onSend: (message: string) => void;
    loading: boolean;
}

export function InputBar({ onSend, loading }: InputBarProps) {
    const [input, setInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !loading) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="relative w-full">
            <div className="relative flex items-center">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about products, lines, or directions..."
                    disabled={loading}
                    className="w-full pl-6 pr-24 py-4 bg-white/80 backdrop-blur-md border border-gray-200 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all disabled:opacity-50 text-gray-700 placeholder-gray-400"
                />
                <div className="absolute right-2 flex gap-1">
                    <button
                        type="button"
                        className="p-2 text-gray-400 hover:text-blue-600 transition-colors rounded-full hover:bg-blue-50"
                        title="Voice input (coming soon)"
                    >
                        <Mic size={20} />
                    </button>
                    <button
                        type="submit"
                        disabled={!input.trim() || loading}
                        className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-md"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </form>
    );
}
