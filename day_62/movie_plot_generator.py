import random
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from PIL import Image, ImageDraw, ImageFont
import re
import requests
from io import BytesIO

# Sample training data for genre classification
training_plots = [
    ("A hacker battles an AI overlord in a futuristic city.", "Sci-Fi"),
    ("A couple rekindles their romance after years apart.", "Romance"),
    ("A detective chases a cunning serial killer.", "Thriller"),
    ("Friends get into absurd mishaps on a road trip.", "Comedy"),
    ("A scientist uses a time machine to save his family.", "Sci-Fi"),
    ("A woman falls for a stranger with a deadly secret.", "Romance"),
    ("A spy uncovers a global conspiracy in a race against time.", "Thriller"),
    ("A chef’s chaotic restaurant opening leads to laughs.", "Comedy"),
    ("A time traveler falls in love while chasing a fugitive.", "Thriller"),
    ("A robot and human bond in a post-apocalyptic world.", "Sci-Fi"),
    ("A con artist’s scam spirals into a darkly funny chase.", "Dark Comedy"),
    ("A romantic getaway turns into a twisted, hilarious mystery.", "Dark Comedy"),
    ("A couple’s love is tested by a thrilling conspiracy.", "Thriller"),
    ("A quirky thief falls for their target, leading to chaotic laughs.", "Dark Comedy"),
    ("A scientist’s rogue AI robot unleashes terror in a lab.", "Horror"),
    ("A haunted robot stalks its creator in a deserted facility.", "Horror"),
    ("A couple’s road trip turns deadly when they encounter a cursed relic.", "Horror"),
    ("A time traveler’s love triggers a terrifying paradox.", "Horror")
]

# Train a simple genre classifier
plots, genres = zip(*training_plots)
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(plots)
classifier = MultinomialNB()
classifier.fit(X, genres)

# Movie title generator
def generate_title(keywords):
    adjectives = ["Echoes of", "Shadows of", "Rise of", "Last", "Infinite", "Lost"]
    nouns = ["Tomorrow", "Destiny", "Stars", "Time", "Heart", "Abyss"]
    title = f"{random.choice(adjectives)} {random.choice(nouns)}"
    if random.random() > 0.5:
        title += f" {random.choice(keywords).title()}"
    return title

# Template-based plot generator with transitions
def generate_plot(keywords):
    templates = {
        "horror": [
            "A {role} discovers a {threat} in a {setting}, triggering a terrifying {event}.",
            "{character} battles a {threat} in a {setting}, racing to stop a {event}."
        ],
        "love": [
            "A {role} falls for {target}, but their romance faces a {conflict} in a {setting}.",
            "{character} and {target} kindle a romance amidst a {conflict} in a {setting}."
        ],
        "travel": [
            "A {role}’s {journey} uncovers a {secret} in a {setting}, leading to a {event}.",
            "{character} embarks on a {journey}, revealing a {secret} in a {setting}."
        ],
        "thriller": [
            "A {role} uncovers a {secret}, sparking a chase against {villain} in a {setting}.",
            "{character} discovers a {secret}, battling {villain} in a high-stakes {event}."
        ]
    }
    
    transitions = {
        "horror": ["when a chilling {threat} emerges.", "as a horrifying {event} unfolds."],
        "love": ["but their love is tested by {conflict}.", "while their hearts face a {conflict}."],
        "travel": ["during a perilous {journey}.", "as their {journey} takes a dark turn."],
        "thriller": ["leading to a tense {event}.", "sparking a deadly {event}."]
    }
    
    roles = ["traveler", "scientist", "explorer", "writer"]
    targets = ["a mysterious stranger", "a fellow adventurer", "a haunted soul"]
    threats = ["cursed relic", "ghostly entity", "malevolent force"]
    journeys = ["time-travel quest", "cross-country road trip", "space voyage"]
    settings = ["haunted town", "ancient ruins", "isolated spaceship", "foggy wilderness"]
    conflicts = ["supernatural curse", "dark secret", "terrifying paradox"]
    secrets = ["hidden curse", "forbidden ritual", "cosmic anomaly"]
    villains = ["a vengeful spirit", "a secret cult", "a rogue AI"]
    events = ["showdown", "ritual", "escape", "catastrophe"]
    
    # Generate plot parts for each keyword
    plot_parts = []
    for i, kw in enumerate(keywords):
        if kw in templates:
            template = random.choice(templates[kw])
            part = template.format(
                role=random.choice(roles),
                character=random.choice(roles).title(),
                target=random.choice(targets),
                threat=random.choice(threats),
                journey=random.choice(journeys),
                setting=random.choice(settings),
                conflict=random.choice(conflicts),
                secret=random.choice(secrets),
                villain=random.choice(villains),
                event=random.choice(events)
            )
            # Add transition if not the last part
            if i < len(keywords) - 1:
                next_kw = keywords[i + 1]
                if next_kw in transitions:
                    transition = random.choice(transitions[next_kw]).format(
                        threat=random.choice(threats),
                        conflict=random.choice(conflicts),
                        journey=random.choice(journeys),
                        event=random.choice(events)
                    )
                    part += f" {transition}"
            plot_parts.append(part)
    
    # Combine parts (limit to 2 for brevity, add final keyword if 3)
    plot = " ".join(plot_parts[:2]) if len(plot_parts) > 1 else plot_parts[0]
    if len(plot_parts) == 3:
        plot += f" Their {keywords[-1]} drives a climactic {random.choice(events)}."
    
    plot = re.sub(r'\s+', ' ', plot).strip()
    return plot[:200] + "..." if len(plot) > 200 else plot

# Genre classifier with probabilities
def classify_genre(plot, keywords):
    X_new = vectorizer.transform([plot])
    probs = classifier.predict_proba(X_new)[0]
    genre_probs = sorted(zip(classifier.classes_, probs), key=lambda x: x[1], reverse=True)
    top_genres = [f"{genre} ({prob:.0%})" for genre, prob in genre_probs[:2]]
    # Bias toward keywords
    if "horror" in keywords:
        return top_genres[0] if "Horror" in top_genres[0] else f"Horror ({genre_probs[0][1]:.0%})"
    elif "love" in keywords:
        return top_genres[0] if "Romance" in top_genres[0] else f"Romance ({genre_probs[0][1]:.0%})"
    elif "travel" in keywords:
        return top_genres[0] if "Sci-Fi" in top_genres[0] else f"Sci-Fi ({genre_probs[0][1]:.0%})"
    return ", ".join(top_genres)

# Poster generator with stock image background
def generate_poster(title, keywords):
    # Use picsum.photos with keyword-based seed
    seed = keywords[0].lower() if keywords else "movie"
    try:
        response = requests.get(f"https://picsum.photos/seed/{seed}/400/600")
        img = Image.open(BytesIO(response.content)).convert('RGB')
    except:
        # Fallback to gradient if image fetch fails
        img = Image.new('RGB', (400, 600), color='black')
        draw = ImageDraw.Draw(img)
        for y in range(600):
            r = int(50 + (y / 600) * 100)
            g = int(50 + (y / 600) * 150)
            b = int(100 + (y / 600) * 155)
            draw.line((0, y, 400, y), fill=(r, g, b))
    
    draw = ImageDraw.Draw(img)
    # Dynamic font size based on title length
    title_len = len(title)
    font_size = 40 if title_len < 20 else 30 if title_len < 30 else 25
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    title = title.upper()
    draw.text((20, 50), title, font=font, fill=(255, 255, 255))
    
    # Add tagline
    taglines = ["A tale beyond the stars", "Love defies fate", "Terror awaits", "Journey into darkness"]
    tagline = random.choice(taglines).upper()
    try:
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        font_small = ImageFont.load_default()
    draw.text((20, 500), tagline, font=font_small, fill=(255, 255, 255))
    
    # Sanitize filename
    safe_title = re.sub(r'[^\w\s-]', '', title.lower().replace(' ', '_'))
    poster_path = os.path.join(r"C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62", f"poster_{safe_title}.png")
    try:
        img.save(poster_path)
        img.show()  # Preview poster
    except Exception as e:
        print(f"Error saving poster: {e}")
    return poster_path

# Save movie pitch to JSON
def save_pitch(title, keywords, plot, genre, poster_path):
    pitch = {
        "title": title,
        "keywords": keywords,
        "plot": plot,
        "genre": genre,
        "poster_path": poster_path
    }
    pitch_path = os.path.join(r"C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62", "movie_pitch.json")
    try:
        with open(pitch_path, "w", encoding="utf-8") as f:
            json.dump(pitch, f, indent=2)
    except Exception as e:
        print(f"Error saving pitch: {e}")
    return f"🎥 Title: {title}\n🧠 Keywords: {', '.join(keywords)}\n\n📜 Plot:\n{plot}\n\n🎯 Predicted Genre: {genre}\n\n🖼️ Poster saved to: {poster_path}"

# Main function
def main():
    keywords = input("Enter 2-3 keywords (comma-separated, e.g., time travel, robots, love): ").strip().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    if len(keywords) < 2 or len(keywords) > 3:
        print("Please provide 2-3 keywords!")
        return
    title = generate_title(keywords)
    plot = generate_plot(keywords)
    genre = classify_genre(plot, keywords)
    poster_path = generate_poster(title, keywords)
    pitch = save_pitch(title, keywords, plot, genre, poster_path)
    print("\n" + pitch)

if __name__ == "__main__":
    main()