import React from 'react';
import { ArrowLeft, ShoppingBag } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';

export function Header() {
    const navigate = useNavigate();
    const location = useLocation();
    const isHome = location.pathname === '/';

    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 h-16">
            <div className="max-w-3xl mx-auto h-full px-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    {!isHome && (
                        <button
                            onClick={() => navigate(-1)}
                            className="p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
                        >
                            <ArrowLeft size={20} />
                        </button>
                    )}
                    <div className="flex items-center gap-2" onClick={() => navigate('/')} role="button">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center shadow-md">
                            <ShoppingBag size={18} className="text-white" />
                        </div>
                        <h1 className="font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
                            MarketWay
                        </h1>
                    </div>
                </div>
            </div>
        </header>
    );
}
