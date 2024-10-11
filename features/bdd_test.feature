# language: ru

Функционал: Создание игры, возможность обновит счёт, получить список вариантов ответов, начать следующий раунд...

    Сценарий: Обновление счёта
        Дано счёт игры [1, 1, 2]
        Когда вызвана функция обновления счёта на [1, 0, 0]
        Тогда результатом должно быть [2, 1, 2]

    Сценарий: Переход к следующему раунду
        Дано идущая игра
        Когда запрашивается переход к следующему раунду
        Тогда результат должен быть: Игра с новыми вариантами ответов и новым треком

    Сценарий: Получение пути к аудио файлу
        Дано идущая игра, загадан трек "Title-Author.mp3"
        Когда запрашивается путь к файлу
        Тогда результат должен быть "Путь к файлу с фрагментом 'resources/out.mp3'"

    Сценарий: Получение верного отвера
        Дано идущая игра с правильным ответом "Title-Author"
        Когда запрошен правильный ответ
        Тогда должно выводится "Title-Author"

    Сценарий: Запрос вариантов ответов
        Дано идущая игра с ответами ["1. ...", "2. ...", "3. ...", "4. ..."]
        Когда запрашивается список ответов
        Тогда результатом должен быть список ["1. ...", "2. ...", "3. ...", "4. ..."]

