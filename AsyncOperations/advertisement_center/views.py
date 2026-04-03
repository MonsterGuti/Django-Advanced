from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from advertisement_center.forms import CommercialForm
from advertisement_center.models import Commercial
from advertisement_center.tasks import enqueue_video_processing
from advertisement_center.utils import status_counts, running_tasks, get_queue_sizes


def index(request):
    # Обединяваме списъка с реклами и статистиката за статусите в един контекст
    context = {
        'commercials': Commercial.objects.all(),
        **status_counts()
    }
    return render(request, 'advertisement_center/commercial_list.html', context)


def create_commercial(request):
    form = CommercialForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            commercial = form.save()
            # Използваме on_commit, за да сме сигурни, че обектът е в DB преди Celery да го поеме
            transaction.on_commit(lambda: enqueue_video_processing(commercial.pk, 'heavy'))
            messages.success(request, 'Commercial saved and sent to heavy queue')
            return redirect('advertisement_center:index')

    context = {'form': form}
    return render(request, 'advertisement_center/commercial_form.html', context)


def refresh_slogan(request, pk: int):
    if request.method == "POST":
        commercial = get_object_or_404(Commercial, pk=pk)
        try:
            # Тук пращаме към "леката" опашка за бърза обработка
            enqueue_video_processing(commercial.pk, 'light')
            messages.info(request, 'Slogan refresh queued on the light worker')
        except Exception as exc:
            messages.error(request, f'Unable to update slogan: {exc}')
    return redirect('advertisement_center:index')


def task_monitor(request):
    context = {
        'running_tasks': running_tasks(),
        'queue_sizes': get_queue_sizes(),
        **status_counts(),
    }
    return render(request, 'advertisement_center/task_monitor.html', context)