# 📚 MarketWay Navigator - API Documentation Suite

Complete documentation package for frontend engineers working with the MarketWay Navigator API.

---

## 📖 Documentation Files

### 1. **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API Reference
   - **What it contains:** Full API documentation with all endpoints, request/response schemas, data models, and code examples
   - **When to use:** When you need detailed information about any endpoint, including all parameters, response fields, and error codes
   - **Best for:** Reference during development, understanding API capabilities

### 2. **[API_QUICK_REFERENCE.md](./API_QUICK_REFERENCE.md)** - Quick Start Guide
   - **What it contains:** Concise examples, TypeScript types, React hooks, and common patterns
   - **When to use:** When you need quick code snippets or want to get started fast
   - **Best for:** Copy-paste examples, quick lookups, troubleshooting common issues

### 3. **[FRONTEND_INTEGRATION_GUIDE.md](./FRONTEND_INTEGRATION_GUIDE.md)** - Integration Guide
   - **What it contains:** Practical integration examples for React, Vue.js, and vanilla JavaScript
   - **When to use:** When setting up your frontend project to consume the API
   - **Best for:** Project setup, implementing API clients, creating reusable hooks/composables

### 4. **[MarketWay_API.postman_collection.json](./MarketWay_API.postman_collection.json)** - Postman Collection
   - **What it contains:** Pre-configured API requests for all endpoints
   - **When to use:** For testing API endpoints without writing code
   - **Best for:** API exploration, manual testing, sharing with team members

---

## 🚀 Quick Start

### For Frontend Engineers

1. **First Time?** Start here:
   ```
   1. Read: API_QUICK_REFERENCE.md (5 min)
   2. Import: MarketWay_API.postman_collection.json into Postman
   3. Test: Try a few endpoints in Postman
   4. Integrate: Follow FRONTEND_INTEGRATION_GUIDE.md for your framework
   ```

2. **Need Details?** Check:
   ```
   API_DOCUMENTATION.md → Full endpoint specifications
   ```

3. **Building a Feature?** Use:
   ```
   FRONTEND_INTEGRATION_GUIDE.md → Copy component examples
   API_QUICK_REFERENCE.md → Get TypeScript types
   ```

---

## 🎯 Common Use Cases

### "I want to search for products"
```javascript
// Quick example from API_QUICK_REFERENCE.md
fetch('http://127.0.0.1:8000/product/search?q=shoes')
  .then(res => res.json())
  .then(data => console.log(data.results));
```
📄 **See:** API_QUICK_REFERENCE.md → Quick Examples → Search Products

### "I need to build a chat interface"
```typescript
// Full component example in FRONTEND_INTEGRATION_GUIDE.md
import { useAsk } from '../hooks/useMarketApi';
// ... complete component code
```
📄 **See:** FRONTEND_INTEGRATION_GUIDE.md → React Integration → Chat Component

### "What's the response format for /ask?"
```json
{
  "answer": "string",
  "source": "local" | "online" | "combined",
  "images": ["string"]
}
```
📄 **See:** API_DOCUMENTATION.md → POST /ask → Response

### "How do I handle file uploads?"
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'query.wav');
fetch('/voice/query', { method: 'POST', body: formData });
```
📄 **See:** API_QUICK_REFERENCE.md → Voice Query

---

## 📋 API Endpoints Overview

| Endpoint | Method | Purpose | Documentation |
|----------|--------|---------|---------------|
| `/ask` | POST | Ask questions about market | [Docs](./API_DOCUMENTATION.md#post-ask) |
| `/product/search` | GET | Search for products | [Docs](./API_DOCUMENTATION.md#get-productsearch) |
| `/line/info/{name}` | GET | Get line details | [Docs](./API_DOCUMENTATION.md#get-lineinfolinename) |
| `/history` | GET | Get market history | [Docs](./API_DOCUMENTATION.md#get-history) |
| `/voice/query` | POST | Voice interaction | [Docs](./API_DOCUMENTATION.md#post-voicequery) |
| `/image/identify` | POST | Image recognition | [Docs](./API_DOCUMENTATION.md#post-imageidentify) |
| `/navigate` | GET | Get directions | [Docs](./API_DOCUMENTATION.md#get-navigate) |

---

## 🛠️ Tools & Resources

### Interactive API Documentation
```
http://127.0.0.1:8000/docs
```
Auto-generated Swagger UI for testing endpoints directly in your browser.

### Postman Collection
Import `MarketWay_API.postman_collection.json` into Postman:
1. Open Postman
2. Click "Import"
3. Select the JSON file
4. Start testing!

### Base URL
```
Local: http://127.0.0.1:8000
Production: https://your-api-domain.com
```

---

## 💡 Tips for Success

### ✅ Do's
- ✅ Use the Postman collection to test endpoints before coding
- ✅ Implement error handling for all API calls
- ✅ Debounce search inputs to reduce API calls
- ✅ Cache responses for frequently accessed data (like history)
- ✅ Use TypeScript types from the documentation
- ✅ Encode URL parameters (especially line names with spaces)

### ❌ Don'ts
- ❌ Don't forget Content-Type headers for JSON requests
- ❌ Don't use FormData for JSON endpoints (only for file uploads)
- ❌ Don't make API calls on every keystroke (use debouncing)
- ❌ Don't hardcode the API URL (use environment variables)
- ❌ Don't ignore error responses

---

## 🏗️ Project Structure Example

```
your-frontend-project/
├── src/
│   ├── api/
│   │   └── client.ts          # API client setup
│   ├── services/
│   │   └── marketApi.ts       # API service layer
│   ├── hooks/                 # React hooks
│   │   └── useMarketApi.ts
│   ├── components/
│   │   ├── ProductSearch.tsx
│   │   ├── MarketChat.tsx
│   │   └── LineDetails.tsx
│   └── types/
│       └── api.ts             # TypeScript types
├── .env                       # Environment variables
└── package.json
```

📄 **See:** FRONTEND_INTEGRATION_GUIDE.md for complete setup instructions

---

## 🔍 Finding What You Need

### By Framework

**React Developers:**
- Setup: FRONTEND_INTEGRATION_GUIDE.md → React Integration
- Hooks: FRONTEND_INTEGRATION_GUIDE.md → Custom React Hooks
- Components: FRONTEND_INTEGRATION_GUIDE.md → React Components

**Vue.js Developers:**
- Setup: FRONTEND_INTEGRATION_GUIDE.md → Vue.js Integration
- Composables: FRONTEND_INTEGRATION_GUIDE.md → Composables

**Vanilla JS Developers:**
- Examples: FRONTEND_INTEGRATION_GUIDE.md → Vanilla JavaScript
- Quick snippets: API_QUICK_REFERENCE.md

### By Task

**Setting Up:**
1. FRONTEND_INTEGRATION_GUIDE.md → Setup
2. FRONTEND_INTEGRATION_GUIDE.md → API Client Setup

**Building Features:**
1. API_QUICK_REFERENCE.md → TypeScript Types
2. FRONTEND_INTEGRATION_GUIDE.md → Components
3. API_DOCUMENTATION.md → Endpoint Details

**Debugging:**
1. API_DOCUMENTATION.md → Error Handling
2. API_QUICK_REFERENCE.md → Common Pitfalls
3. Postman Collection → Test endpoints manually

---

## 📞 Support & Resources

### Documentation
- **Full API Docs:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Quick Reference:** [API_QUICK_REFERENCE.md](./API_QUICK_REFERENCE.md)
- **Integration Guide:** [FRONTEND_INTEGRATION_GUIDE.md](./FRONTEND_INTEGRATION_GUIDE.md)
- **Backend README:** [backend/README.md](./backend/README.md)

### Interactive Tools
- **Swagger UI:** http://127.0.0.1:8000/docs
- **Postman Collection:** MarketWay_API.postman_collection.json

### Getting Help
1. Check the documentation files above
2. Test with Postman collection
3. Review code examples in integration guide
4. Contact the backend team

---

## 🎓 Learning Path

### Beginner
1. ✅ Read API_QUICK_REFERENCE.md
2. ✅ Import and test Postman collection
3. ✅ Try basic fetch examples from Quick Reference
4. ✅ Build a simple search component

### Intermediate
1. ✅ Set up API client from Integration Guide
2. ✅ Create custom hooks/composables
3. ✅ Implement error handling
4. ✅ Add loading states

### Advanced
1. ✅ Implement caching strategy
2. ✅ Add request debouncing
3. ✅ Handle file uploads (voice/image)
4. ✅ Optimize performance

---

## 📊 API Statistics

- **Total Endpoints:** 7
- **JSON Endpoints:** 5
- **File Upload Endpoints:** 2
- **Authentication Required:** None
- **Rate Limiting:** None (currently)

---

## 🔄 Version Information

- **API Version:** 1.0.0
- **Documentation Version:** 1.0.0
- **Last Updated:** 2025-11-28

---

## 📝 Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ MarketWay Navigator API - Quick Reference                  │
├─────────────────────────────────────────────────────────────┤
│ Base URL: http://127.0.0.1:8000                            │
│ Docs: http://127.0.0.1:8000/docs                           │
├─────────────────────────────────────────────────────────────┤
│ POST   /ask                  Ask questions                 │
│ GET    /product/search?q=    Search products               │
│ GET    /line/info/{name}     Get line details              │
│ GET    /history              Get market history            │
│ POST   /voice/query          Voice interaction             │
│ POST   /image/identify       Image recognition             │
│ GET    /navigate?line_name=  Get directions                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎉 Ready to Build!

You now have everything you need to integrate the MarketWay Navigator API into your frontend application. Choose your framework, follow the integration guide, and start building amazing features!

**Happy Coding! 🚀**
