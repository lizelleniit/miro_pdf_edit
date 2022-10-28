# import module
import requests
from PIL import Image
import json
import io
import urllib3
import os
from os.path import exists
import re
import config
from collections import namedtuple
import math

def is_object_on_board(board_id,miro_authorisation,info_tuple):
      
      miro_id_type = type(info_tuple['miro_id'])
      if miro_id_type==str:
            if info_tuple['miro_id']=='':
                  info_tuple['miro_id']=None
            else:
                  info_tuple['miro_id']=int(info_tuple['miro_id'])

      if info_tuple['miro_id'] is None or math.isnan(info_tuple['miro_id']):
            exists = False
      else:
            miro_id=info_tuple['miro_id']
            
            # check if perhaps the id is in object_dict but the item has been deleted from Miro
                        

            url = "https://api.miro.com/v2/boards/"+str(board_id)+"/items/"+str(miro_id)
                        
            headers = {
                  "Accept": "application/json",
                  "Authorization": "Bearer "+miro_authorisation
            }

            response_url_lookup = requests.get(url, headers=headers)
            # todo: double check that there's always a 'message' that miro sends along with 'status'
            if 'status' in response_url_lookup.json().keys():
                  # probably a miro error
                  if response_url_lookup.json()['status']==404:
                        print('Miro cannot find item '+str(info_tuple['name'])+' on Miro. This may be because someone has deleted it. ')
                        exists = False
                        
                  else:
                        
                        print(f"Miro has returned error message {response_url_lookup.json()['message']}")
                        exists = False
                        
                        raise Exception('ending here')
            else:
                  
                  miro_id = response_url_lookup.json()['id']
                  

                  headers = {
                        "Accept": "application/json",
                        "Authorization": "Bearer "+miro_authorisation
                  }
                  
                  ids_on_board=[]
                  cursor=""
                  while True:
                        # miro-enforced limit is 50
                        url = "https://api.miro.com/v2/boards/"+str(config.board_id)+"/items?limit=50&cursor="+cursor 
                        response_item_list = requests.get(url, headers=headers)
                        for item in response_item_list.json()['data']:
                              ids_on_board.append(item['id'])
                        if 'cursor' in response_item_list.json().keys():
                              cursor=response_item_list.json()['cursor']
                        else:
                              break

                  if miro_id in ids_on_board:
                        #print(f'the object with id {miro_id} exists.')
                        exists = True
                  else:
                        #print(f'the object with id {miro_id} does not exist.')
                        exists = False
                  # the image exists
                  

      return exists


def make_or_update_miro(headers,payload,obj_data,object_name,make_new=False):
      info_tuple=obj_data[object_name]
      exists = is_object_on_board(config.board_id,config.miro_authorisation,info_tuple)
      if exists == False:
            url = "https://api.miro.com/v2/boards/"+str(config.board_id)+"/"+obj_data[object_name]['obj_type']
            response = requests.post(url, json=payload, headers=headers)
            
            
            info_tuple['miro_id']=response.json()['id']
      elif exists==True:
            miro_id = info_tuple['miro_id']
            url = "https://api.miro.com/v2/boards/"+str(config.board_id)+"/"+obj_data[object_name]['obj_type']+"/"+str(miro_id)
            response = requests.patch(url, json=payload, headers=headers)           
      obj_data[object_name]=info_tuple

      return obj_data

def make_or_update_frame_miro(obj_data,frame_name,miro_authorisation,position,size,make_new=False):

      
      if frame_name in obj_data.keys():
            print(f"Frame {frame_name} exists in obj_data dict.")

            
            
            
      else:
            print(f"Frame {frame_name} does not exist in obj_data dict. We need to add the frame to the dict first.")
            
            obj_data[frame_name]={'name':frame_name,'board_id': config.board_id,'children':[],'miro_id':None,'position':position,'size':size,'style':None,'obj_type':'frames'}

      info_tuple = obj_data[frame_name]
      headers = {
                        "Accept": "*/*",
                        "Content-Type": "application/json",
                        "Authorization": "Bearer "+miro_authorisation
            }      
      payload = {
                  "data": {
                        "format": "custom",
                        "title": frame_name,
                        "type": "freeform"
                  },
                  "position": {
                        "origin": "center",
                        "x": info_tuple['position'][0],
                        "y": info_tuple['position'][1]
                  },
                  "geometry": {
                        "width": info_tuple['size'][0],
                        "height": info_tuple['size'][1]
                  },
                  'style': {
                        'fillColor': '#FFFFFF',

                  }
            }    
      
      # we now know the frame is recorded in obj_data, but is it on miro? 
      
      obj_data = make_or_update_miro(headers,payload,obj_data,frame_name,make_new=make_new)  
      
      return obj_data


def upload_img_miro(file_path,board_id,parent,position=None,size=None):
      url='https://api.miro.com/v2/boards/'+str(config.board_id)+'/images' 
      
      headers = {
                        "Authorization": "Bearer "+config.miro_authorisation
                  }
      payload={}
      payload['parent']=parent
      payload["position"] = {
                              "origin": "center",
                              "x": position[0],
                              "y": position[1]
                  }
      
      payload['geometry'] = {
                  "width": size[0],
      }
      imageFile = {'resource': (file_path, open(file_path, 'rb'), 'image/jpg'),'data': (None, json.dumps(payload), 'application/json')}

      response = requests.post(url, headers=headers, files=imageFile)

      print(response.json())
      if 'message' in response.json().keys():
            print('Response from Miro: ',response.json()['message'])
      if 'id' not in response.json().keys():
            print(f'Miro did not manage to upload the image. Is it possible that the path {file_path} does not exist?')
            return
      else:
            item_id = response.json()['id']
      
      return item_id

def update_img_miro(file_path,board_id,parent,item_id,size=None,position=None):
      url = "https://api.miro.com/v2/boards/"+str(board_id)+"/images/"+str(item_id)
      
      payload={}
      payload["parent"]=parent
      payload["data"] = {
                                    "title": "randomtitle",
                                    "url": file_path
                                    }
            
      payload["position"] = {
                              "origin": "center",
                              "x": position[0],
                              "y": position[1]
                  }
            
      payload['geometry'] = {
                  "width": size[0],
            }

      headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer "+miro_authorisation
      }

      response = requests.patch(url, json=payload, headers=headers)
      
      
def make_or_update_img_miro(file_path,board_id,parent,object_name,obj_data,position,size):
      #print('Creating or updating figure',fig_name)
      info_tuple = obj_data[object_name]
      exists = is_object_on_board(board_id,miro_authorisation,info_tuple)
      if exists==False:
            miro_id = upload_img_miro(file_path,board_id,parent,position=position,size=size)
            if object_name not in obj_data.keys():
                  obj_data[object_name]={}
            obj_data[object_name]['miro_id']=miro_id
      elif exists==True:
            
                        
            miro_id = obj_data[object_name]['miro_id']

            update_img_miro(file_path,board_id,parent,miro_id,size=size,position=position)

      return obj_data

def make_or_update_frame_miro(obj_data,frame_name):
      info_dict = obj_data['frames'][frame_name]

      headers = {
                  "Accept": "*/*",
                  "Content-Type": "application/json",
                  "Authorization": "Bearer "+miro_authorisation
      }
      payload = {
                  "data": {
                        "format": "custom",
                        "title": frame_name,
                        "type": "freeform"
                  },
                  "position": {
                        "origin": "center",
                        "x": info_dict[position][0],
                        "y": info_dict[position][1]
                  },
                  "geometry": {
                        "width": info_dict[size][0],
                        "height": info_dict[size][1]
                  },
                  'style': {
                        'fillColor': '#FFFFFF',

                  }
            }
            
      obj_data = make_or_update_miro(headers,payload,'frames',obj_data,frame_name)  
            
      
      return frame_dict




def send_to_miro(starting_pos, size, space, base_name):
      files = os.listdir()
      img_list=[]
      frame_list=[]
      for file in files:
            my_regex = r"^" + re.escape(base_name) + r".*\.jpg"

            if len(re.findall(my_regex,file))>0:
                  img_list.append(file)
                  frame_list.append('frame_'+file[:-4])
            
      # Check if data file exists. Create it if it doesn't.
      if exists("obj_data.json"):
            with open("obj_data.json", 'rb') as inp:
                obj_data = json.load(inp) 
      else:
            # make new dict of data
            obj_data={}




      """if 'frames' in obj_data.keys():
            pass
      else:
            obj_data['frames']={}
      if 'images' in obj_data.keys():
            pass
      else:
            obj_data['images']={}
      """
      position = starting_pos.copy()
      
      for frame_name in frame_list:
            obj_data = make_or_update_frame_miro(obj_data,frame_name,config.miro_authorisation,position,size,make_new=False)
            
            position = [position[0] + space + size[0],position[1]] # position[0] = position[0] + space + size[0] let to some weird results 
            

      #for img in img_list:
      #      upload_img_miro(img,config.config.board_id,None,position=[0,0],size=[1000,1000])


      # save updated obj_data to a json file for next time
      with open('obj_data.json', 'w') as handle:
            json.dump(obj_data, handle)


FigTuple = namedtuple('Fig',['name','board_id','miro_id','uuid','url','position','size','parent','obj_type'])
      



 
