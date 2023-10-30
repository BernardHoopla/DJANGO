import time
import pandas
from .slimstampen.spacingmodel import SpacingModel, Fact, Response


def add_facts(model, fact_file):
    fact_directory = "fact_data/"
    if fact_file[-4:] == ".csv":  # chinese
        data = pandas.read_csv(fact_directory + fact_file)
        questions = data["Chinese word"]
        answers = data["English translation"]
        for index in range(len(data)):
            fact = Fact(index + 1, questions[index], answers[index])
            model.add_fact(fact)
    elif fact_file[-5:] == ".xlsx":  # mandarin
        data = pandas.read_excel(fact_directory+fact_file)
        questions = data["Question"]
        answers = data["Answer"]
        for index in range(len(data)):
            fact = Fact(index + 1, questions[index], answers[index])
            model.add_fact(fact)
    else:
        facts = [["hello", "bonjour"], ["dog", "chien"], ["cat", "chat"], ["computer", "ordinateur"]]
        # facts = [["hai", "yes"], ["lie", "no"], ["sumimasen", "excuse me"], ["arigatoo gozaimas", "thank you"],
        #          ["tomodachi", "friend"], ["kazoku", "family"], ["kodomo", "children"], ["pan", "bread"],
        #          ["asa-gohan", "breakfast"], ["hiru-gohan", "lunch"], ["yoru-gohan", "dinner"]]
        for index in range(len(facts)):
            curr_fact = facts[index]
            fact = Fact(index + 1, curr_fact[0], curr_fact[1])
            model.add_fact(fact)


# TODO: turn into multiple functions to get correct pages
def learn_fact(model, session_start_time=0):
    cont = "y"
    orig_time = time.monotonic()
    while cont.lower() == "y":
        print("get fact time:", time.monotonic()-orig_time)
        next_fact, new = model.get_next_fact(current_time=time.monotonic()-orig_time)
        start_time = time.monotonic()
        if new:
            print(next_fact.question + " => " + next_fact.answer)
            answer = input("Type answer: ")
            corr = (next_fact.answer == answer)
        else:
            answer = input(next_fact.question + " => ").lower()
            corr = (next_fact.answer == answer)
        response_time = time.monotonic() - start_time  # TODO: make sure it is correct time step (s etc.)
        if not corr:
            print(f"Sorry, that response is wrong. \nThe correct answer is: '{next_fact.answer}'")
        elif not new:
            print("That answer is correct!")
        s_time = int((start_time-session_start_time)*1000)
        r_time = int(response_time*1000)
        # print(s_time, r_time, corr)
        resp = Response(fact=next_fact, start_time=s_time, rt=r_time, correct=corr)
        model.register_response(resp)
        print("Print Facts:")
        for f in model.facts:
            print(f, model.calculate_activation(start_time + model.LOOKAHEAD_TIME, f))
        print("\n")
        # print(next_fact, model.calculate_activation(42000 + model.LOOKAHEAD_TIME, next_fact))
        if not new:
            cont = input("Learn next fact? [y/n]\n")
