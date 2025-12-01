import React, { useState } from 'react';
import { Search, MapPin, ShoppingBag } from 'lucide-react';
import { useMarketApi } from '../hooks/useMarketApi';

export function ProductSearch() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<any[]>([]);
    const [hasSearched, setHasSearched] = useState(false);
    const { loading, error, searchProducts } = useMarketApi();

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setHasSearched(true);
        try {
            const response = await searchProducts(query);
            setResults(response.results);
        } catch (err) {
            setResults([]);
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-4 pt-8">
            <form onSubmit={handleSearch} className="relative mb-8">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Search className="text-gray-400" size={20} />
                </div>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search for products (e.g., Medicine, Shoes)..."
                    className="w-full pl-12 pr-4 py-4 bg-white border border-gray-200 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all text-lg"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="absolute right-2 top-2 bottom-2 px-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:bg-gray-300"
                >
                    {loading ? '...' : 'Search'}
                </button>
            </form>

            <div className="space-y-4">
                {error && (
                    <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-100">
                        {error}
                    </div>
                )}

                {hasSearched && !loading && results.length === 0 && !error && (
                    <div className="text-center py-12 text-gray-500">
                        <ShoppingBag size={48} className="mx-auto mb-4 opacity-20" />
                        <p>No products found matching "{query}"</p>
                    </div>
                )}

                {results.map((line, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex gap-4">
                            {line.image_url && (
                                <img
                                    src={`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}${line.image_url}`}
                                    alt={line.line_name}
                                    className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
                                />
                            )}
                            <div className="flex-1">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="font-semibold text-lg text-gray-900">{line.line_name}</h3>
                                        <div className="flex items-center gap-2 mt-1 text-gray-600">
                                            <MapPin size={16} className="text-blue-500" />
                                            <span className="font-medium">{line.layout.column} column</span>
                                            <span className="text-gray-300">•</span>
                                            <span className="text-sm">Position {line.layout.order}</span>
                                        </div>
                                    </div>
                                    <span className="bg-blue-50 text-blue-700 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                        In Stock
                                    </span>
                                </div>
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {line.items_sold.map((item: string, i: number) => (
                                        <span key={i} className={`text-xs px-2 py-1 rounded-md ${item.toLowerCase().includes(query.toLowerCase())
                                                ? 'bg-yellow-100 text-yellow-800 font-medium'
                                                : 'bg-gray-50 text-gray-600'
                                            }`}>
                                            {item}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
