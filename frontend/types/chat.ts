export interface Message {
    id: string;
    sender: 'user' | 'bot';
    text: string;
    image_url?: string;
}
export interface ItemSearchResponse {
    query: string;
    direction: string;
    name: string;
}

export interface InfoSearchResponse {
    info: string;
}

export type ChatResponse = ItemSearchResponse | InfoSearchResponse;


