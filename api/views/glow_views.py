from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.glow import Glow
from ..serializers import GlowSerializer, UserSerializer

# Index Glows - show all the glows that belong to the board/:id
# Create Glows
class Glows(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GlowSerializer
    def get(self, request, board_id):
        """Index request"""
        # Get all the glows on the board
        glows = Glow.objects.filter(board_id=board_id)

        data = GlowSerializer(glows, many=True).data
        return Response({ 'glows': data })

    def post(self, request, board_id):
      """Create request"""
      # Add owner to request data object 'glow'
      request.data['glow']['owner'] = request.user.id
      request.data['glow']['board_id'] = board_id
      # Serialize/ Create board
      glow = GlowSerializer(data=request.data['glow'])

      if glow.is_valid():
          glow.save()
          return Response({ 'glow': glow.data }, status=status.HTTP_201_CREATED)
      return Response(glow.errors, status=status.HTTP_400_BAD_REQUEST)

class GlowDetail(generics.RetrieveUpdateDestroyAPIView):
    # def get(self, request, pk):
    def get(self, request, pk):
      """Show request"""
      glow = get_object_or_404(Glow, pk=pk)
      # glow = Glow.objects.filter(board_id=board_id, pk=pk)

      # glow = get_object_or_404(Glow, pk=pk)

      data = GlowSerializer(glow).data
      return Response({ 'glow': data })

    def delete(self, request, pk):
      """Delete request"""
      glow = get_object_or_404(Glow, pk=pk)
      if not request.user.id == glow.owner.id:
        raise PermissionDenied('Unauthorized, you do not own this glow')
      glow.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
      """Update Request"""
      if request.data['glow'].get('owner', False):
          del request.data['glow']['owner']

      glow = get_object_or_404(Glow, pk=pk)
      if not request.user.id == glow.owner.id:
          raise PermissionDenied('Unauthorized, you do not own this glow')

      request.data['glow']['owner'] = request.user.id
      data = GlowSerializer(glow, data=request.data['glow'])
      if data.is_valid():
          data.save()
          return Response(status=status.HTTP_204_NO_CONTENT)
      return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
