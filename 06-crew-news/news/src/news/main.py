#!/usr/bin/env python
import sys
import requests
import warnings
import os
from datetime import datetime

from news.crew import NewsPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the research crew.
    """
    resp = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=UTC")
    dt = datetime.fromisoformat(resp.json()["dateTime"])

    current_date = dt.strftime("%B %Y")   # → "February 2026"
    print(current_date)

    inputs = {
        'sector': 'crewai framework',
        'current_date': current_date
    }

    # Create and run the crew
    result = NewsPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()