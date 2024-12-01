from django.http import JsonResponse

from product import models


def set_user_token(request):
    token = request.COOKIES.get('user_token')

    if not token:
        anonim_user = models.AnonymousUser.objects.create()
        token = str(anonim_user.token)
        response = JsonResponse({'message': 'Yangi token yaratildi', 'token': token})
        response.set_cookie('user_token', token, max_age=60 * 60 * 24 * 30)
        return response

    return JsonResponse({'token': token})


def set_user_session(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    user = models.AnonymousUser.objects.filter(session=session_id).first()
    if user is None:
        user = models.AnonymousUser.objects.create(session=session_id)
    return session_id