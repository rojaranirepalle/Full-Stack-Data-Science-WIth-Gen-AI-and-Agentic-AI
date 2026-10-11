from phi.agent import Agent, RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.google import Gemini as _Gemini
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
import os
import time

# Load API keys
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Free tier allows only 5 requests/minute per model, and the team makes many
# calls per query, so space requests out and retry if we still hit a 429.
MIN_SECONDS_BETWEEN_CALLS = 13
_last_call = 0.0


def _wait_for_slot():
    global _last_call
    wait = MIN_SECONDS_BETWEEN_CALLS - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()


class Gemini(_Gemini):
    def invoke(self, messages):
        for attempt in range(4):
            _wait_for_slot()
            try:
                return super().invoke(messages=messages)
            except ResourceExhausted:
                if attempt == 3:
                    raise
                time.sleep(30)

    def invoke_stream(self, messages):
        for attempt in range(4):
            _wait_for_slot()
            yielded = False
            try:
                for chunk in super().invoke_stream(messages=messages):
                    yielded = True
                    yield chunk
                return
            except ResourceExhausted:
                if yielded or attempt == 3:
                    raise
                time.sleep(30)


agent = Agent(
    model=Gemini(id="gemini-3.6-flash"),
    markdown=True,
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
#agent.print_response("Share a 2 sentence horror story.")


# ✅ Live Cricket Match Agent
match_agent = Agent(
    name="Live Match Agent",
    model=Gemini(id="gemini-3.6-flash"),  # Using OpenAI GPT-4o
    tools=[DuckDuckGo()],
    instructions=[
        "Search for live cricket match scores.",
        "Summarize the score, top players, and match situation.",
        "Use markdown tables for clarity."
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# ✅ Player Stats Agent
player_agent = Agent(
    name="Player Stats Agent",
    model=Gemini(id="gemini-3.6-flash"),
    tools=[DuckDuckGo()],
    instructions=[
        "Find recent cricket player statistics.",
        "Include batting and bowling stats for the last 5 matches.",
        "Use tables for formatting."
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# ✅ Cricket News Agent
news_agent = Agent(
    name="Cricket News Agent",
    model=Gemini(id="gemini-3.6-flash"),
    tools=[DuckDuckGo()],
    instructions=[
        "Find and summarize the latest cricket news.",
        "Highlight upcoming matches, injuries, and tournament updates.",
        "List headlines with sources."
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# ✅ Main Cricket Team (Combining all agents)
cricket_team = Agent(
    name="Cricket Analysis Team",
    model=Gemini(id="gemini-3.6-flash"),
    team=[match_agent, player_agent, news_agent],
    instructions=[
        "Provide live match scores, player statistics, and news updates.",
        "Use structured formatting and markdown tables.",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# ✅ Run Query to Fetch Cricket Data
cricket_team.print_response(
    "Get the latest score of the India vs Australia match, recent stats for Virat Kohli, and cricket news.", 
    stream=True
)