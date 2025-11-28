# MarketWay Navigator API - Quick Reference

## Base URL
```
http://127.0.0.1:8000
```

## Quick Links
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **Full Documentation:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## Endpoints at a Glance

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/ask` | Ask questions about market | No |
| GET | `/product/search?q={query}` | Search for products | No |
| GET | `/line/info/{line_name}` | Get line details | No |
| GET | `/history` | Get market history | No |
| POST | `/voice/query` | Voice query (audio in/out) | No |
| POST | `/image/identify` | Identify product from image | No |
| GET | `/navigate?line_name={name}` | Get directions to line | No |

---

## Quick Examples

### 1. Ask a Question
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Where can I buy shoes?"}'
```

```javascript
fetch('http://127.0.0.1:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'Where can I buy shoes?' })
})
.then(res => res.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "answer": "Found 'shoes' in the following lines: Blessed Line, Victory Line, Wisdom Line, Godly Line.",
  "source": "local",
  "images": ["/images/Blessed Lines.jpg", "/images/Victory line.jpg"]
}
```

---

### 2. Search Products
```bash
curl "http://127.0.0.1:8000/product/search?q=clothes"
```

```javascript
fetch('http://127.0.0.1:8000/product/search?q=clothes')
  .then(res => res.json())
  .then(data => console.log(data.results));
```

**Response:**
```json
{
  "query": "clothes",
  "results": [
    {
      "line_name": "Best Line",
      "items_sold": ["pharmacies", "clothes", "wine", "bodystuff"],
      "layout": { "column": "left", "order": 5 }
    }
  ]
}
```

---

### 3. Get Line Information
```bash
curl "http://127.0.0.1:8000/line/info/Victory%20Line"
```

```javascript
fetch('http://127.0.0.1:8000/line/info/Victory Line')
  .then(res => res.json())
  .then(data => console.log(data));
```

**Response:**
```json
{
  "line_name": "Victory Line",
  "items_sold": ["beads", "jewelries", "clothes", "babystuff", "shoes"],
  "layout": { "column": "right", "order": 5 },
  "image_url": "/images/Victory line.jpg"
}
```

---

### 4. Get Navigation Directions
```bash
curl "http://127.0.0.1:8000/navigate?line_name=Victory%20Line"
```

```javascript
fetch('http://127.0.0.1:8000/navigate?line_name=Victory Line')
  .then(res => res.json())
  .then(data => console.log(data.directions));
```

**Response:**
```json
{
  "line_name": "Victory Line",
  "directions": "Go to the RIGHT column, it's the 5th line on that side.",
  "layout": { "column": "right", "order": 5 }
}
```

---

### 5. Get Market History
```bash
curl "http://127.0.0.1:8000/history"
```

```javascript
fetch('http://127.0.0.1:8000/history')
  .then(res => res.json())
  .then(data => console.log(data.history));
```

---

### 6. Voice Query (File Upload)
```javascript
// Record audio or get audio file
const formData = new FormData();
formData.append('file', audioBlob, 'query.wav');

fetch('http://127.0.0.1:8000/voice/query', {
  method: 'POST',
  body: formData
})
.then(res => res.blob())
.then(blob => {
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();
});
```

---

### 7. Image Identification (File Upload)
```javascript
// Get image from file input
const formData = new FormData();
formData.append('file', imageFile);

fetch('http://127.0.0.1:8000/image/identify', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Common Response Patterns

### Success Response (JSON)
```json
{
  "field1": "value",
  "field2": ["array", "values"]
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

### Status Codes
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (line doesn't exist)
- `422` - Validation Error
- `500` - Server Error

---

## Available Market Lines

### Left Column
1. Mothers Line - medicine, babystuff, cookedfood
2. Family Line - drinks, fowlfeed, toothpaste, ropesandbags, sleepers
3. Magazine Line - pharmacies, bodylotion, drinks(egwine)
4. Onitsha Line - cosmetics, wine, fewpharmacies
5. Best Line - pharmacies, clothes, wine, bodystuff

### Right Column
1. Fish Line - dryfish
2. Obama Line - medicine, kitchenutensils, wigs
3. Peaceful Line - babystuff, pharmacy, wine
4. Blessed Line - shoes, boxes, buckets, kitchenutensils
5. Victory Line - beads, jewelries, clothes, babystuff, shoes, wigs, baggyjeans, bodylotion, schoolequipment
6. Universal Line - clothes, sleepers, bags, kitchenutensils, hair, wigs
7. Fashion Line - clothes, sportwears, bodystuff, mesh, rainboots
8. Wisdom Line - clothes, bags, shoes, sleepers, kitchenutensils
9. Godly Line - shoes, dresses, roomdecoitems, bags, babystuff
10. Rapa Line - (no items listed)

---

## TypeScript Types

```typescript
// Request Types
interface AskRequest {
  question: string;
}

// Response Types
interface AskResponse {
  answer: string;
  source: 'local' | 'online' | 'combined';
  images: string[];
}

interface ProductSearchResponse {
  query: string;
  results: Line[];
}

interface Line {
  line_name: string;
  items_sold: string[];
  layout: {
    column: 'left' | 'right';
    order: number;
  };
}

interface LineInfoResponse extends Line {
  image_url: string | null;
}

interface NavigateResponse {
  line_name: string;
  directions: string;
  layout: {
    column: 'left' | 'right';
    order: number;
  };
}

interface HistoryResponse {
  history: string;
}
```

---

## React Hooks Example

```typescript
import { useState } from 'react';

const API_BASE = 'http://127.0.0.1:8000';

// Hook for asking questions
export function useAsk() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = async (question: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      if (!res.ok) throw new Error('Failed to get answer');
      return await res.json();
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { ask, loading, error };
}

// Hook for product search
export function useProductSearch() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(
        `${API_BASE}/product/search?q=${encodeURIComponent(query)}`
      );
      if (!res.ok) throw new Error('Search failed');
      return await res.json();
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { search, loading, error };
}

// Usage in component
function SearchComponent() {
  const { search, loading } = useProductSearch();
  const [results, setResults] = useState([]);

  const handleSearch = async (query: string) => {
    const data = await search(query);
    setResults(data.results);
  };

  return (
    <div>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {loading && <p>Loading...</p>}
      {results.map(line => <div key={line.line_name}>{line.line_name}</div>)}
    </div>
  );
}
```

---

## Testing Tips

### 1. Use the Interactive Docs
Visit http://127.0.0.1:8000/docs to test endpoints directly in your browser.

### 2. Test with cURL
Quick command-line testing:
```bash
# Test if API is running
curl http://127.0.0.1:8000/history

# Test product search
curl "http://127.0.0.1:8000/product/search?q=shoes"
```

### 3. Use Postman/Insomnia
Import the provided Postman collection for easy testing.

### 4. Browser DevTools
Use the Network tab to inspect requests and responses.

---

## Common Pitfalls

### ❌ Don't forget to encode URLs
```javascript
// Wrong
fetch(`/line/info/Victory Line`)

// Correct
fetch(`/line/info/${encodeURIComponent('Victory Line')}`)
```

### ❌ Don't forget Content-Type header for JSON
```javascript
// Wrong
fetch('/ask', {
  method: 'POST',
  body: JSON.stringify({ question: 'test' })
})

// Correct
fetch('/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'test' })
})
```

### ❌ Don't use FormData for JSON endpoints
```javascript
// Wrong (for /ask endpoint)
const formData = new FormData();
formData.append('question', 'test');

// Correct
const body = JSON.stringify({ question: 'test' });
```

### ✅ Do use FormData for file uploads
```javascript
// Correct (for /voice/query and /image/identify)
const formData = new FormData();
formData.append('file', fileBlob, 'filename.wav');
```

---

## Need More Help?

- **Full Documentation:** See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Interactive Testing:** http://127.0.0.1:8000/docs
- **Backend README:** [backend/README.md](./backend/README.md)
