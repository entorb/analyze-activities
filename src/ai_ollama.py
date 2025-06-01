"""Using Ollama local LLM AI model to analyze the data."""

import time
from pathlib import Path

# pip install ollama
from ollama import chat  # type: ignore

MODEL = "qwen3:latest"
# deepseek-r1:latest
# llama3.2:latest
# qwen3:latest
# mistral:latest


cont = Path("data/join.json").read_text()

time_start = time.time()
stream = chat(
    model=MODEL,
    messages=[
        {
            "role": "system",
            # "role": "user",
            # 5 data sources: Sleep data, sport activities, calendar entries,
            #  coding commits, personal journal.
            "content": """Create a text summary for my daily journal that I provide you in JSON format.
            Highlight the key events and activities.
            Take sleep data also into account.
            No daily breakdowns.
            Do not sum the minutes spend on activities.
            Do not count the coding tasks.
            Not interested in visualization of the data, just a text report.
            Reply in German
            """,  # noqa: E501
            # cspell: disable
            #             "content": """
            # Erstelle eine Text Zusammenfassung meiner Aktivitäten, die ich als JSON bereitstelle.  # noqa: E501
            # 4 verschiedenen Datenquellen:
            # - Schlaf, Sport, Kalendereinträge, Coding commits, Tagebuch
            # """,
            # cspell: enable
        },
        {"role": "user", "content": cont},
    ],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
print()

print(f"{round(time.time() - time_start)}s")
