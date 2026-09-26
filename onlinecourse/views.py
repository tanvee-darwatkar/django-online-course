from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Submission, Choice, Question

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        selected_ids = request.POST.getlist('choice')
        
        for choice_id in selected_ids:
            choice = Choice.objects.get(id=int(choice_id))
            submission.choices.add(choice)
            
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = [choice.id for choice in submission.choices.all()]
    total_score = 0
    grade = 0
    
    for question in course.question_set.all():
        total_score += question.grade
        if question.is_get_score(selected_ids):
            grade += question.grade
            
    context['course'] = course
    context['grade'] = grade
    context['total_score'] = total_score
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)