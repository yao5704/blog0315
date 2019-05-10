from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .form import CommentForm


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('blog0315:index'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        # comment_form.cleaned_data['text']处理
        body = comment_form.cleaned_data['text']
        # body = body[3:]
        # body_count = len(body)
        # body1 = body[:body_count - 4]
        # body2 = body[body_count:]
        # body = body1 + body2
        #
        comment.text = body
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
    else:
        #return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)