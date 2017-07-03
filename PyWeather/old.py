def updateLocal(self,data,dataName):
        respdata = None
        host = self.config['socketServer']       
      
        try:
            h = httplib2.Http(timeout=10)           
            resp, respdata = h.request(
                uri='http://' + host + '/' + dataName,
                method='POST',
                headers={'Content-Type': 'application/json; charset=UTF-8'},
                body=data.toJSON()                
                )

            if (resp.status != 200):
                respdata = None
                Logger.error('updateLocal ' + str(resp.status))            
                
        except Exception as e:          
            Logger.error(e)

        return respdata   