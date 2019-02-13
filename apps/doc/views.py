from django.shortcuts import render
from utils import json_status
from .models import Doc
from django.http import FileResponse
import requests


def index(request):
    docs = Doc.objects.filter(is_delete=False).all()
    return render(request, 'doc/docDownload.html', context={"docs": docs})


def download_doc(request):
    doc_id = request.GET.get("doc_id")
    doc = Doc.objects.filter(id=doc_id).first()
    if doc:
        file_path = doc.file_path
        res = FileResponse(requests.get(file_path))
        file_type = file_path.split('.')[-1]
        if file_type == 'jpg':
            res["Content-type"] = "image/jpeg"
        elif file_type == 'doc':
            res["Content-type"] = "application/msword"
        elif file_type == 'txt':
            res["Content-type"] = "text/plain"
        else:
            res["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        res["Content-Disposition"] = "attachment; filename={}".format(file_path.split('/')[-1])
        return res
    return json_status.params_error(message="文档不存在")
