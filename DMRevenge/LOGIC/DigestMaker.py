import subprocess
import os

from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate

import COMPONENT.BasicErrorComponent as BEC
#import COMPONENT.BasicErrorComponent as BEC
#from COMPONENT import *
#class versionの作成。
#一応成功した。
class DigestMaker:
    
    def __init__(self,path,output,threshold ,silence_section ):
        try:
            self.path = path
            self.output = output
            self.threshold = threshold
            self.silence_section = silence_section
            self.video = VideoFileClip(self.path)
        except OSError:
                BEC.show_error("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
            
    
    def get_info(self):
        
        try:
            self.info = subprocess.run(["echo 'A'"], shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
            self.info = subprocess.run(["ffmpeg","-vn" ,"-i", self.path, "-af",
                                    f"silencedetect=noise={self.threshold}dB:d={self.silence_section}",
                                    "-f", "null", "-"], encoding='utf-8',stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True,
                                    text = True)
        except IndexError:
            BEC.show_error("外部アプリとの接続エラーがはっせいしました。\nファイル名にひらがなの数字などを使っていませんか?")
        except:
            BEC.show_error("予期せぬエラーが発生しました\n外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
        # "-af", "silencedetect=noise=-33dB:d=0.6"オーディオの設定。ノイズのデシベルと、秒数の指定。
        
        self.info = str(self.info)
        
        return self.info
    def silence_detect(self,info):
        self.info = info
        lines = info.split('\\n')
        
        time_list =[]

        for line in lines:
            if "silencedetect" in line:
                words = line.split(" ")

                for i in range(len(words)):
                    if "silence_start" in words[i]:
                       
                        time_list.append(float(words[i+1].replace('\\r','')))
                    if "silence_end" in words[i]:
                        
                        time_list.append(float(words[i+1].replace('\\r','')))
               
            
        self.starts_ends = list(zip(*[iter(time_list)]*2))
        
        return self.starts_ends



    def using_parts(self,starts_ends):
        
        
        #動画の長さを図る
        duration = self.video.duration

        #５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
        self.merge_list = [[self.starts_ends[i][1],self.starts_ends[i + 1][0]] for i in range(len(self.starts_ends)) if i <= len(starts_ends) - 2]
        #音声の始まりが無音ではなかった場合,最初の部分をつける
        if self.starts_ends[0][0] != 0:
            self.merge_list.insert(0,[0,self.starts_ends[0][1]])
        #音声の終わりが無音ではなかった場合、最後の部分をつける

        if self.starts_ends[-1][1] <= int(duration):
            self.merge_list.insert(-1,[self.starts_ends[-1][1],int(duration)])
        return self.merge_list

    def concatenate_videos(self,merge_list):      
        clips = {}      
        count = 0

        for i in range(len(merge_list)):
            clips[count] = self.video.subclip(self.merge_list[i][0],self.merge_list[i][1])
            count += 1
        
        #listがたのから集合にclipsを入れていく
        videos = [clips[i] for i in range(count)]
        #concatenateで、それらを合体させていく
        result = concatenate(videos)
        #.write_videofileで合体させたものを動画として出力。
        result.write_videofile(self.output,fps = 20,preset = "ultrafast")


def run(path,output,threshold,silence_section):
    movie = DigestMaker(path,output,threshold,silence_section)    
    try:
        info = movie.get_info()
    except OSError:
        BEC.show_error("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
    else:
        pass
    info = movie.get_info()
    starts_ends = movie.silence_detect(info)
    if type(starts_ends) == bool:
        pass
    elif starts_ends == []:
        BEC.show_error(">>無音区間の検出ができませんでした。スレッショルドなどの値を見直してみてください。")
        pass      

    else:
       
        try:
            merge_list = movie.using_parts(starts_ends)
            movie.concatenate_videos(merge_list)
        except OSError:
            BEC.show_error("外部アプリとの連携が取れていない可能性があります。PC,アプリを再起動して見てください")
        except:
            BEC.show_error("予期せぬエラーが発生しました。")
        else:
            BEC.show_info("動画出力が完了しました。")
