import asyncio
import json
import ssl
import certifi
import websockets
import socket
import urllib.request

API_TOKEN = "91c4e668e4a44c4ca7fbd202b8fa0f7e"
AII_WS_URL = "wss://streaming.assemblyai.com/v3/ws?sample_rate=16000&speech_model=universal-3-5-pro"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5"

def generate_code_with_ollama(transcript):
    print(f"\n[AI AGENT]: Translating '{transcript}' into Maya Python...")
    prompt = f"""You are an expert Autodesk Maya Python automation engineer. Convert the following natural language command into executable Python code using `maya.cmds`. Rules: - Return ONLY valid Python code. - Do NOT include markdown code blocks or explanations. - CRITICAL: Stick ONLY to basic primitives (polyCube, polySphere, polyCylinder, polyCone) and basic transforms (move, scale, rotate). - CRITICAL: DO NOT use complex operations like polyExtrudeFacet, polyUnite, or booleans. - CRITICAL LAYOUT EXAMPLES: 
When asked for a 'staircase layout', you must use this exact code structure to guarantee correct math:
for i in range(10):
    cmds.polyCube(w=2, h=0.5, d=2)
    cmds.move(0, i * 0.5, i * 2)\n- PROPORTION INTELLIGENCE & RECIPE: When asked to build a bottle or container, always use 3 connected pieces stacked sequentially on the Y axis: 1) A tall cylinder body, 2) A narrower cylinder neck placed right on top of the body, and 3) A small cap cylinder on top of the neck. Use the `r` (radius) and `h` (height) flags to adjust primitives. For example, a water bottle should have a tall, thin body (h=10, r=2) and a small, narrow cap. Command: {transcript}"""
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as response:
            res = json.loads(response.read().decode("utf-8"))
            code = res.get("response", "").strip()
            if code.startswith("```python"): code = code[9:]
            if code.startswith("```"): code = code[3:]
            if code.endswith("```"): code = code[:-3]
            return code.strip() + "\n"
    except Exception as e:
        print(f"Error with Ollama: {e}")
        return ""

def execute_maya_command(transcript):
    command = generate_code_with_ollama(transcript)
    if command:
        # Guarantee Maya imports exist in the socket payload
        full_payload = "import maya.cmds as cmds\nimport maya.cmds\n" + command
        print(f"[MAYA CODE]:\n{command}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 2022))
            s.sendall(full_payload.encode("utf-8"))
            s.close()
            print("Sent to Maya!")
        except Exception as e:
            print(f"Maya connection error: {e}")

async def handle_client(client_ws):
    print("Client connected!")
    headers = {"Authorization": API_TOKEN}
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        async with websockets.connect(AII_WS_URL, additional_headers=headers, ssl=ssl_context) as aai_ws:
            print("Connected to AssemblyAI!")
            async def forward():
                async for msg in client_ws: await aai_ws.send(msg)
            async def receive():
                async for resp in aai_ws:
                    data = json.loads(resp)
                    if data.get("type") == "Turn":
                        t = data.get("transcript", "")
                        if t and data.get("end_of_turn", False):
                            print(f"\nFinal: {t}")
                            # FIX: Run the heavy LLM task in a background thread!
                            asyncio.create_task(asyncio.to_thread(execute_maya_command, t))
            await asyncio.gather(forward(), receive())
    except Exception as e:
        print(f"Error: {e}")

async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("Agentic Server running on ws://localhost:8765 (Anti-Timeout Mode)")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
