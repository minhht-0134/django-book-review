from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.forms.models import model_to_dict

from ..models import Activity

def activities(request):
  user_id = request.POST.get('user_id') or request.user.id

  target_object_type = request.POST.get('target_object_type')
  if target_object_type == 'user':
    target_object_type_id = ContentType.objects.get(
      app_label='auth', model='user').id
  else:
    target_object_type_id = ContentType.objects.get(
      app_label='books', model=target_object_type).id

  target_object_id = request.POST.get('target_object_id')
  content = request.POST.get('content')
  status = request.POST.get('status')
  action_type = request.POST.get('action_type')

  activity = Activity(
    user_id=user_id,
    target_object_id=target_object_id,
    target_object_type_id=target_object_type_id,
    action_type=action_type,
    content=content,
    status=status,
  )
  activity.save()

  return JsonResponse({ **model_to_dict(activity), 'status_text': activity.status_text() })

def activitiesChange(request, pk):
  activity = Activity.objects.get(pk=pk)

  activity.content = request.POST.get('content') or activity.content
  activity.status = request.POST.get('status') or activity.status
  activity.action_type = request.POST.get('action_type') or activity.action_type
  activity.save()

  return JsonResponse({ **model_to_dict(activity), 'status_text': activity.status_text() })

def activitiesDelete(request, pk):
  activity = Activity.objects.get(pk=pk)

  activityChildren = Activity.objects.filter(
    target_object_id=activity.id,
    target_object_type_id=ContentType.objects.get(app_label='books', model='activity').id,
  )

  if activityChildren is not None: activityChildren.delete()

  activity.delete()

  return JsonResponse({})
