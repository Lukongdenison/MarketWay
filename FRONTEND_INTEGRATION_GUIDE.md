# Frontend Integration Guide - MarketWay Navigator API

This guide provides practical examples for integrating the MarketWay Navigator API into your frontend application.

---

## Table of Contents

1. [Setup](#setup)
2. [API Client Setup](#api-client-setup)
3. [React Integration](#react-integration)
4. [Vue.js Integration](#vuejs-integration)
5. [Vanilla JavaScript](#vanilla-javascript)
6. [Common UI Patterns](#common-ui-patterns)
7. [Error Handling](#error-handling)
8. [Performance Tips](#performance-tips)

---

## Setup

### Environment Variables

Create a `.env` file in your frontend project:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
# or for production
VITE_API_BASE_URL=https://your-api-domain.com
```

For Create React App:
```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
```

---

## API Client Setup

### Option 1: Axios Client

```typescript
// src/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Option 2: Fetch Wrapper

```typescript
// src/api/client.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async upload<T>(endpoint: string, formData: FormData): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      // Don't set Content-Type for FormData - browser sets it automatically
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return await response.json();
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

---

## React Integration

### API Service Layer

```typescript
// src/services/marketApi.ts
import apiClient from '../api/client';

export interface AskResponse {
  answer: string;
  source: 'local' | 'online' | 'combined';
  images: string[];
}

export interface Line {
  line_name: string;
  items_sold: string[];
  layout: {
    column: 'left' | 'right';
    order: number;
  };
}

export interface LineInfo extends Line {
  image_url: string | null;
}

export interface ProductSearchResponse {
  query: string;
  results: Line[];
}

export interface NavigateResponse {
  line_name: string;
  directions: string;
  layout: {
    column: 'left' | 'right';
    order: number;
  };
}

export const marketApi = {
  // Ask a question
  async ask(question: string): Promise<AskResponse> {
    const { data } = await apiClient.post('/ask', { question });
    return data;
  },

  // Search for products
  async searchProducts(query: string): Promise<ProductSearchResponse> {
    const { data } = await apiClient.get(`/product/search?q=${encodeURIComponent(query)}`);
    return data;
  },

  // Get line information
  async getLineInfo(lineName: string): Promise<LineInfo> {
    const { data } = await apiClient.get(`/line/info/${encodeURIComponent(lineName)}`);
    return data;
  },

  // Get market history
  async getHistory(): Promise<{ history: string }> {
    const { data } = await apiClient.get('/history');
    return data;
  },

  // Get navigation directions
  async navigate(lineName: string): Promise<NavigateResponse> {
    const { data } = await apiClient.get(`/navigate?line_name=${encodeURIComponent(lineName)}`);
    return data;
  },

  // Voice query
  async voiceQuery(audioFile: File): Promise<Blob> {
    const formData = new FormData();
    formData.append('file', audioFile);
    
    const response = await fetch(`${apiClient.defaults.baseURL}/voice/query`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Voice query failed');
    }

    return await response.blob();
  },

  // Image identification
  async identifyImage(imageFile: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    const { data } = await apiClient.post('/image/identify', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },
};
```

### Custom React Hooks

```typescript
// src/hooks/useMarketApi.ts
import { useState, useCallback } from 'react';
import { marketApi, AskResponse, ProductSearchResponse, LineInfo } from '../services/marketApi';

// Hook for asking questions
export function useAsk() {
  const [data, setData] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = useCallback(async (question: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = await marketApi.ask(question);
      setData(result);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to get answer';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, ask };
}

// Hook for product search with debouncing
export function useProductSearch(debounceMs = 300) {
  const [data, setData] = useState<ProductSearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(
    debounce(async (query: string) => {
      if (!query.trim()) {
        setData(null);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const result = await marketApi.searchProducts(query);
        setData(result);
        return result;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Search failed';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    }, debounceMs),
    [debounceMs]
  );

  return { data, loading, error, search };
}

// Hook for line information
export function useLineInfo(lineName: string | null) {
  const [data, setData] = useState<LineInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLineInfo = useCallback(async () => {
    if (!lineName) return;

    setLoading(true);
    setError(null);
    try {
      const result = await marketApi.getLineInfo(lineName);
      setData(result);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load line info';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [lineName]);

  useEffect(() => {
    fetchLineInfo();
  }, [fetchLineInfo]);

  return { data, loading, error, refetch: fetchLineInfo };
}

// Debounce utility
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
```

### React Components

#### Search Component

```typescript
// src/components/ProductSearch.tsx
import React, { useState } from 'react';
import { useProductSearch } from '../hooks/useMarketApi';

export function ProductSearch() {
  const [query, setQuery] = useState('');
  const { data, loading, error, search } = useProductSearch();

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    search(value);
  };

  return (
    <div className="product-search">
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder="Search for products..."
        className="search-input"
      />

      {loading && <div className="loading">Searching...</div>}
      
      {error && <div className="error">{error}</div>}

      {data && data.results.length > 0 && (
        <div className="results">
          <h3>Found in {data.results.length} lines:</h3>
          {data.results.map((line) => (
            <div key={line.line_name} className="line-card">
              <h4>{line.line_name}</h4>
              <p>Column: {line.layout.column} | Position: {line.layout.order}</p>
              <div className="items">
                {line.items_sold.map((item) => (
                  <span key={item} className="item-tag">{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {data && data.results.length === 0 && (
        <div className="no-results">No results found for "{query}"</div>
      )}
    </div>
  );
}
```

#### Chat/Ask Component

```typescript
// src/components/MarketChat.tsx
import React, { useState } from 'react';
import { useAsk } from '../hooks/useMarketApi';

export function MarketChat() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Array<{
    type: 'user' | 'bot';
    text: string;
    images?: string[];
  }>>([]);
  const { loading, ask } = useAsk();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    // Add user message
    setMessages(prev => [...prev, { type: 'user', text: question }]);
    const currentQuestion = question;
    setQuestion('');

    try {
      const response = await ask(currentQuestion);
      
      // Add bot response
      setMessages(prev => [...prev, {
        type: 'bot',
        text: response.answer,
        images: response.images,
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
      }]);
    }
  };

  return (
    <div className="market-chat">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <p>{msg.text}</p>
            {msg.images && msg.images.length > 0 && (
              <div className="images">
                {msg.images.map((img, i) => (
                  <img
                    key={i}
                    src={`${import.meta.env.VITE_API_BASE_URL}${img}`}
                    alt="Market line"
                    className="line-image"
                  />
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message bot loading">Thinking...</div>}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about the market..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
```

#### Line Details Component

```typescript
// src/components/LineDetails.tsx
import React from 'react';
import { useLineInfo } from '../hooks/useMarketApi';

interface LineDetailsProps {
  lineName: string;
}

export function LineDetails({ lineName }: LineDetailsProps) {
  const { data, loading, error } = useLineInfo(lineName);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return null;

  return (
    <div className="line-details">
      <h2>{data.line_name}</h2>
      
      {data.image_url && (
        <img
          src={`${import.meta.env.VITE_API_BASE_URL}${data.image_url}`}
          alt={data.line_name}
          className="line-image"
        />
      )}

      <div className="location">
        <strong>Location:</strong> {data.layout.column} column, position {data.layout.order}
      </div>

      <div className="items">
        <strong>Items Sold:</strong>
        <ul>
          {data.items_sold.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## Vue.js Integration

### Composables (Vue 3)

```typescript
// src/composables/useMarketApi.ts
import { ref, Ref } from 'vue';
import { marketApi, AskResponse, ProductSearchResponse } from '../services/marketApi';

export function useAsk() {
  const data: Ref<AskResponse | null> = ref(null);
  const loading = ref(false);
  const error: Ref<string | null> = ref(null);

  const ask = async (question: string) => {
    loading.value = true;
    error.value = null;
    try {
      const result = await marketApi.ask(question);
      data.value = result;
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to get answer';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return { data, loading, error, ask };
}

export function useProductSearch() {
  const data: Ref<ProductSearchResponse | null> = ref(null);
  const loading = ref(false);
  const error: Ref<string | null> = ref(null);

  const search = async (query: string) => {
    if (!query.trim()) {
      data.value = null;
      return;
    }

    loading.value = true;
    error.value = null;
    try {
      const result = await marketApi.searchProducts(query);
      data.value = result;
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Search failed';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return { data, loading, error, search };
}
```

### Vue Component

```vue
<!-- src/components/ProductSearch.vue -->
<template>
  <div class="product-search">
    <input
      v-model="query"
      @input="handleSearch"
      type="text"
      placeholder="Search for products..."
      class="search-input"
    />

    <div v-if="loading" class="loading">Searching...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="data && data.results.length > 0" class="results">
      <h3>Found in {{ data.results.length }} lines:</h3>
      <div
        v-for="line in data.results"
        :key="line.line_name"
        class="line-card"
      >
        <h4>{{ line.line_name }}</h4>
        <p>Column: {{ line.layout.column }} | Position: {{ line.layout.order }}</p>
        <div class="items">
          <span
            v-for="item in line.items_sold"
            :key="item"
            class="item-tag"
          >
            {{ item }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="data && data.results.length === 0" class="no-results">
      No results found for "{{ query }}"
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useProductSearch } from '../composables/useMarketApi';
import { debounce } from 'lodash-es';

const query = ref('');
const { data, loading, error, search } = useProductSearch();

const handleSearch = debounce(() => {
  search(query.value);
}, 300);
</script>
```

---

## Vanilla JavaScript

```javascript
// src/api.js
const API_BASE_URL = 'http://127.0.0.1:8000';

class MarketAPI {
  async ask(question) {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    
    if (!response.ok) throw new Error('Failed to get answer');
    return await response.json();
  }

  async searchProducts(query) {
    const response = await fetch(
      `${API_BASE_URL}/product/search?q=${encodeURIComponent(query)}`
    );
    
    if (!response.ok) throw new Error('Search failed');
    return await response.json();
  }

  async getLineInfo(lineName) {
    const response = await fetch(
      `${API_BASE_URL}/line/info/${encodeURIComponent(lineName)}`
    );
    
    if (!response.ok) throw new Error('Line not found');
    return await response.json();
  }
}

const api = new MarketAPI();

// Usage
document.getElementById('searchBtn').addEventListener('click', async () => {
  const query = document.getElementById('searchInput').value;
  const results = await api.searchProducts(query);
  displayResults(results);
});

function displayResults(data) {
  const container = document.getElementById('results');
  container.innerHTML = '';
  
  data.results.forEach(line => {
    const card = document.createElement('div');
    card.className = 'line-card';
    card.innerHTML = `
      <h3>${line.line_name}</h3>
      <p>Location: ${line.layout.column} column, position ${line.layout.order}</p>
      <div class="items">
        ${line.items_sold.map(item => `<span class="tag">${item}</span>`).join('')}
      </div>
    `;
    container.appendChild(card);
  });
}
```

---

## Common UI Patterns

### Loading States

```typescript
function LoadingSpinner() {
  return (
    <div className="spinner">
      <div className="spinner-circle"></div>
      <p>Loading...</p>
    </div>
  );
}

// CSS
.spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-circle {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

### Empty States

```typescript
function EmptyState({ message }: { message: string }) {
  return (
    <div className="empty-state">
      <svg>...</svg>
      <h3>No Results</h3>
      <p>{message}</p>
    </div>
  );
}
```

### Error Display

```typescript
function ErrorMessage({ error, onRetry }: { error: string; onRetry?: () => void }) {
  return (
    <div className="error-message">
      <span className="error-icon">⚠️</span>
      <p>{error}</p>
      {onRetry && <button onClick={onRetry}>Try Again</button>}
    </div>
  );
}
```

---

## Error Handling

### Global Error Handler

```typescript
// src/utils/errorHandler.ts
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function handleApiError(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message;
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unexpected error occurred';
}

// Usage in components
try {
  await marketApi.ask(question);
} catch (error) {
  const message = handleApiError(error);
  setError(message);
  // Optionally log to error tracking service
  console.error('API Error:', error);
}
```

---

## Performance Tips

### 1. Debounce Search Inputs

```typescript
import { debounce } from 'lodash-es';

const debouncedSearch = debounce((query: string) => {
  marketApi.searchProducts(query);
}, 300);
```

### 2. Cache API Responses

```typescript
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

async function cachedRequest<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const cached = cache.get(key);
  
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  
  const data = await fetcher();
  cache.set(key, { data, timestamp: Date.now() });
  return data;
}

// Usage
const history = await cachedRequest('history', () => marketApi.getHistory());
```

### 3. Lazy Load Images

```typescript
<img
  src={`${API_BASE_URL}${imageUrl}`}
  loading="lazy"
  alt="Market line"
/>
```

### 4. Use React Query (Optional)

```typescript
import { useQuery } from '@tanstack/react-query';

function useLineInfo(lineName: string) {
  return useQuery({
    queryKey: ['line', lineName],
    queryFn: () => marketApi.getLineInfo(lineName),
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: !!lineName,
  });
}
```

---

## Summary

This guide provides everything you need to integrate the MarketWay Navigator API into your frontend application. Choose the patterns that best fit your tech stack and project requirements.

**Key Takeaways:**
- Use environment variables for API URLs
- Implement proper error handling
- Add loading states for better UX
- Debounce search inputs
- Cache responses when appropriate
- Handle file uploads correctly for voice/image endpoints

For more details, see:
- [Full API Documentation](./API_DOCUMENTATION.md)
- [Quick Reference](./API_QUICK_REFERENCE.md)
- [Postman Collection](./MarketWay_API.postman_collection.json)
