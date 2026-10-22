import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task

def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date_str = request.POST.get("due_date")

        print("--- 1. 受け取った文字列:", repr(due_date_str))

        due_date = None
        if due_date_str:
            try:
                naive_dt = datetime.datetime.fromisoformat(due_date_str)
                due_date = timezone.make_aware(naive_dt, timezone.get_current_timezone())
                print("--- 2. 変換成功した due_date:", due_date)
            except Exception as e:
                print("--- 日時変換エラー発生:", type(e), e)
                due_date = None

        print("--- 3. データベースに保存する直前の due_date:", due_date)

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date
            )

        return redirect("index")

    tasks = Task.objects.all().order_by("completed", "due_date")

    return render(
        request,
        "app/index.html",
        {"tasks": tasks}
    )


def complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect("index")


def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("index")