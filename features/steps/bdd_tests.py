from behave import given, when, then
from main import Game
import os.path

@given('счёт игры [{score1:d}, {score2:d}, {score3:d}]')
def step_impl(context, score1, score2, score3):
    context.game = Game()
    context.game.scores = [score1, score2, score3]

@when('вызвана функция обновления счёта на [{update1:d}, {update2:d}, {update3:d}]')
def step_impl(context, update1, update2, update3):
    context.result = context.game.update_score([update1, update2, update3])

@then('результатом должно быть [{expected1:d}, {expected2:d}, {expected3:d}]')
def step_impl(context, expected1, expected2, expected3):
    assert context.game.scores == [expected1, expected2, expected3]
    assert context.result == context.game.scores

@given('идущая игра')
def step_impl(context):
    context.game = Game()
    context.initial_variants = context.game.current_variants.copy()
    context.initial_solution = context.game.current_solution

@when('запрашивается переход к следующему раунду')
def step_impl(context):
    context.game.next_task()

@then('результат должен быть: Игра с новыми вариантами ответов и новым треком')
def step_impl(context):
    assert context.game.current_variants != context.initial_variants
    assert context.game.current_solution != context.initial_solution

@given('идущая игра, загадан трек "{track}"')
def step_impl(context, track):
    context.game = Game()
    context.game.current_solution = track

@when('запрашивается путь к файлу')
def step_impl(context):
    context.result = context.game.get_music_file()

@then('результат должен быть "Путь к файлу с фрагментом \'{track}\'"')
def step_impl(context, track):
    assert os.path.exists(context.result)
    assert track in context.result

@given('идущая игра с правильным ответом "{answer}"')
def step_impl(context, answer):
    context.game = Game()
    context.game.current_solution = answer

@when('запрошен правильный ответ')
def step_impl(context):
    context.result = context.game.get_solution()

@then('должно выводится "{expected}"')
def step_impl(context, expected):
    assert context.result == expected

@given('идущая игра с ответами {answers}')
def step_impl(context, answers):
    context.game = Game()
    context.game.current_variants = eval(answers)

@when('запрашивается список ответов')
def step_impl(context):
    context.result = context.game.get_answers()

@then('результатом должен быть список {expected}')
def step_impl(context, expected):
    assert context.result == eval(expected)
