from burp import IBurpExtender, ITab
import json
import socket
import subprocess


class BurpExtender(IBurpExtender, ITab):

                cb = None
                
                @staticmethod
                def addRedirection(host, ip, callbacks, log):
                               cb = callbacks
                               config = cb.saveConfigAsJson("project_options.connections.hostname_resolution")
                               configJson =  json.loads(config)
                               newEntry = {u'ip_address': u'127.0.0.1', u'enabled': True, u'hostname': u'test.test'}
                               newEntry["ip_address"] = ip
                               newEntry["hostname"] = host
                               configJson['project_options']['connections']['hostname_resolution'].append(newEntry)
                               cb.loadConfigFromJson(json.dumps(configJson))
                               log.append("- New entry at (Project options -> Hostname Resolution)\n------------------------------------------------------------------------------------------------\n")
                
                @staticmethod
                def getStagingIP(host, log):
                               log.append("- " + host + "\n")
                               process = subprocess.Popen(["nslookup", host], stdout=subprocess.PIPE)
                               output = process.communicate()[0].split('\n')
                               subprocess.Popen.kill(process)
                               akamaiProduction = output[3].partition("    ")[2]
                               log.append("- Akamai Production: " + akamaiProduction + "\n")
                               akamaiStaging =  akamaiProduction.replace("akamaiedge", "akamaiedge" + "-staging").strip()
                               log.append("- Akamai Staging: " + akamaiStaging + "\n")
                               stagingIP = socket.gethostbyname(akamaiStaging)
                               log.append("- Staging IP: " + stagingIP + "\n")
                               return stagingIP 
                
                def registerExtenderCallbacks( self, callbacks):
                                global cb
                                cb = callbacks
                                callbacks.addSuiteTab(self) 
                                
                def getTabCaption(self):
                                return "Test on Akamai Staging"
                
           
                def getUiComponent(self):
                                from javax.swing import (JPanel,JButton,JTextField,JTextArea,JScrollPane)
                                
                                panel = JPanel()

                                text = JTextField(50)

                                panel.add(text) 
                                log = JTextArea("",30,65)
                                log.setWrapStyleWord(True)
                                scroll = JScrollPane(log)

                                def btn1Click(event):
                                    global cb
                                    host = text.getText()
                                    self.addRedirection(host, self.getStagingIP(host, log), cb, log)
                                    return
                                    
                                btn1 = JButton("Test on Akamai Staging", actionPerformed= btn1Click)
                                panel.add(btn1)

                
                                panel.add(scroll)

                                return panel
