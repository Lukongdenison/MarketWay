import { useState, useCallback } from 'react';
import type { AskResponse, ProductSearchResponse } from '../services/marketApi';
import { marketApi } from '../services/marketApi';

export function useMarketApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const askMarket = useCallback(async (question: string): Promise<AskResponse> => {
        setLoading(true);
        setError(null);
        try {
            const result = await marketApi.askMarket(question);
            return result;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to get answer';
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const searchProducts = useCallback(async (query: string): Promise<ProductSearchResponse> => {
        setLoading(true);
        setError(null);
        try {
            const result = await marketApi.searchProducts(query);
            return result;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Search failed';
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return { loading, error, askMarket, searchProducts };
}
