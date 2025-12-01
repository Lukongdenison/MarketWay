import apiClient from '../api/client';

export interface AskResponse {
    answer: string;
    source: 'local' | 'online' | 'combined';
    images: string[];
}

export interface ProductSearchResponse {
    query: string;
    results: any[];
}

export const marketApi = {
    async askMarket(question: string): Promise<AskResponse> {
        const { data } = await apiClient.post('/ask', { question });
        return data;
    },

    async searchProducts(query: string): Promise<ProductSearchResponse> {
        const { data } = await apiClient.get(`/product/search?q=${encodeURIComponent(query)}`);
        return data;
    },
};
