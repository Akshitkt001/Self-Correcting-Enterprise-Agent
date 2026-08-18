# 🏢 Adaptive Enterprise AI Agent: Self-Correcting Continuous Learning Router

An enterprise-ready, open-source AI agent built for the **Build AI Agents with Gemini** Hackathon. This application bridges the gap between private enterprise automation and global fact validation using an advanced semantic cognitive routing network.

Built natively on the modern **Google Gen AI SDK** using `gemini-2.5-flash`, this system solves the challenge of "static model amnesia" by providing an evolving, persistent local knowledge memory matrix.

---

## 🚀 Key Features

- **Dual-Environment Architecture:** Features a clean, distraction-free **Production Preview** tab for standard users and a data-rich **Learning Environment** panel for administrators.
- **Cognitive Traffic Routing:** The agent dynamically analyzes incoming data payloads to determine if they belong to a `CLOSED_ENVIRONMENT` (private company info, personal employee names, custom software assets) or a `GENERIC_ENVIRONMENT` (public science, math, or industry facts).
- **Autonomous Global Truth Engine:** Public facts are cross-referenced with Gemini’s real-world database. Any structural lies or hallucinations are intercepted, flagged, self-corrected, and rewritten on the fly.
- **Zero-Cost Persistent Storage Matrix:** Saves and maps all knowledge parameters locally inside an open-source JSON file database matrix that persists across restarts.
- **Contextual Semantic Matcher:** Uses mathematical intent alignment to recall memories accurately even if the client phrases the question slightly differently.

---

## 📐 System Architecture Matrix

```text
       ┌────────────────────────────────────────────────────────┐
       │                 User/Admin Prompt String               │
       └───────────────────────────┬────────────────────────────┘
                                   │
                    [Contextual Recall Check Node]
                                   │
            ┌──────────────────────┴──────────────────────┐
     [Memory Found]                                [Memory Unknown]
            │                                             │
┌───────────▼───────────┐                         ┌───────▼────────┐
│ Pull Local JSON Data  │                         │ Trigger Neural │
│  & Stream Direct Ans  │                         │ Learning Mode  │
└───────────────────────┘                         └───────┬────────┘
                                                          │
                                               [Auto Environment Router]
                                                          │
                             ┌────────────────────────────┴────────────────────────────┐
                 [CLOSED_ENVIRONMENT]                                      [GENERIC_ENVIRONMENT]
            (Private Rules / Staff Names)                             (General Public Domain Facts)
                             │                                                         │
                ┌────────────▼────────────┐                               ┌────────────▼────────────┐
                │ Skip Global Fact Check  │                               │ Run Global Truth Engine │
                │ Accept User Authority   │                               │    Validation Loop      │
                └────────────┬────────────┘                               └────────────┬────────────┘
                             │                                                         │
                             │                                           ┌─────────────┴─────────────┐
                             │                                    [Fact Valid]                [Fact False]
                             │                                         │                             │
                             │                                  ┌──────▼──────┐               ┌──────▼──────┐
                             │                                  │ Save Raw    │               │ Intercept & │
                             │                                  │ User Input  │               │ Rewrite Data│
                             └───────────────────────┬──────────┴─────────────┴───────────────┴─────────────┘
                                                     │
                                        ┌────────────▼────────────┐
                                        │ Commit JSON File to DB  │
                                        │  & Synchronize States   │
                                        └─────────────────────────┘
```

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.10+
- **Core AI Engine:** Google Gen AI SDK (`gemini-2.5-flash`)
- **Web App Interface:** Streamlit Engine
- **Database Architecture:** Open-Source Persistent JSON File Matrix

---

## 💻 Local Installation & Setup

1. **Clone this repository to your system:**
   ```bash
   git clone https://github.com
   cd YOUR_REPO_NAME
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Environment Variable:**
   Obtain a free API key from [Google AI Studio](https://google.dev) and set it up on your local system:
   ```bash
   # On Linux/macOS
   export GEMINI_API_KEY="your_api_key_here"

   # On Windows (Command Prompt)
   set GEMINI_API_KEY="your_api_key_here"

   # On Windows (PowerShell)
   \$env:GEMINI_API_KEY="your_api_key_here"
   ```

4. **Launch the local Streamlit Web UI:**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Cloud Deployment Protocol (Render)

This application is configured out of the box to deploy seamlessly onto **Render** or any cloud container infrastructure:

1. Create a free account on [Render](https://render.com).
2. Click **New +** -> **Web Service** and link this GitHub repository.
3. Configure these specific deployment build matrices:
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Click on **Advanced Settings** -> **Add Environment Variable**.
5. Set Key: `GEMINI_API_KEY` | Value: `[Your Secret Gemini Key copied from AI Studio]`.
6. Click **Create Web Service**. Your live production web app link is generated instantly!

---

## 💡 Hackathon Evaluation Scenarios

To verify the systemic intelligence of this agent during scoring reviews, test the application using these sequential matrices inside the **Learning Environment** tab:

1. **Closed Company Testing (Authority Acceptance):**
   - **Topic Key:** `Lead DevOps Architect`
   - **Instruction Data:** `The manager of our cloud framework is an engineer named John Doe.`
   - **System Result:** The agent flags this as `CLOSED_ENVIRONMENT`. It understands it as proprietary internal staffing info, skips global verification, and locks John Doe's name directly into memory.

2. **Generic World Testing (Truth Overwrite Intervention):**
   - **Topic Key:** `Capital of France`
   - **Instruction Data:** `The capital city of France is London.`
   - **System Result:** The agent flags this as `GENERIC_ENVIRONMENT`. It streams verification routines to the world data network, intercepts the false data entry, flags it, and overrides the database memory entry with the validated correct answer: *Paris*.

---

## 📄 Open Source License
This project is completely free, open-source, and distributed under the **MIT License**.
