from moviepy.editor import *
import os
import whisper
import time

timer0=time.time()
timer=time.time()
audio_folder = 'resources'
audio_file='the-biggest-myth-in-education-48kbps.mp3'
temp_folder=os.path.join('temp','temp_audio_holder-'+audio_file[:10])
output_folder=os.path.join('output','output-'+audio_file[:10])
WHISPER_MODEL='small'
WHISPER_LANG='eng'
output_file=f'transcript_{WHISPER_LANG}_{WHISPER_MODEL}_'+audio_file[:-4]
path = os.path.join(audio_folder,audio_file)
audio_clip=AudioFileClip(path)
n= round(audio_clip.duration)-1   # en este caso el remanente es milesimas de segundo, abrir un archivo para poco tiempo , causa error!

counter =0 
start=0
audio_clip.close()
#time interval
t_interval=60

exit_flag=False


# create temp folder if doesn't exists
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
# create output folder if doesn't exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Using whisper
try:
    model = whisper.load_model(WHISPER_MODEL, device='gpu')
    print("GPU Found,")
except:
    print("No GPU found, using CPU")
    model = whisper.load_model(WHISPER_MODEL, device='cpu')
    
print("Loading mp3 and models took:", round(time.time()-timer,2))
timer=time.time()

def save_txt_file(list_txt):
    path_to_save=os.path.join(output_folder,output_file)
    with open(path_to_save, mode="a+") as f: 
        f.write(list_txt+'\n') 


while(True):
    audio_clip= AudioFileClip(path)
    if t_interval >= n:
        exit_flag=True
        t_interval=n
    
    temp=audio_clip.subclip(start,t_interval)
    temp_saving_location=os.path.join(temp_folder,f'temp_{counter}.mp3')
    temp.write_audiofile(temp_saving_location)
    temp.close()
    counter+=1
    start = t_interval
    audio_clip.close()
    if exit_flag:
        break
    t_interval+=60


print(f"Splitting mp3 into {counter} pieces, took:", round(time.time()-timer,2))
timer=time.time()

list_chunks=os.listdir(temp_folder)
start=0
end=0
id_encounter=0
final_list_of_text = []
total_text=[]
for indx in range(len(list_chunks)):
    timer2=time.time()
    # for chunk in list_chunks: # No mantiene ordern
    chunk=f'temp_{indx}.mp3'
    path_to_saved_file= os.path.join(temp_folder, chunk)
    audio_clip=AudioFileClip(path_to_saved_file)
    duration=audio_clip.duration
    audio_clip.close() 

    out = model.transcribe(path_to_saved_file)
    print(f"Saving text of {chunk}")
    save_txt_file(out['text'])
    print(f"Processing chunk{indx} and saving txt, took:", round(time.time()-timer2,2))
 


# save_txt_file(total_text)
print('Whole process took:', round(time.time()- timer0, 2),"or",round((time.time()- timer0)/60, 2),"minutes")