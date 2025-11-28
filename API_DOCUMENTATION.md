# MarketWay Navigator API Documentation

**Version:** 1.0.0  
**Base URL:** `http://127.0.0.1:8000` (local) or your deployed URL

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL & Headers](#base-url--headers)
4. [Endpoints](#endpoints)
   - [POST /ask](#post-ask)
   - [GET /product/search](#get-productsearch)
   - [GET /line/info/{line_name}](#get-lineinfolinename)
   - [GET /history](#get-history)
   - [POST /voice/query](#post-voicequery)
   - [POST /image/identify](#post-imageidentify)
   - [GET /navigate](#get-navigate)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Code Examples](#code-examples)

---

## Overview

The MarketWay Navigator API provides endpoints for:
- **Intelligent Q&A**: Ask questions about the market, products, and history
- **Product Search**: Find which market lines sell specific products
- **Line Information**: Get detailed information about specific market lines
- **Voice Interaction**: Speech-to-text and text-to-speech capabilities
- **Image Recognition**: Identify products from images
- **Navigation**: Get directions to specific market lines
- **Market History**: Access historical information about Bamenda Main Market

---

## Authentication

Currently, the API does not require authentication for most endpoints. However, ensure you have the proper CORS configuration if calling from a web browser.

---

## Base URL & Headers

### Base URL
```
http://127.0.0.1:8000
```

### Recommended Headers
```http
Content-Type: application/json
Accept: application/json
```

For file uploads (voice/image endpoints):
```http
Content-Type: multipart/form-data
```

---

## Endpoints

### POST /ask

Ask general questions about the market, products, or history. The API intelligently searches local data first, then falls back to online search if needed.

#### Request

**URL:** `/ask`  
**Method:** `POST`  
**Content-Type:** `application/json`

**Body:**
```json
{
  "question": "Where can I find medicine?"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | The question to ask about the market |

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "answer": "Found 'medicine' in the following lines: Mothers Line, Obama Line, Peaceful Line.",
  "source": "local",
  "images": [
    "/images/Mothers Line.jpg",
    "/images/Obama Line.jpg",
    "/images/Peaceful Line.jpg"
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | The answer to the question |
| `source` | string | Data source: `"local"`, `"online"`, or `"combined"` |
| `images` | array | Array of image URLs related to the answer |

#### Example Use Cases

```javascript
// Find products
{
  "question": "Where can I buy shoes?"
}

// Market history
{
  "question": "When was the market built?"
}

// General queries
{
  "question": "What can I find in Victory Line?"
}
```

---

### GET /product/search

Search for products and find which market lines sell them.

#### Request

**URL:** `/product/search`  
**Method:** `GET`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Product name to search for |

**Example:**
```
GET /product/search?q=shoes
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "query": "shoes",
  "results": [
    {
      "line_name": "Blessed Line",
      "items_sold": ["shoes", "boxes", "buckets", "kitchenutensils"],
      "layout": {
        "column": "right",
        "order": 4
      }
    },
    {
      "line_name": "Victory Line",
      "items_sold": ["beads", "jewelries", "clothes", "babystuff", "shoes", "wigs", "baggyjeans", "bodylotion", "schoolequipment"],
      "layout": {
        "column": "right",
        "order": 5
      }
    },
    {
      "line_name": "Wisdom Line",
      "items_sold": ["clothes", "bags", "shoes", "sleepers", "kitchenutensils"],
      "layout": {
        "column": "right",
        "order": 8
      }
    },
    {
      "line_name": "Godly Line",
      "items_sold": ["shoes", "dresses", "roomdecoitems", "bags", "babystuff"],
      "layout": {
        "column": "right",
        "order": 9
      }
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | The search query that was executed |
| `results` | array | Array of line objects that sell the searched product |
| `results[].line_name` | string | Name of the market line |
| `results[].items_sold` | array | List of items sold in this line |
| `results[].layout` | object | Layout information for the line |
| `results[].layout.column` | string | Column position: `"left"` or `"right"` |
| `results[].layout.order` | number | Order/position within the column |

---

### GET /line/info/{line_name}

Get detailed information about a specific market line.

#### Request

**URL:** `/line/info/{line_name}`  
**Method:** `GET`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `line_name` | string | Yes | Name of the market line (case-insensitive) |

**Example:**
```
GET /line/info/Victory Line
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "line_name": "Victory Line",
  "items_sold": [
    "beads",
    "jewelries",
    "clothes",
    "babystuff",
    "shoes",
    "wigs",
    "baggyjeans",
    "bodylotion",
    "schoolequipment"
  ],
  "layout": {
    "column": "right",
    "order": 5
  },
  "image_url": "/images/Victory line.jpg"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `line_name` | string | Name of the market line |
| `items_sold` | array | List of items sold in this line |
| `layout` | object | Layout information |
| `layout.column` | string | Column position: `"left"` or `"right"` |
| `layout.order` | number | Order/position within the column |
| `image_url` | string \| null | URL to the line's image, or null if not available |

#### Error Response

**Status:** `404 Not Found`

```json
{
  "detail": "Line not found"
}
```

---

### GET /history

Get historical information about Bamenda Main Market.

#### Request

**URL:** `/history`  
**Method:** `GET`

**Example:**
```
GET /history
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "history": "Bamenda Main Market, also known as Bamenda Central Market, is one of the largest and most vibrant markets in the North West Region of Cameroon..."
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `history` | string | Full historical text about the market (extracted from PDF) |

---

### POST /voice/query

Submit a voice query and receive an audio response.

#### Request

**URL:** `/voice/query`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`

**Form Data:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Audio file (WAV, MP3, etc.) containing the voice query |

**Example (using FormData):**
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'query.wav');

fetch('/voice/query', {
  method: 'POST',
  body: formData
});
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `audio/mpeg`

Returns an MP3 audio file containing the spoken response.

#### Process Flow

1. **Speech-to-Text**: Your audio is converted to text
2. **Query Processing**: The text is processed like a regular search
3. **Text-to-Speech**: The response is converted back to audio
4. **Audio Response**: MP3 file is returned

#### Error Response

**Status:** `400 Bad Request`

```json
{
  "detail": "Could not understand audio"
}
```

---

### POST /image/identify

Identify products from an uploaded image.

#### Request

**URL:** `/image/identify`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`

**Form Data:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Image file (JPG, PNG, etc.) containing the product |

**Example (using FormData):**
```javascript
const formData = new FormData();
formData.append('file', imageFile, 'product.jpg');

fetch('/image/identify', {
  method: 'POST',
  body: formData
});
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "identified_product": "shoes",
  "confidence": 0.85,
  "matching_lines": [
    {
      "line_name": "Blessed Line",
      "items_sold": ["shoes", "boxes", "buckets", "kitchenutensils"]
    },
    {
      "line_name": "Victory Line",
      "items_sold": ["beads", "jewelries", "clothes", "babystuff", "shoes", "wigs", "baggyjeans", "bodylotion", "schoolequipment"]
    }
  ]
}
```

> **Note:** The exact response structure depends on the image service implementation. Check with your backend team for the specific fields returned.

---

### GET /navigate

Get directions to a specific market line.

#### Request

**URL:** `/navigate`  
**Method:** `GET`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `line_name` | string | Yes | Target line name to navigate to |

**Example:**
```
GET /navigate?line_name=Victory Line
```

#### Response

**Status:** `200 OK`  
**Content-Type:** `application/json`

```json
{
  "line_name": "Victory Line",
  "directions": "Go to the RIGHT column, it's the 5th line on that side.",
  "layout": {
    "column": "right",
    "order": 5
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `line_name` | string | Name of the target line |
| `directions` | string | Human-readable directions to the line |
| `layout` | object | Layout information |
| `layout.column` | string | Column position: `"left"` or `"right"` |
| `layout.order` | number | Order/position within the column |

#### Error Response

**Status:** `404 Not Found`

```json
{
  "detail": "Line not found"
}
```

---

## Data Models

### Line Object

```typescript
interface Line {
  line_name: string;
  items_sold: string[];
  layout: {
    column: "left" | "right";
    order: number;
  };
}
```

### Layout Object

```typescript
interface Layout {
  column: "left" | "right";  // Which column of the market
  order: number;              // Position within that column (1-based)
}
```

### Available Market Lines

The market has the following lines:

**Left Column:**
1. Mothers Line
2. Family Line
3. Magazine Line
4. Onitsha Line
5. Best Line

**Right Column:**
1. Fish Line
2. Obama Line
3. Peaceful Line
4. Blessed Line
5. Victory Line
6. Universal Line
7. Fashion Line
8. Wisdom Line
9. Godly Line
10. Rapa Line

---

## Error Handling

### Standard Error Response

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid input, missing required fields |
| `404` | Not Found | Line not found, resource doesn't exist |
| `422` | Unprocessable Entity | Validation error (check request format) |
| `500` | Internal Server Error | Server-side error |

### Error Handling Best Practices

```javascript
try {
  const response = await fetch('/product/search?q=shoes');
  
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
    // Handle error appropriately
    return;
  }
  
  const data = await response.json();
  // Process successful response
} catch (error) {
  console.error('Network Error:', error);
  // Handle network errors
}
```

---

## Code Examples

### JavaScript/TypeScript (Fetch API)

#### Basic Question

```javascript
async function askQuestion(question) {
  const response = await fetch('http://127.0.0.1:8000/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question })
  });
  
  const data = await response.json();
  console.log('Answer:', data.answer);
  console.log('Images:', data.images);
  return data;
}

// Usage
askQuestion('Where can I buy clothes?');
```

#### Product Search

```javascript
async function searchProduct(productName) {
  const response = await fetch(
    `http://127.0.0.1:8000/product/search?q=${encodeURIComponent(productName)}`
  );
  
  const data = await response.json();
  console.log(`Found ${data.results.length} lines selling ${productName}`);
  return data.results;
}

// Usage
searchProduct('shoes');
```

#### Get Line Information

```javascript
async function getLineInfo(lineName) {
  const response = await fetch(
    `http://127.0.0.1:8000/line/info/${encodeURIComponent(lineName)}`
  );
  
  if (!response.ok) {
    throw new Error('Line not found');
  }
  
  const data = await response.json();
  return data;
}

// Usage
getLineInfo('Victory Line');
```

#### Voice Query

```javascript
async function sendVoiceQuery(audioBlob) {
  const formData = new FormData();
  formData.append('file', audioBlob, 'query.wav');
  
  const response = await fetch('http://127.0.0.1:8000/voice/query', {
    method: 'POST',
    body: formData
  });
  
  // Response is an audio file
  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  
  // Play the audio
  const audio = new Audio(audioUrl);
  audio.play();
  
  return audioUrl;
}
```

#### Image Identification

```javascript
async function identifyProduct(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://127.0.0.1:8000/image/identify', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data;
}

// Usage with file input
document.getElementById('imageInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const result = await identifyProduct(file);
  console.log('Identified:', result);
});
```

#### Navigation

```javascript
async function getDirections(lineName) {
  const response = await fetch(
    `http://127.0.0.1:8000/navigate?line_name=${encodeURIComponent(lineName)}`
  );
  
  if (!response.ok) {
    throw new Error('Line not found');
  }
  
  const data = await response.json();
  console.log('Directions:', data.directions);
  return data;
}

// Usage
getDirections('Victory Line');
```

### React Example

```typescript
import { useState } from 'react';

interface AskResponse {
  answer: string;
  source: string;
  images: string[];
}

function MarketSearch() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about the market..."
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      
      {response && (
        <div>
          <p>{response.answer}</p>
          <div>
            {response.images.map((img, i) => (
              <img key={i} src={img} alt="Market line" />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

### Axios Example

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Ask a question
async function askQuestion(question) {
  const { data } = await api.post('/ask', { question });
  return data;
}

// Search products
async function searchProduct(query) {
  const { data } = await api.get('/product/search', {
    params: { q: query }
  });
  return data;
}

// Get line info
async function getLineInfo(lineName) {
  const { data } = await api.get(`/line/info/${lineName}`);
  return data;
}

// Navigate
async function navigate(lineName) {
  const { data } = await api.get('/navigate', {
    params: { line_name: lineName }
  });
  return data;
}
```

---

## Interactive API Documentation

For interactive testing and exploration, visit the auto-generated Swagger UI documentation:

```
http://127.0.0.1:8000/docs
```

This provides:
- Interactive API testing
- Request/response examples
- Schema definitions
- Try-it-out functionality

---

## CORS Configuration

If you're calling the API from a web browser, ensure CORS is properly configured on the backend. The backend should include appropriate CORS headers:

```python
# Backend CORS configuration (already handled in main.py)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Rate Limiting

Currently, there are no rate limits on the API. However, be mindful of:
- External API usage (Tavily search has its own limits)
- File upload sizes for voice/image endpoints
- Server resources for voice/image processing

---

## Best Practices

### 1. **Error Handling**
Always implement proper error handling for network failures and API errors.

### 2. **Loading States**
Show loading indicators during API calls for better UX.

### 3. **Debouncing**
For search inputs, debounce user input to avoid excessive API calls.

```javascript
import { debounce } from 'lodash';

const debouncedSearch = debounce(async (query) => {
  const results = await searchProduct(query);
  // Update UI with results
}, 300);
```

### 4. **Caching**
Cache frequently accessed data (like market history or line information) to reduce API calls.

### 5. **Image URLs**
Image URLs are relative paths. Prepend the base URL when displaying:

```javascript
const imageUrl = `http://127.0.0.1:8000${data.image_url}`;
```

### 6. **URL Encoding**
Always encode URL parameters, especially line names with spaces:

```javascript
const lineName = encodeURIComponent('Victory Line');
fetch(`/line/info/${lineName}`);
```

---

## Support & Contact

For issues, questions, or feature requests:
- Check the interactive docs at `/docs`
- Review the backend README.md
- Contact the backend development team

---

**Last Updated:** 2025-11-28  
**API Version:** 1.0.0
