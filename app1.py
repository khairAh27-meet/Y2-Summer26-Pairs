from anthropic import Anthropic
from dotenv import load_dotenv
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime, timedelta


load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


print("🌍 Welcome to the AI Travel Planner!")

destination = input("Destination: ")
start_date = input("Start date: ")
end_date = input("End date: ")
budget = input("Budget ($): ")
interests = input("Interests (separated by commas): ")


prompt = f"""
You are an expert travel planner.

Create a personalized day-by-day travel itinerary.

Destination: {destination}
Start Date: {start_date}
End Date: {end_date}
Budget: ${budget}
Interests: {interests}

For each day include:
- Morning
- Afternoon
- Evening

Do NOT include prices.
"""


response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1500,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


itinerary = response.content[0].text


print("\n Your Travel Itinerary\n")
print(itinerary)


pdf_file = "travel_plan.pdf"

doc = SimpleDocTemplate(pdf_file)

styles = getSampleStyleSheet()

content = []

content.append(
    Paragraph(f"Travel Plan: {destination}", styles["Title"])
)

content.append(Spacer(1, 20))


for line in itinerary.split("\n"):
    content.append(
        Paragraph(line, styles["Normal"])
    )
    content.append(
        Spacer(1, 10)
    )


doc.build(content)

print("PDF created:", pdf_file)


def create_calendar_file(destination, start_date, itinerary):

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        try:
            start = datetime.strptime(start_date, "%Y/%m/%d")
        except ValueError:
            start = datetime.strptime(start_date, "%d/%m/%Y")


    calendar = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Travel Planner//EN
"""


    days = itinerary.split("Day")

    for i, day in enumerate(days[1:]):

        event_date = start + timedelta(days=i)

        date = event_date.strftime("%Y%m%d")

        description = day.replace("\n", " ")

        calendar += f"""
BEGIN:VEVENT
SUMMARY:{destination} Trip - Day {i+1}
DESCRIPTION:{description}
DTSTART;VALUE=DATE:{date}
DTEND;VALUE=DATE:{date}
END:VEVENT
"""


    calendar += """
END:VCALENDAR
"""


    with open("travel_plan.ics", "w", encoding="utf-8") as file:
        file.write(calendar)



create_calendar_file(
    destination,
    start_date,
    itinerary
)


print(" Google Calendar created: travel_plan.ics")
print(" All files created successfully!")