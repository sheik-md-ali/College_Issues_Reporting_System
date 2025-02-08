from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from .models import Issue
from .serialnizers import IssueSerializer # type: ignore

@api_view(['GET'])
def get_issues(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data) 