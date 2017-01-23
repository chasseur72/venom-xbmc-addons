#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 

import urllib2,urllib,re,xbmcgui,xbmc

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MailRu'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'mailru'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {"User-Agent":UA}

        req1 = urllib2.Request(self.__sUrl,None,headers)
        resp1 = urllib2.urlopen(req1)
        sHtmlContent = resp1.read()
        resp1.close()

        sPattern = '{"metadataUrl":"([^"]+)",'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        vurl = 'http://my.mail.ru/' + aResult[1][0]
        
        req = urllib2.Request(vurl,None,headers)
        
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
        
        data = response.read()
        head = response.headers
        response.close()

        #get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            #print aResult
            if (aResult[0] == True):
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1]+ ';'
       

        sPattern = '{"url":"([^"]+)",.+?"key":"(\d+p)"}'
        aResult = oParser.parse(data, sPattern)
        xbmc.log(str(aResult))
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))   
            #Si une seule url
            if len(url) == 1:
                api_call = 'http:' + url[0]
                xbmc.log(str(api_call))
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = 'http:' + url[ret]
                    xbmc.log(str(api_call))
                    
        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Cookie=' + cookies
            
        return False, False
