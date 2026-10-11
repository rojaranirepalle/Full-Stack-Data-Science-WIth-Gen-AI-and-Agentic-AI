# pip install phidata  
# pip install groq
 
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="qwen/qwen3.8-27b"),
    markdown=True
)

agent.print_response("about nvidia stock")
