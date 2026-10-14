"""Local Gemini-to-OpenRouter API Bridge.
Enables Google ADK and Google GenAI SDK to seamlessly use OpenRouter with cheap models.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import json
import os
import uvicorn

app = FastAPI()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")

def fix_schema(s):
    if not isinstance(s, dict):
        return s
    res = {}
    for k, v in s.items():
        if k == "type" and isinstance(v, str):
            res[k] = v.lower()
        elif isinstance(v, dict):
            res[k] = fix_schema(v)
        elif isinstance(v, list):
            res[k] = [fix_schema(item) if isinstance(item, dict) else item for item in v]
        else:
            res[k] = v
    if "properties" in res and "type" not in res:
        res["type"] = "object"
    return res

@app.get("/v1beta/models/{model_name:path}")
async def get_model(model_name: str):
    return {
        "name": f"models/{model_name}",
        "supportedGenerationMethods": ["generateContent", "countTokens"]
    }

@app.post("/v1beta/models/{model_path:path}")
async def generate_content(model_path: str, request: Request):
    body = await request.json()
    
    # Extract tools
    tools_payload = []
    for tool_group in body.get("tools", []):
        for decl in tool_group.get("functionDeclarations", []):
            params = fix_schema(decl.get("parameters", {}))
            tools_payload.append({
                "type": "function",
                "function": {
                    "name": decl.get("name"),
                    "description": decl.get("description", ""),
                    "parameters": params
                }
            })

    # Extract messages
    messages = []
    
    # System instruction
    sys_inst = body.get("systemInstruction")
    if sys_inst:
        sys_text = "".join(p.get("text", "") for p in sys_inst.get("parts", []))
        if sys_text:
            messages.append({"role": "system", "content": sys_text})

    # Contents
    for c in body.get("contents", []):
        role = c.get("role", "user")
        parts = c.get("parts", [])
        
        # Check for function responses
        fn_responses = [p for p in parts if "functionResponse" in p]
        fn_calls = [p for p in parts if "functionCall" in p]
        text_parts = [p.get("text", "") for p in parts if "text" in p]

        if fn_responses:
            for p in fn_responses:
                resp_info = p["functionResponse"]
                messages.append({
                    "role": "tool",
                    "tool_call_id": resp_info.get("id", f"call_{resp_info.get('name')}"),
                    "name": resp_info.get("name"),
                    "content": json.dumps(resp_info.get("response", {}))
                })
        elif fn_calls:
            tcs = []
            for i, p in enumerate(fn_calls):
                fc = p["functionCall"]
                tcs.append({
                    "id": fc.get("id", f"call_{fc.get('name')}"),
                    "type": "function",
                    "function": {
                        "name": fc.get("name"),
                        "arguments": json.dumps(fc.get("args", {}))
                    }
                })
            messages.append({
                "role": "assistant",
                "content": "".join(text_parts) or None,
                "tool_calls": tcs
            })
        else:
            messages.append({
                "role": "assistant" if role == "model" else "user",
                "content": "".join(text_parts)
            })

    # Prepare OpenRouter request
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }
    if tools_payload:
        payload["tools"] = tools_payload

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        data = resp.json()

    if "error" in data:
        return JSONResponse(status_code=500, content=data)

    choice = data["choices"][0]
    msg = choice["message"]

    parts = []
    if msg.get("tool_calls"):
        for tc in msg["tool_calls"]:
            fn = tc["function"]
            args = json.loads(fn.get("arguments", "{}"))
            parts.append({
                "functionCall": {
                    "id": tc.get("id"),
                    "name": fn.get("name"),
                    "args": args
                }
            })
    else:
        parts.append({"text": msg.get("content", "")})

    return {
        "candidates": [
            {
                "content": {
                    "role": "model",
                    "parts": parts
                },
                "finishReason": "STOP"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8088)
