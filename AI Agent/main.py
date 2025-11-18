import json
import warnings
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool


warnings.filterwarnings("ignore")


load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]



llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that helps generate concise, structured research output.
            Use necessary tools (search, wikipedia, save_text_to_file).
            Wrap your final response in this format only — no extra text:
            {format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


tools = [search_tool, wiki_tool, save_tool]


agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print(" AI Research Assistant is ready! Type 'exit' to quit.\n")

    while True:
        query = input("What can I help you research? ").strip()
        if query.lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break

        try:
            raw_response = agent_executor.invoke({"query": query})

            output_str = raw_response.get("output", "{}")
            output_data = json.loads(output_str)
            structured_response = ResearchResponse(**output_data)

            
            print("\n Research Summary:")
            print(structured_response.summary)
            print("\n Sources:", structured_response.sources)
            print("\n Tools Used:", structured_response.tools_used)
            print("-" * 80)

        except json.JSONDecodeError:
            print("⚠️ Could not parse JSON from output:", raw_response)
        except Exception as e:
            print("⚠️ Error parsing response:", e, "Raw Response -", raw_response)
