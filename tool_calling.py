from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

load_dotenv()

class Confidence(str, Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

class Assistant(BaseModel):
    agent_name: Annotated[str, Field(min_length=5, max_length=50)]
    short_description: Annotated[str, Field(min_length=100, max_length=1500)]
    target_users: Annotated[list[str], Field(min_length=3, max_length=5)]
    core_tools_needed: Annotated[list[str], Field(min_length=4, max_length=6)]
    suggested_tech_stack: Annotated[list[str], Field(min_length=4, max_length=7)]
    first_milestone: Annotated[str, Field(min_length=100, max_length=500)]
    potential_challenges: Annotated[list[str], Field(min_length=3, max_length=5)]
    confidence: Confidence 

system_prompt = '''You are a Senior AI Agent Architect. 

CRITICAL CONSTRAINTS:
1. agent_name: Must be professional and catchy.
2. short_description: Explain the 'how' and 'benefit' clearly. Keep it under 100 words.
3. target_users: Provide a list of 3 to 5 hyper-specific personas.
4. core_tools_needed: Provide a list of 4 to 6 specific functions or integrations.
5. suggested_tech_stack: Provide 4 to 7 realistic, Python-based tools.
6. first_milestone: Provide a concrete task achievable within 14 days. Be descriptive to meet length requirements.
7. potential_challenges: Provide 3 to 5 distinct technical or logical risks.
8. confidence: Use ONLY lowercase: 'high', 'medium', or 'low'.'''

agent = Agent(
    model='groq:llama-3.3-70b-versatile',
    output_type=Assistant,
    instructions=system_prompt
)

@agent.tool_plain
def CurrentDateTime(timezone: str = 'UTC') -> str:
    '''Get the current date & time. Pass timezone as "UTC" if unsure. Call this with no argument: {}'''
    result = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[TOOL CALLED] CurrentDateTime → {result}')  # <-- add this
    return result

History: list[ModelMessage] = []

def helper_function(user_string: str):
    data = agent.run_sync(f'Extract: {user_string}', message_history=History)
    History.extend(data.new_messages()) 

    print('Agent Name:', data.output.agent_name)
    print('Short Description:', data.output.short_description)
    
    if data.output.target_users:
        print('Target Users:')
        for point in data.output.target_users:
            print(f'. {point}')

    if data.output.core_tools_needed:
        print('Core Tools Needed:')
        for point in data.output.core_tools_needed:
            print(f'. {point}')

    if data.output.suggested_tech_stack:
        print('Suggested Tech Stack:')
        for point in data.output.suggested_tech_stack:
            print(f'. {point}')

    print(f'First Milestone: {data.output.first_milestone}')

    if data.output.potential_challenges:
        print('Potential Challenges:')
        for point in data.output.potential_challenges:
            print(f'. {point}')

    print(f'Confidence: {data.output.confidence}')

if __name__ == '__main__':
    while True:
        user_string = str(input('Enter your query ("exit" for exit): '))
        if user_string.lower() == 'exit':
            break
        helper_function(user_string)

    