from burp import IBurpExtender, ITab
import json
import socket
import subprocess


class BurpExtender(IBurpExtender, ITab):

                cb = None
                
                @staticmethod
                def addRedirection(host, ip, callbacks):
                               cb = callbacks
                               config = cb.saveConfigAsJson("project_options.connections.hostname_resolution") 
                               configJson =  json.loads(config)
                               newEntry = {u'ip_address': u'127.0.0.1', u'enabled': True, u'hostname': u'test.test'}
                               newEntry["ip_address"] = ip
                               newEntry["hostname"] = host
                               configJson['project_options']['connections']['hostname_resolution'].append(newEntry)
                               cb.loadConfigFromJson(json.dumps(configJson))
                
                @staticmethod
                def getStagingIP(host):
                               process = subprocess.Popen(["nslookup", host], stdout=subprocess.PIPE)
                               output = process.communicate()[0].split('\n')
                               subprocess.Popen.kill(process)
                               akamaiProduction = output[3].partition("    ")[2]
                               akamaiStaging =  akamaiProduction.replace("akamaiedge", "akamaiedge" + "-staging").strip()
                               return socket.gethostbyname(akamaiStaging)
                
                def registerExtenderCallbacks( self, callbacks):
                                global cb
                                cb = callbacks
                                callbacks.addSuiteTab(self) 
                                
                def getTabCaption(self):
                                return "Test on Akamai Staging"
                
           
                def getUiComponent(self):
                                from javax.swing import (JPanel,JButton,JTextField)
                                
                                def btn1Click(event):
                                    global cb
                                    host = text.getText()
                                    self.addRedirection(host, self.getStagingIP(host), cb)
                                    return
                                    
                                panel = JPanel()
                                text = JTextField(50) 
                                panel.add(text) 
                                btn1 = JButton("Test on Akamai Staging", actionPerformed= btn1Click)
                                panel.add(btn1)
                                return panel
