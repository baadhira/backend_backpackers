from email import charset
from urllib import response
from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data,accepted_media_type=None,renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            reponse = json.dumps({'errors':data})
        else:
            reponse = json.dumps(data) 
        return reponse   