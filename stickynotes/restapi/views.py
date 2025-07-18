from django.shortcuts import render
from rest_framework.views import APIView
from restapi.serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework import status
from restapi.models import Note
from drf_yasg.utils import swagger_auto_schema
class NoteCR(APIView):
    @swagger_auto_schema(request_body=NoteSerializer)
    def post(self,request):
        ser = NoteSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"status":str(ser.data)},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":str(ser.errors)},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        try:
            note_list = Note.objects.all()
            serialized_note_list = NoteSerializer(note_list,many=True)
            return Response(serialized_note_list.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(serialized_note_list.errors,status=status.HTTP_400_BAD_REQUEST)        
class NoteUD(APIView):
        def put(self,request,id):
            toupdate_note = Note.objects.get(pk=id)
            ser = NoteSerializer(toupdate_note,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_200_OK)
            else:
                return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        def delete(self,request,id):
            try:
                Note.objects.get(pk=id).delete()
                return Response({"status":"selected item deleted"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"deletion process failed"},status=status.HTTP_400_BAD_REQUEST)
class SearchByTitle(APIView):
    def get(self,request,title):
        try:
            notes = Note.objects.filter(note_title__icontains=title)
            ser_notes = NoteSerializer(notes,many=True)
            return Response(ser_notes.data,status=status.HTTP_200_OK)
        except:
            return Response(ser_notes.errors,status=status.HTTP_400_BAD_REQUEST)
class SearchByContent(APIView):
    def get(self,request,content):
        try:
            notes = Note.objects.filter(note_body__icontains=content)
            ser_notes = NoteSerializer(notes,many=True)
            return Response(ser_notes.data,status=status.HTTP_200_OK)
        except:
            return Response(ser_notes.errors,status=status.HTTP_400_BAD_REQUEST)
class FilterByTags(APIView):
    def get(self,request,tag):
        try:
            notes = Note.objects.filter(note_tags__icontains=tag)
            ser_notes = NoteSerializer(notes,many=True)
            return Response(ser_notes.data,status=status.HTTP_200_OK)
        except:
            return Response(ser_notes.errors,status=status.HTTP_400_BAD_REQUEST)