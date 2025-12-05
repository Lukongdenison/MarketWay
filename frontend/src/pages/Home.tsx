import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MessageSquare, Search, MapPin } from 'lucide-react';

export function Home() {
    const navigate = useNavigate();

    return (
        <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center p-6 bg-gradient-to-b from-blue-50 to-white">
            <div className="text-center mb-12 max-w-2xl">
                <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 tracking-tight">
                    Navigate the Market with <span className="text-blue-600">Ease</span>
                </h1>
                <p className="text-lg text-gray-600">
                    Find products, locate lines, and get directions instantly with MarketWay AI.
                </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6 w-full max-w-4xl">
                <button
                    onClick={() => navigate('/chat')}
                    className="group relative overflow-hidden bg-white p-8 rounded-3xl shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 text-left"
                >
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <MessageSquare size={120} className="text-blue-600" />
                    </div>
                    <div className="relative z-10">
                        <div className="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <MessageSquare size={28} className="text-blue-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">Ask MarketWay</h2>
                        <p className="text-gray-600">Chat with our AI assistant to find anything you need in the market.</p>
                    </div>
                </button>

                <button
                    onClick={() => navigate('/search')}
                    className="group relative overflow-hidden bg-white p-8 rounded-3xl shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 text-left"
                >
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Search size={120} className="text-emerald-600" />
                    </div>
                    <div className="relative z-10">
                        <div className="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <Search size={28} className="text-emerald-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">Search Products</h2>
                        <p className="text-gray-600">Quickly find specific items and see which lines sell them.</p>
                    </div>
                </button>
            </div>

            <div className="mt-16 flex items-center gap-2 text-gray-400 text-sm">
                <MapPin size={16} />
                <span>MarketWay Navigator • Phase 1 Beta</span>
            </div>
        </div>
    );
}
