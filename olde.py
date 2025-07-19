from dotenv import load_dotenv
""" Load environment variables from .env file. """
load_dotenv()  
from flask import Flask, render_template
import feedparser
import os
import together


""" Read the TogetherAI API key from the .env file. """
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


""" Read the feed limit from the environment file or set a default value """
FEED_LIMIT = int(os.getenv("FEED_LIMIT", "5"))  # Default to 5 articles


""" Check if the API key is provided. """
if not TOGETHER_API_KEY: 
    raise ValueError("Please provide your TogetherAI API key in the environment settings file.")


# Initialize the OpenAI client with the API key
# client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)


# def translate_text(input_text, target_language="fr"):
#     # Define the prompt for translation
#     prompt = "Translate the following English text into Shakespearean English"
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": prompt},
#             {"role": "user", "content": input_text},
#         ],
#     )
#     return response.choices[0].message.content


def translate_text(input_text):
    # Define the prompt for translation
    prompt = f"Translate the following English text into Shakespearean English using iambic pentameter:\n\n{input_text}"
    # Retrieve the response from the TogetherAI API
    response = together.Complete.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )
    # print("####  Together API response:", response)
    # Safeguard in case API structure isn't as expected
    try:
        return response["choices"][0]["text"].strip()
    except (KeyError, IndexError, TypeError) as e:
        # print("Error parsing Together API response:", e)
        # print("#### Full response:", response)
        return "[Translation unavailable]"


# def translate_feed(feed):
#     translated_feed = {}
#     #
#     # Translate feed title and description
#     translated_feed["title"] = translate_text(feed["title"])
#     translated_feed["description"] = translate_text(feed["description"])
#     translated_feed["link"] = feed["link"]
#     translated_feed["entries"] = []
#     #
#     # Translate and limit the number of entries in the feed
#     for entry in feed["entries"][:FEED_LIMIT]:
#         translated_entry = {
#             "title": translate_text(entry["title"]),
#             "summary": translate_text(entry["summary"]),
#         }
#         translated_feed["entries"].append(translated_entry)
#     return translated_feed


def translate_feed(feed):
    # Translate the feed’s identity (aka the feed's "title") and description
    # translate_feed = {
    #     "title": translate_text(feed["title"]),
    #     "description": translate_text(feed["description"]),
    #     "link": feed["link"],
    #     "entries": [],
    # }
    translated_feed = {
        "title": feed["title"], ## When this gets translated, it becomes an article summary or title; idk why.
        "description": feed["description"], ## When this gets translated, it becomes an article summary or description; idk why.
        "link": feed["link"],
        "entries": [],
    }
    # Translate each entry and limit the number of entries in the feed
    for entry in feed["entries"][:FEED_LIMIT]:
        translated_entry = {
            "title": translate_text(entry["title"]),
            "summary": translate_text(entry.get("summary", "")),
            "link": entry["link"],
        }
        translated_feed["entries"].append(translated_entry)
    return translated_feed


""" Define the Flask route to render the index page."""
@app.route("/")


def index():
    rss_feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
    feed = read_rss(rss_feed_url) ## aka feed_data
    translated_feed = translate_feed(feed)
    return render_template("index.html", feed=translated_feed)


def read_rss(feed_url):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    # Prepare the feed data
    feed_data = {
        "title": feed.feed.title,
        "description": feed.feed.description,
        "link": feed.feed.link,
        "entries": [],
    }
    # Limit the number of articles fetched
    for entry in feed.entries[:FEED_LIMIT]:
        entry_data = {
            "title": entry.title, 
            "summary": entry.get("summary", ""),
            "link": entry.link,
            }
        feed_data["entries"].append(entry_data)
    return feed_data


if __name__ == "__main__":
    app.run(debug=True)
