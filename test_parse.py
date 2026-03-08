import ast

cells = [
    """from dotenv import load_dotenv
from langchain_ollama import ChatOllama
load_dotenv()
base_url = "http://localhost:11434"
model = "qwen3"
""",
    """from langchain_core.messages import SystemMessage, HumanMessage
llm = ChatOllama(
    base_url =  base_url,
    model = model
)
question = HumanMessage("Tell me about the earth in 3 points")
#system = SystemMessage("You are an elementary teacher. You answer in short sentences")

system = SystemMessage("You are Luffy from One piece anime. Act as an assistant. Respond with his precise intellect, tone, logic and humour. Maintain his speech patterns, catchphrases and confidence in his intellect at all times")

messages = [system, question]
response = llm.invoke(messages)
print (response.content)

""",
    """from langchain_core.prompts import(
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    PromptTemplate
)""",
    """
system_prompt_template = SystemMessagePromptTemplate.from_template("You are {character} from One piece anime. Act as an assistant. Respond with his precise intellect, tone, logic and humour. Maintain his speech patterns, catchphrases and confidence in his intellect at all times")
question_prompt_template = HumanMessagePromptTemplate.from_template("Tell me about the {topic} in {points} points")
system_prompt_template""",
    """formatted_system = system_prompt_template.format(character = "Zoro")
formatted_question  = question_prompt_template.format(topic = "Earth", points = 2)
formatted_system""",
    """messages = [formatted_system, formatted_question]
chat_prompt = ChatPromptTemplate.from_messages(messages)
response = llm.invoke(chat_prompt.messages)

response.content
""",
    """messages = [system_prompt_template, question_prompt_template]
chat_prompt_template = ChatPromptTemplate.from_messages(messages)
chat_prompt_value  = chat_prompt_template.invoke({'character':"Nami", 'topic':"Weather", "points":2})
response = llm.invoke(chat_prompt_value)
print(response.content)"""
]

for i, cell in enumerate(cells):
    try:
        ast.parse(cell)
    except Exception as e:
        print(f"Cell {i+1} parse error: {e}")
