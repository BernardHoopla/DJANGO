from example.slimstampen.spacingmodel import SpacingModel
from example.slimstampen_utility_functions import add_facts


class Info:
    # session info
    session_length = 0
    session_start_time = None
    session_end_time = None
    correct_answer = 0
    wrong_answer = 0

    # model info within session
    model = None
    curr_fact = None
    start_time = False
    end_time = False
    correct = False

    # how often leaderboard toggled
    toggled = 0
