# example/views.py
import random
import time
from datetime import datetime

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import UserInputForm, InputForm
from .slimstampen.spacingmodel import SpacingModel, Response
from .slimstampen_utility_functions import add_facts
from .info import Info

from .models import Leaderboard
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # now = datetime.now()
    participant_id = 0  # TODO: update from model/login
    model = SpacingModel()
    add_facts(model, "33-chinese-words.csv")
    fact = model.get_next_fact(0)
    num_facts = len(model.facts)

    context = {}
    context['first_question'] = fact[0].question
    context['first_answer'] = fact[0].answer
    context['num_questions'] = num_facts
    context['participant_nr'] = participant_id
    context['form'] = InputForm()
    return render(
        request,
        'home.html',
        context
    )


def choose_session(request):
    # choose session length
    session_length = 2  # Time in minutes
    Info.session_length = session_length * 60 * 1000
    Info.session_start_time = False

    # start the session
    model = SpacingModel()
    add_facts(model, "33-chinese-words.csv")

    Info.model = model
    Info.correct_answer = 0
    Info.wrong_answer = 0
    Info.toggled = 0
    return render(request, 'session/choose_session.html', {})


# def result_view(request):


def session_view(request):
    # Calculate when start/end session
    if not Info.session_start_time:
        Info.session_start_time = int(time.monotonic()) % 1000 * 1000
        Info.session_end_time = Info.session_start_time + Info.session_length

    model = Info.model
    # SAVE PREVIOUS RESPONSE
    if Info.end_time and Info.end_time > Info.start_time:
        rt = int(Info.end_time - Info.start_time)
        response = Response(fact=Info.curr_fact[0], start_time=Info.start_time, rt=rt, correct=Info.correct)
        model.register_response(response)

    # CHECK ANSWER
    if request.method == 'POST':
        curr_time = int(time.monotonic()) % 1000 * 1000
        Info.end_time = curr_time
        fact = Info.curr_fact

        form = UserInputForm(request.POST)
        if form.is_valid():
            # Check that answer is correct
            user_input = form.cleaned_data['text_input']
            correct = False
            if user_input.lower() == fact[0].answer:
                correct = True
                Info.correct_answer += 1
            else:
                Info.wrong_answer += 1

            answer = f"That is wrong :(\nThe correct answer is {fact[0].answer}."
            if correct:
                answer = "That is correct!"

            Info.correct = correct
            return render(request, 'session/result.html', {'form': form, 'answer': answer,
                                                           'leaderboard': create_leaderboard()})
    # SESSION TIME OVER
    if Info.session_end_time <= int(time.monotonic()) % 1000 * 1000:
        return render(request, 'session/session_end.html', {'correct': Info.correct_answer, 'wrong': Info.wrong_answer,
                                                            'leaderboard': create_leaderboard()})

    # QUESTION
    curr_time = int(time.monotonic()) % 1000 * 1000
    start_time = curr_time
    Info.start_time = start_time
    fact = model.get_next_fact(current_time=int(start_time))
    Info.curr_fact = fact
    question = fact[0].question

    form = UserInputForm()
    # NEW FACT to learn
    if fact[1]:
        return render(request, 'session/learn_fact.html', {'form': form, 'question': question, 'answer': fact[0].answer,
                                                           'leaderboard': create_leaderboard()})
    return render(request, 'session/session_leaderboard.html', {'form': form, 'question': question,
                                                                'leaderboard': create_leaderboard()})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request)
            return redirect('start_session')  # Redirect to the "start_session" page after successful login
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def input_form(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['text_input']
            print(user_input)
            # TODO: If you want to save the input to the database (optional)
            # user = UserInput(text_input=user_input)
            # user.save()
            return render(request, 'result.html', {'user_input': user_input})
    else:
        form = UserInputForm()
    return render(request, 'input_form.html', {'form': form})


def create_leaderboard():
    group_names = ["Blue Guppies", "Red Pandas", "Green Gnomes", "Yellow Parakeets"]
    leaderboard = [(name, random.randint(50, 100)) for name in group_names]
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard


def leaderboard_view(request):
    # leaderboard = Leaderboard.objects.all()
    # leaderboard = [(entry.player_name, entry.score) for entry in leaderboard]
    group_names = ["Blue Guppies", "Red Pandas", "Green Gnomes", "Yellow Parakeets"]
    leaderboard = [(name, random.randint(50, 100)) for name in group_names]
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})

@csrf_exempt
def toggle_leaderboard(request):
    if request.method == 'POST':
        visible = request.POST.get('visible')  # Get the visibility state from the request
        # Process the visibility information as needed (e.g., store it in the database)
        # You can add your custom logic here
        response_data = {'message': 'Toggle event received.'}
        print("VISIBILITY:", visible)
        Info.toggled += 1
        return JsonResponse(response_data)
    return JsonResponse({'message': 'Invalid request.'})
