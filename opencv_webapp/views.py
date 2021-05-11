from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import SimpleUploadForm, ImageUploadForm
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})
    # html 경로 중요
    # opencv_webapp\templates\opencv_webapp\first_view.html

def simple_upload(request):
    if request.method == 'POST': # 사용자가 form 태그 내부의 submit 버튼을 클릭하여 데이터를 제출했을 시
        form = SimpleUploadForm(request.POST, request.FILES) # 빈 양식을 만든 후 사용자가 업로드한 데이터를 채워, 채워진 양식을 만듦
        if form.is_valid(): # form이 문제가 없다면
            myfile = request.FILES['image'] # 'image' : HTML input tag의 name attribute의 값
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # 업로드된 이미지의 경로명 & 이미지 파일 객체 자체
            uploaded_file_url = fs.url(filename)
            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else: # request.method == 'GET'
        form = SimpleUploadForm() # 빈 양식
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)

def detect_face(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES) # filled form
        if form.is_valid(): # form이 문제가 없다면
            post = form.save(commit=False) # commit=False: 임시저장 -> Form에 채워진 데이터를 DB에 실제로 저장하기 전에 데이터 변경, 추가 가능
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장
            # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (record 1건에 해당)
            imageURL = settings.MEDIA_URL + form.instance.document.name # == post.docuement.url
            # settings.MEDIA_URL: '/media/'
            # form.instance.document.name: /images/2021/05/10/xxx.jpg
            # imageURL: /media/images/2021/05/10/xxx.jpg == post.docuement.url
            # document: ImageUploadModel Class에 선언되어 있는 “document”에 해당
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 경로를 받아서 저장하는 함수
            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)

    else: # request.method == 'GET'
         form = ImageUploadForm() # empty form
         return render(request, 'opencv_webapp/detect_face.html', {'form':form})
