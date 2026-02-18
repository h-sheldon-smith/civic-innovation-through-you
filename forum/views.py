from django.shortcuts import render

# Create your views here.
def Forum_Placeholder_View(request):
    some_state = "correct horse";
    return render(request, "forum/forum_placeholder.html", {"passed_state": some_state})