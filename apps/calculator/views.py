from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from apps.calculator.models import CalculatorQuestion
from apps.calculator.services import recommend_products


def _collect_answers(data) -> dict:
    answers = {}
    for key in ('strength', 'format', 'country', 'budget'):
        if key in data:
            answers[key] = data.get(key, '')
    return answers


@require_GET
def calculator_results(request):
    """HTMX-підбір для блоку на головній. Повна сторінка → редірект на #home-calculator."""
    answers = _collect_answers(request.GET)
    if not request.htmx:
        return redirect('/#home-calculator')

    hits = recommend_products(answers) if answers else []
    return render(request, 'calculator/partials/results.html', {
        'hits': hits,
        'results': [h.product for h in hits],
        'answers': answers,
    })


@require_http_methods(['GET', 'POST'])
def calculator_page(request):
    """Залишено для зворотної сумісності старих посилань."""
    return redirect('/#home-calculator')


def calculator_api(request):
    """JSON endpoint for mobile/bot."""
    questions = []
    for q in CalculatorQuestion.objects.filter(is_active=True).prefetch_related('options'):
        questions.append({
            'step': q.step_key,
            'title': q.title,
            'options': [
                {
                    'label': o.label,
                    'value': o.value,
                    'filter_field': o.filter_field,
                    'filter_value': o.filter_value,
                }
                for o in q.options.filter(is_active=True)
            ],
        })
    return JsonResponse({'questions': questions})
