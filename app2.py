#<<<<<<< HEAD

#=======
import os
from urllib.parse import quote
from anthropic import Anthropic
from dotenv import load_dotenv
import requests

load_dotenv()


# ------------------------
# Weather Function
# ------------------------

def get_weather(location):
    url = f"https://wttr.in/{quote(location)}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current_condition"][0]

        return f"""
Current weather in {location}
Weather: {current['weatherDesc'][0]['value']}
Temperature: {current['temp_C']}°C
Feels like: {current['FeelsLikeC']}°C
Humidity: {current['humidity']}%
Wind: {current['windspeedKmph']} km/h
"""

    except Exception:
        return "Couldn't get the weather."


# ------------------------
# Get user travel info
# ------------------------

def user_info():
    location = input("Where are you travelling? ")
    activity = input("What are you interested in doing? ")
    budget = int(input("What's your budget? "))

    return location, activity, budget


# ------------------------
# Google Maps link function
# ------------------------

def google_maps_link(place):
    return f"https://www.google.com/maps/search/?api=1&query={quote(place)}"


# ------------------------
# Claude setup
# ------------------------

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found!")

client = Anthropic(api_key=api_key)


# ------------------------
# Chat function
# ------------------------

def run_agent2():

    print("You: (type exit to quit)")

    system_message = """
your name is ward, Your job is to provide real travel answers and do not make up facts.

Rules:
- Be creative
- Be helpful
- Never invent information unless the user asks you to.
- When suggesting a place, always include a Google Maps link if possible.
- If the user asks about the weather, use the weather information provided below instead of guessing.

Response format:
- Start with a one-sentence summary of what the user said.
- Then give your answer.
- End with one follow-up question.
"""

    history = []

    while True:

        user_input = input(">> ")

        if user_input.lower() == "exit":
            break

        # Create Google Maps link
        map_link = google_maps_link(user_input)

        # Get weather if requested
        weather_info = ""

        if "weather" in user_input.lower():
            location = input("Which city would you like the weather for? ")
            weather_info = get_weather(location)

        # Add everything to Claude's context
        user_message = f"""
User request:
{user_input}

Google Maps link:
{map_link}

Weather information:
{weather_info}
"""

        history.append({
            "role": "user",
            "content": user_message
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text

        print(f"\nClaude: {reply}\n")

        history.append({
            "role": "assistant",
            "content": reply
        })



# Start program


run_chat()
# ------------------------
#run_chat()

#>>>>>>> 6128ef1d4d07a72777d4a2c33a68c945318f78aa
