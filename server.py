import random
import requests
from ok_api import OkApi, Upload
import vk_api
import os
from configparser import ConfigParser
from flask import Flask, flash, request, redirect, url_for
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
upload_folder = 'photos'
config = ConfigParser()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
vkPhotoReady = False
app = Flask( 
	__name__,
	template_folder='templates',  
	static_folder='static' 
)
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = "IDFSD"
@app.route('/') 
def base_page():
	return '12312312312'
@app.route('/upload', methods=['GET', 'POST']) 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login',methods=["GET", "POST"])
def log_in():
  global config
  with open("settings.ini", "r") as cfg:
    if request.headers.get('social') == "vk":
      config.set('Settings','vklogin', request.headers.get("vklogin"))
      config.set('Settings','vkpassword', request.headers.get("vkpassword"))
      config.set('Settings', 'vktoken', request.headers.get("vktoken"))
    else:
      config.set('Settings', 'okaccess', request.headers.get("okaccess"))
      config.set('Settings', 'okappkey', request.headers.get("okappkey"))
      config.set('Settings', 'oksecret', request.headers.get("oksecret"))
      config.write(cfg)
  
def keys(social): 
  config.read("settings.ini")
  if social == "vk":
      return [config.get("Settings","vklogin"),config.get("Settings","vkpassword"),config.get("Settings","vktoken")]
  else:
    return [config.get("Settings","okaccess"),config.get("Settings","okappkey"),config.get("oksecret")]
                                                            
@app.route('/upload_to_server', methods=['GET', 'POST'])
def upload_file():
      global vkPhotoReady
      if 'file' not in request.files:
        print(request.files)
        return "WFT" #wrong file type
      file = request.files['file']
      if file.filename == '':
        print("nf")
        return "NF" #no file
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          vkPhotoReady = True
          return 'S'

          
def symbols_limit(limit):
  symbols = 0
  for _ in msg_text:
    symbols += 1
    if symbols > limit:
      return True
    else:
      return False


@app.route('/api',methods=['GET','POST'])
def get_info():
  global vkPhotoReady, msg_text
  social = request.headers.get("Social")
  action = request.headers.get("Action")
  if "vk" in social:
    sss = keys("vk")
    user_login=sss[0]
    user_password=sss[1]
    token = sss[2]
    vk_s = vk_api.VkApi(token=token,scope='wall', app_id=51486776,login=user_login, password=user_password)
    vk_s.auth()
    vk = vk_s.get_api()
    try:
      ownerid = "-" + request.headers.get("id")
    except:
      ownerid = vk.users.get()[0]["id"]
    last_post = vk.wall.get(owner_id=ownerid)["items"][0]["id"]
    try:
      msg_text = request.headers.get("MsgText")
    except:
      pass
    if action == "post":
      if vkPhotoReady:
        upload_url = vk_api.photos.getWallUploadServer(group_id=ownerid)['upload_url']
        with open("/photos") as skazhite_photo:
          request1 = requests.post(upload_url, files={'photo': open(os.listdir()[0], "rb")})
          request1 = json.loads(request.text)
          request1 = vk.method('photos.saveWallPhoto', {'photo': request1['photo'], 'server': request1['server'], 'hash': request1['hash']})
          #attachments = 'photo{}_{}'.format(OWNER_ID, rs[0]['id'])
          vk.wall.post(owner_id=ownerid,message=msg_text, attachments=f"photo{ownerid}_{request1[0]['id']}")
          vkPhotoReady = False
          os.remove(f"files/{os.listdir[0]}")
          return "S"
      else:
        vk.wall.post(owner_id=ownerid,message=msg_text)
        return "S"
    elif action == "posts":
      ea_sports = vk.wall.get(owner_id=ownerid)
      return ea_sports["response"]["items"][0]["text"]
    elif action == "edit":
      vk.wall.edit(owner_id=ownerid, post_id=last_post, message = msg_text)
      return "S"
    elif action == "delete":
      try:
        vk.wall.delete(owner_id=ownerid, post_id=last_post)
        return "S"
      except:
        return "F"
    elif action == "last_post_text":
      return vk.wall.get(owner_id=ownerid)["items"][0]["text"]
    elif action == "modergroups":
      aye = {}
      for group in vk.groups.get(user_id=ownerid,filter="editor")["response"]["items"]:
        aye[group["id"]] = group["name"]
      return aye
  elif "ok":
    ok = OkApi(access_token=keys("ok")[0],
               application_key=keys("ok")[1],
               application_secret_key=keys("ok")[2])

    upload = Upload(ok)
    files_photo = []
    files_video = []
    for i in os.listdir('files'):
      if i.rsplit('.', 1)[1].lower() in ["png","jpeg","jpg"]:
        files_photo.append(i)
    upload_response = upload.photo(photos=files_photo)
    for i in os.listdir('files'):
      if i.rsplit('.', 1)[1].lower() in ["png","jpeg","jpg"]:
        os.remove(f'files/{i}')
    for photo_id in upload_response['photos']:
        token = upload_response['photos'][photo_id]['token']
        response = ok.photosV2.commit(photo_id=photo_id, token=token)
    for i in os.listdir('files'):
      if i.rsplit('.', 1)[1].lower() == "mp4":
        files_video.append(i)
    for vidos in files_video:
      upload_response = upload.video(video=vidos, file_name=vidos[:-4])
  
      response = ok.video.update(vid=upload_response['video_id'], title='VideoTitle')
      print(response)
      for i in os.listdir('files'):
        if i.rsplit('.', 1)[1].lower() == "mp4":
          os.remove(f'files/{i}')
  if action == "delete":
    pass
    
if __name__ == "__main__":
	app.run( 
		host='0.0.0.0',  
		port=random.randint(2000, 9000)
	)