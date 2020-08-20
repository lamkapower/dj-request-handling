from collections import Counter

from django.shortcuts import render_to_response

from django.http import HttpResponse

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if request.GET['from-landing'] == 'original':
        counter_click['original'] += 1
        return render_to_response('index.html')
    if request.GET['from-landing'] == 'test':
        counter_click['test'] += 1
        return render_to_response('index.html')
    else:
        return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    if request.GET.get('ab-test-arg', 'original') == 'original':
        counter_show['original'] += 1
        return render_to_response('landing.html')
    elif request.GET.get('ab-test-arg', 'original') == 'test':
        counter_show['test'] += 1
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    total_show_original = counter_show['original']
    total_click_original = counter_click['original']
    total_show_test = counter_show['test']
    total_click_test = counter_click['test']
    try:
        original_conversion = total_click_original / total_show_original
        test_conversion = total_click_test / total_show_test
    except ZeroDivisionError:
        return HttpResponse('Количество просмотров = 0')
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
