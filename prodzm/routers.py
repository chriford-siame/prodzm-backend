from rest_framework.routers import DefaultRouter

# from prodzm.restful_api.viewsets  import (
#     AnswerViewSet,
#     QuestionViewSet,
#     ReportViewSet,
#     UserProfileViewSet,
# )

router = DefaultRouter()
# router.register(r'users', UserProfileViewSet, basename='user')

app_name = 'prodzm'
urlpatterns = router.urls
