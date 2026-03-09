#!/usr/bin/env python
import os
import warnings

from datetime import datetime
from engineering_team.crew import Homework
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# def run(grade: str, to_email: str):
def run():
    """
    Run the crew.
    """
    print("#### in run()")
    inputs = {
        'grade': 'Three',
        'to_email': 'sushobhanmondal@gmail.com',
        'topic': 'simple fractions'
    }
    
    try:
        result = Homework().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()