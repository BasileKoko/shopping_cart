from rest_framework.response import Response
from rest_framework.views import APIView


class ItemView(APIView):

    def get(self, request):
        msg = 'I am working'
        return Response(msg)
