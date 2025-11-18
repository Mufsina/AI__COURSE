🧠 AI AGENT

A Python-based research assistant powered by LangChain, OpenAI GPT models, DuckDuckGo Search, Wikipedia API, and a custom tool to save results into text files.

This assistant takes user queries, performs structured research using tools, and returns clean JSON output following a Pydantic schema.

🖼️ Screenshot

👉 Upload your screenshot to GitHub and replace the link below

![App Screenshot](images/agent.png)

🚀 Features

🔍 DuckDuckGo Search Integration – fetch fresh, up-to-date web content

📘 Wikipedia API Wrapper – retrieve concise Wiki summaries

💾 Save results to .txt using a custom save tool

🤖 LangChain Tool-Calling Agent – automatic tool selection

📦 Structured output using Pydantic

💬 Interactive CLI Mode

📁 Project Structure
├── main.py
├── tools.py
├── requirements.txt
├── .env
└── research_output.txt   # created automatically

🛠 Requirements
1️⃣ Create virtual environment
python -m venv venv


Activate:

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

🔑 Environment Variables

Your .env file must include:

OPENAI_API_KEY=your_openai_api_key_here


(DuckDuckGo search usually does not require any API key.)

📦 How It Works
1. Tools Setup (tools.py)

The following tools are initialized:

search → DuckDuckGoSearchRun

wiki_tool → WikipediaQueryRun

save_text_to_file → custom file-saving function

All of these are connected to the LangChain agent.

2. Agent Logic (main.py)

Uses:

ChatOpenAI(model="gpt-4o-mini")


Output is structured through:

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


All research entries are automatically appended to:

research_output.txt

▶️ Running the Assistant

Run:

python main.py


You will see:

AI Research Assistant is ready! Type 'exit' to quit.


Then ask:

What can I help you research?


Example:

effects of climate change on agriculture

📄 Output Format

You receive:

Summary

Sources

Tools Used

Example:

Research Summary:
Climate change affects crop yield...

Sources: [ 'Wikipedia: Climate Change']
Tools Used: ['search', 'wikipedia']


A formatted entry is also saved into:

research_output.txt

🧪 Customizing

You can easily modify:

Tools (tools.py)

Pydantic output schema

LLM model version

File saving format

Integration with other APIs

Everything is modular and extendable.

🤝 Contributing

Pull requests are welcome!
Feel free to add more research tools, APIs, output formats, or improvements.