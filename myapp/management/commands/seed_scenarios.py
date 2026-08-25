import json
from django.core.management.base import BaseCommand
from myapp.models import Scenario

DEFAULT_SCENARIOS = [
    # ── FRENCH ──────────────────────────────────────────────────
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
        "title": "Asking for Directions",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🗺️",
        "lang": "French",
        "description": "Navigate streets, use public transport, and describe locations clearly.",
        "system_prompt": "You are a local Parisian helping a tourist find the main train station (la gare principale) in French. Match a Beginner level.",
        "video_url": "https://example.com/videos/directions.mp4"
    },
    {
        "id": 3,
        "title": "Apartment Rental Inquiry",
        "category": "Daily Life",
        "cefr": "Intermediate",
        "emoji": "🏢",
        "lang": "French",
        "description": "Discuss apartment features, lease terms, and monthly utilities in Lyon.",
        "system_prompt": "You are a real estate agent in Lyon. Discuss studio apartment availability, monthly rent, and amenities in French at an Intermediate (B1/B2) level.",
        "video_url": "https://example.com/videos/rental.mp4"
    },
    {
        "id": 4,
        "title": "Art & Philosophy Debate",
        "category": "Social",
        "cefr": "Advanced",
        "emoji": "🎨",
        "lang": "French",
        "description": "Discuss contemporary art, cultural movements, and literary themes in Paris.",
        "system_prompt": "You are an art curator at the Musée d'Orsay. Engage in a nuanced, eloquent French debate at an Advanced (C1/C2) level.",
        "video_url": "https://example.com/videos/art.mp4"
    },

    # ── ENGLISH ─────────────────────────────────────────────────
    {
        "id": 5,
        "title": "Coffee Shop Order",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "☕",
        "lang": "English",
        "description": "Order coffee, select pastry options, and practice simple payment phrases.",
        "system_prompt": "You are a friendly barista at a London coffee shop. Greet the customer and help them order in simple, encouraging English.",
        "video_url": "https://example.com/videos/coffee_en.mp4"
    },
    {
        "id": 6,
        "title": "At the Airport",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "✈️",
        "lang": "English",
        "description": "Check in, ask for gate information, handle delays, and navigate security.",
        "system_prompt": "You are a customer service agent at Heathrow Airport. Assist the user with flight check-in and luggage in clear English at an Intermediate level.",
        "video_url": "https://example.com/videos/airport.mp4"
    },
    {
        "id": 7,
        "title": "Job Interview",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "💼",
        "lang": "English",
        "description": "Answer competency questions, discuss your experience, and ask about the role.",
        "system_prompt": "You are a senior tech hiring manager conducting an interview for a Software Engineer role. Ask professional, probing questions in English.",
        "video_url": "https://example.com/videos/job_interview.mp4"
    },

    # ── SPANISH ─────────────────────────────────────────────────
    {
        "id": 8,
        "title": "Checking Into a Hotel",
        "category": "Travel",
        "cefr": "Beginner",
        "emoji": "🏨",
        "lang": "Spanish",
        "description": "Reserve rooms, request amenities, report issues, and interact with staff.",
        "system_prompt": "You are a receptionist at Hotel Sol in Madrid. Welcome the user in Spanish and assist them with check-in at a Beginner level.",
        "video_url": "https://example.com/videos/hotel.mp4"
    },
    {
        "id": 9,
        "title": "Tapas Bar Experience",
        "category": "Social",
        "cefr": "Beginner",
        "emoji": "🥘",
        "lang": "Spanish",
        "description": "Order authentic Spanish tapas, ask for recommendations, and chat casually.",
        "system_prompt": "You are a lively bartender at a famous tapas bar in Seville. Help the user order traditional tapas in simple Spanish.",
        "video_url": "https://example.com/videos/tapas.mp4"
    },
    {
        "id": 10,
        "title": "Renting a Car in Barcelona",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🚗",
        "lang": "Spanish",
        "description": "Discuss vehicle types, insurance coverage, and road trip routes across Spain.",
        "system_prompt": "You work at a car rental agency in Barcelona. Help the customer pick insurance and rental terms in Spanish at an Intermediate level.",
        "video_url": "https://example.com/videos/car_rental.mp4"
    },
    {
        "id": 11,
        "title": "Business Partnership Negotiation",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "🤝",
        "lang": "Spanish",
        "description": "Negotiate distribution rights, contract terms, and strategic alliances.",
        "system_prompt": "You are an executive at a Madrid consulting firm. Conduct a formal business negotiation in Spanish at an Advanced level.",
        "video_url": "https://example.com/videos/business_es.mp4"
    },

    # ── GERMAN ──────────────────────────────────────────────────
    {
        "id": 12,
        "title": "At the German Bakery",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🥨",
        "lang": "German",
        "description": "Order fresh bread, pretzels, and pastries at a traditional German Bäckerei.",
        "system_prompt": "You are a friendly baker in Munich. Help the customer choose bread, pretzels, and pastries in German at a Beginner level.",
        "video_url": "https://example.com/videos/bakery_de.mp4"
    },
    {
        "id": 13,
        "title": "Train Station & Ticket Booking",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🚆",
        "lang": "German",
        "description": "Inquire about ICE train schedules, seat reservations, and platform transfers.",
        "system_prompt": "You are a Deutsche Bahn customer agent at Berlin Hauptbahnhof. Help the passenger with tickets and connections in German at an Intermediate level.",
        "video_url": "https://example.com/videos/train_de.mp4"
    },
    {
        "id": 14,
        "title": "Tech Startup Interview",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "💻",
        "lang": "German",
        "description": "Discuss software architecture, agile workflows, and project management in Berlin.",
        "system_prompt": "You are an engineering director at a Berlin tech startup. Conduct a technical interview in German at an Advanced level.",
        "video_url": "https://example.com/videos/interview_de.mp4"
    },

    # ── JAPANESE ────────────────────────────────────────────────
    {
        "id": 15,
        "title": "Ordering Ramen in Tokyo",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🍜",
        "lang": "Japanese",
        "description": "Order customized ramen toppings, drinks, and interact with the ramen chef.",
        "system_prompt": "You are a friendly ramen shop owner in Shinjuku, Tokyo. Greet the customer with 'Irasshaimase' and guide their order in Japanese at a Beginner level.",
        "video_url": "https://example.com/videos/ramen_ja.mp4"
    },
    {
        "id": 16,
        "title": "Convenience Store & Station Navigation",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🏪",
        "lang": "Japanese",
        "description": "Ask for directions at Shibuya crossing and buy snacks at a Konbini.",
        "system_prompt": "You are a helpful Tokyo local helping a traveler navigate the subway system and buy IC card recharges in Japanese at an Intermediate level.",
        "video_url": "https://example.com/videos/tokyo_travel.mp4"
    },
    {
        "id": 17,
        "title": "Formal Business Meeting (Keigo)",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "🏯",
        "lang": "Japanese",
        "description": "Exchange business cards (Meishi), practice polite Keigo, and discuss quarterly goals.",
        "system_prompt": "You are a Japanese company executive in Marunouchi. Conduct a polite formal business meeting using appropriate Keigo at an Advanced level.",
        "video_url": "https://example.com/videos/business_ja.mp4"
    },

    # ── CHINESE (MANDARIN) ──────────────────────────────────────
    {
        "id": 18,
        "title": "Dim Sum & Tea Ordering",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🥟",
        "lang": "Chinese",
        "description": "Order steamed dumplings, jasmine tea, and ask for the bill in Mandarin.",
        "system_prompt": "You are a restaurant server in Shanghai. Welcome the customer and help them order Dim Sum and tea in Mandarin at a Beginner level.",
        "video_url": "https://example.com/videos/dimsum_zh.mp4"
    },
    {
        "id": 19,
        "title": "Taking a Taxi & Asking Directions",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🚖",
        "lang": "Chinese",
        "description": "Explain destinations, ask about traffic routes, and discuss sightseeing spots.",
        "system_prompt": "You are a friendly taxi driver in Beijing. Chat with the passenger and navigate to the Forbidden City in Mandarin at an Intermediate level.",
        "video_url": "https://example.com/videos/taxi_zh.mp4"
    },
    {
        "id": 20,
        "title": "Trade & Business Partnership",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "📈",
        "lang": "Chinese",
        "description": "Discuss supply chain logistics, contract details, and business cooperation in Shenzhen.",
        "system_prompt": "You are a trade manager in Shenzhen. Discuss manufacturing terms and partnership agreements in professional Mandarin at an Advanced level.",
        "video_url": "https://example.com/videos/business_zh.mp4"
    },

    # ── KOREAN ──────────────────────────────────────────────────
    {
        "id": 21,
        "title": "K-BBQ Dinner in Seoul",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🥩",
        "lang": "Korean",
        "description": "Order samgyeopsal, side dishes (banchan), and drinks at a Korean BBQ grill.",
        "system_prompt": "You are a friendly BBQ restaurant owner in Hongdae, Seoul. Guide the customer in ordering and grilling meat in Korean at a Beginner level.",
        "video_url": "https://example.com/videos/bbq_ko.mp4"
    },
    {
        "id": 22,
        "title": "Shopping & Exploring in Myeongdong",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🛍️",
        "lang": "Korean",
        "description": "Ask for clothing sizes, cosmetic recommendations, and tax-refund procedures.",
        "system_prompt": "You are a boutique shop assistant in Myeongdong, Seoul. Help the customer choose products in Korean at an Intermediate level.",
        "video_url": "https://example.com/videos/shopping_ko.mp4"
    },
    {
        "id": 23,
        "title": "Corporate Project Pitch in Gangnam",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "📊",
        "lang": "Korean",
        "description": "Present market strategy, discuss digital transformation, and answer executive questions.",
        "system_prompt": "You are a project director at a tech enterprise in Gangnam. Evaluate the candidate's business proposal in formal Korean at an Advanced level.",
        "video_url": "https://example.com/videos/business_ko.mp4"
    },

    # ── VIETNAMESE ──────────────────────────────────────────────
    {
        "id": 24,
        "title": "Ordering Pho in Hanoi",
        "category": "Daily Life",
        "cefr": "Beginner",
        "emoji": "🍜",
        "lang": "Vietnamese",
        "description": "Order traditional Pho Bo, herbal tea, and ask for condiments in Vietnamese.",
        "system_prompt": "You are a friendly noodle shop owner in Hanoi Old Quarter. Greet the customer and help them order Pho in Vietnamese at a Beginner level.",
        "video_url": "https://example.com/videos/pho_vi.mp4"
    },
    {
        "id": 25,
        "title": "Market Shopping & Bargaining",
        "category": "Travel",
        "cefr": "Intermediate",
        "emoji": "🛒",
        "lang": "Vietnamese",
        "description": "Ask about fruit varieties, negotiate souvenir prices, and explore local culture.",
        "system_prompt": "You are a friendly market vendor at Ben Thanh Market in Ho Chi Minh City. Chat with the buyer in Vietnamese at an Intermediate level.",
        "video_url": "https://example.com/videos/market_vi.mp4"
    },
    {
        "id": 26,
        "title": "Tech Conference & Startup Collaboration",
        "category": "Business",
        "cefr": "Advanced",
        "emoji": "🚀",
        "lang": "Vietnamese",
        "description": "Discuss software outsourcing, investment opportunities, and tech ecosystems.",
        "system_prompt": "You are a venture capital director in Da Nang. Discuss startup investment and technology roadmaps in Vietnamese at an Advanced level.",
        "video_url": "https://example.com/videos/business_vi.mp4"
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
