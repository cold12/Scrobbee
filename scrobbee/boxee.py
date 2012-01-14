#!/usr/bin/env python

import boxeeboxclient

class Boxee():
    client = None
    
    def __init__(self, ip, port):
        self.client = boxeeboxclient.BoxeeBoxClient('scrobbee', ip, port, application_id="scrobbee", application_label="Scrobbee")
    
    def getCurrentlyPlaying(self):
        now_playing = {}
        
        activePlayers = self.getActivePlayers()
        
        if (activePlayers["audio"]):
            now_playing["player"] = "audio"
            
            labels = self.getInfoLabels(['MusicPlayer.Title',
                                         'MusicPlayer.Artist',
                                         'MusicPlayer.Album',
                                         'MusicPlayer.TrackNumber',
                                         'MusicPlayer.Duration'])
            
            duration = labels["MusicPlayer.Duration"].split(":")
            if (len(duration) == 2):
                duration = int(duration[0]) * 60 + int(duration[1])
            else:
                duration = int(duration[0])
            
            now_playing["title"] = labels["MusicPlayer.Title"]
            now_playing["duration"] = duration
            now_playing["artist"] = labels["MusicPlayer.Artist"]
            now_playing["album"] = labels["MusicPlayer.Album"]
            now_playing["trackNumber"] = labels["MusicPlayer.TrackNumber"]
            now_playing["percentage"] = int(self.getMusicPlayerPercentage())
        elif (activePlayers["video"]):
            labels = self.getInfoLabels(['VideoPlayer.Title',
                                         'VideoPlayer.Year',
                                         'VideoPlayer.TVShowTitle',
                                         'VideoPlayer.Season',
                                         'VideoPlayer.Episode',
                                         'VideoPlayer.Duration',
                                         'Player.Filenameandpath'])
        
            duration = labels["VideoPlayer.Duration"].split(":")
            if (len(duration) == 3):
                duration = int(duration[0]) * 60 + int(duration[1])
            else:
                duration = int(duration[0])
        
            now_playing["filename"] = labels["Player.Filenameandpath"]
            now_playing["year"] = labels["VideoPlayer.Year"] if labels["VideoPlayer.Year"] != "" else "0"
            now_playing["duration"] = duration
            now_playing["percentage"] = int(self.getVideoPlayerPercentage())
            now_playing["episode"] = ""
            now_playing["season"] = ""
            now_playing["episode_title"] = ""
        
            if (labels["VideoPlayer.TVShowTitle"] != ""):
                now_playing["type"] = "tv-show"
                now_playing["title"] = labels["VideoPlayer.TVShowTitle"]
                now_playing["season"] = labels["VideoPlayer.Season"]
                now_playing["episode"] = labels["VideoPlayer.Episode"]
                now_playing["episode_title"] = labels["VideoPlayer.Title"]
            else:
                now_playing["type"] = "movie"
                now_playing["title"] = labels["VideoPlayer.Title"]
        else:
            now_playing["type"] = None
        
        return now_playing
        
    def getActivePlayers(self):
        activePlayers = self.client.callMethod("Player.GetActivePlayers")
        
        return activePlayers["result"]
    
    def getMusicPlayerPercentage(self):
        return float(self.client.callMethod("AudioPlayer.GetPercentage")["result"])
        
    def getVideoPlayerPercentage(self):
        return float(self.client.callMethod("VideoPlayer.GetPercentage")["result"])
        
    def getInfoLabels(self, labels):
        resp = self.client.callMethod("System.GetInfoLabels", {'labels': labels}, True);
        return resp["result"]
    
    def getInfoBooleans(self, booleans):
        resp = self.client.callMethod("System.GetInfoBooleans", {'booleans': booleans}, True);
        return resp["result"]
    
    def showNotification(self, notification):
        self.client.callMethod("GUI.NotificationShow", {"msg": notification}, True)