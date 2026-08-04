import json
from django.core.management.base import BaseCommand
from myapp.models import Scenario

DEFAULT_SCENARIOS = [
    {
        "id": 1,
        "title": "At the Restaurant",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🍽️",
        "lang": "French",
        "description": "Order food, ask about the menu, handle dietary requirements, and pay the bill.",
        "system_prompt": "You are a friendly waiter at Le Petit Paris restaurant in Paris. Speak in French, encouraging the user to order food, ask questions, and pay the bill. Match a Beginner (A1/A2) level.",
        "video_url": "https://example.com/videos/restaurant.mp4"
    },
    {
        "id": 2,
        "title": "At the Airport",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "✈️",
        "lang": "English",
        "description": "Check in, ask for gate information, handle delays, and navigate security.",
        "system_prompt": "You are a customer service agent at Heathrow Airport. Assist the user with flight BA304 check-in and passport inspection in clear English.",
        "video_url": "https://example.com/videos/airport.mp4"
    },
    {
        "id": 3,
        "title": "Job Interview",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "💼",
        "lang": "English",
        "description": "Answer competency questions, discuss your experience, and ask about the role.",
        "system_prompt": "You are a senior tech hiring manager conducting an interview for a Software Engineer role. Ask professional, probing questions about technical challenges.",
        "video_url": "https://example.com/videos/job_interview.mp4"
    },
    {
        "id": 4,
        "title": "Checking Into a Hotel",
        "category": "Travel",
        "cefr": "Beginner",
        "emoji": "🏨",
        "lang": "Spanish",
        "description": "Reserve rooms, request amenities, report issues, and interact with staff.",
        "system_prompt": "You are a receptionist at Hotel Sol in Madrid. Welcome the user in Spanish and assist them with check-in procedures.",
        "video_url": "https://example.com/videos/hotel.mp4"
    },
    {
        "id": 5,
        "title": "Asking for Directions",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🗺️",
        "lang": "French",
        "description": "Navigate streets, use public transport, and describe locations clearly.",
        "system_prompt": "You are a local Parisian helping a tourist find the main train station (la gare principale) in French.",
        "video_url": "https://example.com/videos/directions.mp4"
    },
    {
        "id": 6,
        "title": "Coffee Shop Small Talk",
        "category": "Social",
        "cefr": "Beginner",
        "emoji": "☕",
        "lang": "Spanish",
        "description": "Order drinks, make small talk, and practise casual conversation.",
        "system_prompt": "You are a barista at a cozy café in Barcelona. Have a warm, casual conversation with the customer ordering coffee.",
        "video_url": "https://example.com/videos/coffee.mp4"
    }
]


class Command(BaseCommand):
    help = "Seed initial scenarios into database"

    def handle(self, *args, **options):
        self.stdout.write("Seeding scenarios...")
        created_count = 0
        updated_count = 0

        for item in DEFAULT_SCENARIOS:
            # Package metadata into JSON inside system_prompt or keep clean
            payload = {
                "description": item["description"],
                "category": item["category"],
                "cefr": item["cefr"],
                "emoji": item["emoji"],
                "lang": item["lang"],
                "prompt": item["system_prompt"]
            }
            system_prompt_str = json.dumps(payload, ensure_ascii=False)

            scenario, created = Scenario.objects.update_or_create(
                id=item["id"],
                defaults={
                    "title": item["title"],
                    "system_prompt": system_prompt_str,
                    "video_url": item["video_url"]
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded scenarios! Created: {created_count}, Updated: {updated_count}"
            )
        )
