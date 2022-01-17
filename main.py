import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from licensing.methods import Key, Helpers
import math
import requests
import logging
import json
import generateExcelFile
import sendEmail
import sys
from datetime import datetime

# written by Padua, game url, RSA Public Key and authentication code are removed from this code sample
# If you have interest in this code contact me on Discord: Padua#6834
RSAPubKey = ""
auth = ""


class RRbot:
    def __init__(self, email, password, warsIds, price, partyId):
        result = Key.activate(token=auth,
                              rsa_pub_key=RSAPubKey,
                              product_id=,
                              key="",
                              machine_code=Helpers.GetMachineCode())

        if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
            logging.warn("The license does not work: {0}".format(result[1]))
            sys.exit()
        else:
            s = requests.Session()
            logging.warn("License works, Bot started")
            self.email = email
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.loginWithFacebook(email, password)
            sessid = self.driver.get_cookie('PHPSESSID')
            expires = sessid.get('expiry', None)
            sessid.pop('expiry', None)
            sessid.pop('httpOnly', None)
            sessid['expires'] = expires
            self.driver.close()
            # give the session the cookies; logged in!
            s.cookies.set(**sessid)
            # grab the c (verification token)
            c = s.get(
                'http://rivalregions.com/#overview').text.split("var c_html = '")[1].split("'")[0]
            # grab the playerID
            playerID = s.get(
                'http://rivalregions.com/#overview').text.split("var id		=	")[1].split(";")[0]
            self.c = c
            self.s = s
            self.sessid = sessid
            self.playerID = playerID
            self.expireTime = expires
            party = self.partyJson()
            self.price = price
            self.partyId = partyId
            #time used for sending email
            now = datetime.now()
            currentTime = now.strftime("%H:%M:%S")
            warUrl = 'gameURL'
            warsIds = str(warsIds).split(',')            
            for war in warsIds:
                if war == "" or math.isnan(int(war)):
                    logging.warn(
                        "YOU ADDED AN UNACCEPTABLE VALUE TO THE WAR ID LIST")
                    break
                content = s.get(f'{warUrl}{war}?c={self.c}').text
                soup = BeautifulSoup(content, 'html.parser')
                # Returns the table row for every party in the war damage page
                for partyInfo in soup.select('tr[user]'):
                    foundPartyId = str(partyInfo).split(
                        'user="')[1]
                    foundPartyId = foundPartyId.split('"')[0]
                    # FOUND THE PARTY ID
                    if (foundPartyId == partyId):
                        #GET PARTY NAME
                        partyName = str(partyInfo).split(
                            'class="list_name pointer">')[1]
                        partyName = partyName.split('<br/>')[0]
                        #GET SIDE IN WAR (OFFENSIVE OR DEFENSIVE)
                        actionLink = str(partyInfo).split('<td action="')[1]
                        actionLink = actionLink.split('"')[0]
                        content2 = s.get(
                            f'http://rivalregions.com/{actionLink}?c={self.c}').text
                        soup2 = BeautifulSoup(content2, 'html.parser')
                        for memberInfo in soup2.select('tr[user]'):
                            #GET PARTY MEMBER ID
                            memberId = str(memberInfo).split('user="')[1]
                            memberId = memberId.split('"')[0]
                            #GET MEMBER'S NAME
                            memberName = str(memberInfo).split(
                                'class="list_name pointer">')[1]
                            memberName = memberName.split('</td>')[0]
                            #GET MEMBER'S LEVEL
                            memberLevel = str(memberInfo).split(
                                '<span class="yellow">', 2)[1]
                            memberLevel = memberLevel.split('</span>')[0]
                            memberDamage = str(memberInfo).split(
                                '<span class="yellow">', 2)[2]
                            memberDamage = memberDamage.split('</span>')[0]
                            memberDamage = int(memberDamage.replace(".", ""))
                            ##########################################
                            # WAR DATA FOR SPECIFIC MEMBER COLLECTED #
                            ##########################################
                            if not party:  # IF EMPTY PARTY ARRAY, ADD NEW MEMBER
                                playerJson = {"PlayerID": memberId,
                                              "PlayerName": memberName,
                                              "PlayerLevel": memberLevel,
                                              "PlayerDamage": memberDamage,
                                              "PlayerPayment" : '0'}
                                party.append(playerJson)
                            else:  # ELSE = IF PARTY ARRAY ISNT EMPTY
                                found = False
                                for memberArray in party:
                                    logging.info("PLAYER ID = " +
                                          memberArray['PlayerID'])
                                    # IF = IF ALREADY EXISTS, UPDATE DAMAGE COUNT
                                    if memberArray['PlayerID'] == memberId:
                                        memberArray['PlayerDamage'] += memberDamage
                                        found = True
                                        break
                                if not found:  # ELSE = DOESNT EXIST, ADD NEW MEMBER ARRAY
                                    playerJson = {"PlayerID": memberId,
                                                  "PlayerName": memberName,
                                                  "PlayerLevel": memberLevel,
                                                  "PlayerDamage": memberDamage,
                                                  "PlayerPayment" : '0'}
                                    party.append(playerJson)
        #### PAYMENT TIME #####
        for data in party:
            value = data["PlayerDamage"] * (int(price) * 1000)
            value = str(value).split(".")[0]
            data["PlayerPayment"] = value
            logging.info("SET PAYMENT FOR "+data["PlayerName"]+ ": $"+ data["PlayerPayment"])
            if data['PlayerID'] != self.playerID:
                logging.info("EXPECTED VALUE FOR " +
                             data['PlayerName'] + " equals " + value)
                response = s.post(url='gameURL', data={
                    "whom": data["PlayerID"], "type": "0", "n": value, "c": {self.c}})
        self.saveJsonData(party, "partyData.json")
        generateExcelFile.getExcelData()
        sendEmail.sendEmail(currentTime)  # SENDS THE .xlsx FILE VIA EMAIL
        # DELETE GENERATED LOCAL FILES
        if os.path.isfile('paymentReceipt.xlsx') and os.path.isfile('partyData.json'):
            os.remove('paymentReceipt.xlsx')  # remove the file
            os.remove('partyData.json')  # remove the file
        else:
            logging.info("COULDNT FILE THE FILES TO DELETE")

    def loginWithFacebook(self, email, password):
        RR = 'gameURL'
        self.driver.get("facebookURL")
        sleep(2)
        self.driver.find_element_by_name("email").send_keys(email)
        sleep(2)
        self.driver.find_element_by_name(
            "pass").send_keys(password, Keys.ENTER)
        sleep(5)
        self.driver.get(RR)
        sleep(5)
        self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Facebook')]").click()
        sleep(5)
        try:
            self.driver.find_elements_by_class_name('header_slide')
        except NoSuchElementException:
            self.driver.find_element_by_class_name("kkf49tns").click() #Verification status
        sleep(2)

    def loginWithVK(self, email, password):
        RR = 'gameURL'
        self.driver.get("vkURL")
        sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/form/input[7]").send_keys(email)
        sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/form/input[8]").send_keys(password)
        sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/form/button').click()
        sleep(5)
        self.driver.get(RR)
        sleep(5)
        self.driver.find_element_by_xpath(
            "//div[contains(text(), 'VK')]").click()
        sleep(2)
        self.driver.find_element_by_xpath(
            '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]').click()

    def loginWithGoogle(self, email, password):
        RR = 'gameURL'
        self.driver.get("googleMailURL")
        sleep(2)
        self.driver.find_element_by_class_name(
            "whsOnd").send_keys(email, Keys.ENTER)
        sleep(2)
        self.driver.find_element_by_class_name(
            "whsOnd").send_keys(password, Keys.ENTER)
        sleep(2)
        self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Next')]").click()

    def partyJson(self):
        data = []
        return data

    def readJsonData(self):
        # read the json into a dict
        with open('partyData.json', 'r') as f:
            data = json.loads(f.read())
            return data

    def saveJsonData(self, data, fileName):
        # save the dict to disk
        with open(fileName, 'w') as f:
            f.write(json.dumps(data))
