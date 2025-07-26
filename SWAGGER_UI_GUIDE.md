# Swagger UI Authentication Guide

## 🔐 How to Use Swagger UI with Authentication

The 403 errors you're seeing are **completely normal** - the API requires authentication tokens.

### ✅ Step-by-Step Instructions:

1. **Open Swagger UI**: http://localhost:8200/docs

2. **Click the "Authorize" button** (🔒 icon) at the **top right** of the page

3. **Enter one of these mock tokens** in the authorization dialog:
   ```
   linq-demo-token
   ```
   OR
   ```
   linq-assessment-token
   ```
   OR
   ```
   linq-sales-engineer
   ```

4. **Click "Authorize"** then **"Close"**

5. **Test the Auth endpoints**:
   - **GET /contacts**: Click "Try it out" → "Execute"
   - **POST /contacts**: Click "Try it out" → Fill form → "Execute"
   - **GET /contacts/stats**: Click "Try it out" → "Execute"
