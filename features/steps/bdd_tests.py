from behave import given, when, then
from main import Game
import main
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


@given('идущая игра, ход игрока 1')
def step_impl(context):
    context.app = main.QApplication([])
    context.window = main.MainWindow()


@when('игрок даёт правильный ответ и нажимает на кнопку ответить')
def step_impl(context):
    _index = context.window.game.current_variants.index(context.window.game.get_solution())
    context.window.answers[_index].setChecked(True)
    context.window.submit()


@then('Счёт игры изменяется')
def step_impl(context):
    assert context.window.game.scores == [1, 0, 0]


@when('игрок даёт неправильный ответ и нажимает на кнопку ответить')
def step_impl(context):
    _index = context.window.game.current_variants.index(context.window.game.get_solution())
    context.window.answers[(_index + 1) % 3].setChecked(True)
    context.window.submit()


@then('Счёт игры не изменяется и ход переходит к игроку 2')
def step_impl(context):
    assert context.window.game.scores == [0, 0, 0]
    assert context.window.current_player == 1


@when('игрок даёт правильный ответ и нажимает на кнопку ответить, а затем завершает игру')
def step_impl(context):
    _index = context.window.game.current_variants.index(context.window.game.get_solution())
    context.window.answers[(_index + 1) % 3].setChecked(True)
    context.window.submit()
    context.window.end_game()


@then('Счёт игры изменяется, игрок 1 занимает 1 место')
def step_impl(context):
    assert str(context.window.end_of_game.labels[0].text()).startswith("User1")
