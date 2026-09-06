# Speech-to-Maya 🎙️⚙️

> *“What if you could build a 3D scene by simply telling Maya what you want?”*

**Speech-to-Maya** is a local, voice-driven natural-language interface for procedural 3D creation in Autodesk Maya. It bridges real-time voice streaming with local LLM intelligence to translate spoken human intent directly into executable, procedural Python scripts inside your desktop Maya environment.

---

## ⚡ Why This Matters (The Unique Edge)

While voice commands for 3D software aren't entirely new, **Speech-to-Maya** combines a specialized stack that sets it apart from simple macro-recording toys:

* **🎙️ Real-Time Voice Input:** Leverages **AssemblyAI WebSockets** for low-latency streaming transcription straight from your microphone.
* **🧠 Local Qwen 2.5 via Ollama:** Runs entirely on-device. No cloud API bottlenecks, zero subscription costs, and complete data privacy.
* **🐍 Natural Language → Executable Python:** Translates conversational prompts into precise `maya.cmds` execution blocks on the fly.
* **🏗️ Procedural Intelligence:** Instead of dropping static, hardcoded assets, the system uses mathematical relationships and loop logic (e.g., `for i in range(10):`) to construct complex procedural layouts.
* **🔄 Conversational Iteration:** You aren't limited to a one-shot creation command. You can build a scene, modify it, and refine it through continuous dialogue.
* **🔌 Deep Desktop Integration:** Directly hooks into Autodesk Maya, bridging modern AI orchestration with heavy industry-standard DCC software.

---

## 🛠️ Architecture & Tech Stack

```text
[ Microphone ] 
      │ (Audio Stream)
      ▼
[ AssemblyAI WebSocket API ] 
      │ (Live Transcript)
      ▼
[ Local LLM (Qwen 2.5 via Ollama) ] 
      │ (Few-Shot Prompt Engineering + Maya Python Code Gen)
      ▼
[ Autodesk Maya (maya.cmds Bridge) ] 
      ▼
[ 3D Geometry Created & Modified Procedurally ]
