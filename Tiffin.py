
import re
import urllib
from bs4 import BeautifulSoup

class Tiffin:
    'Common base class used to define tiffins. It stores all the attributes and all the methods that each tiffin should have.'
    title = ''
    description = ''
    email=''
    phone = ''
    city = ''
    zipcode = ''
    specialities = ''
    cuisine =''
    fname=''
    def __init__(self,title,description,email,phone,fname,city,zipcode,specialities,cuisine):
        self.title=title
        self.description=description
        self.email=email
        self.phone=phone
        self.fname=fname
        self.city=city
        self.zipcode=zipcode
        self.specialities=specialities
        self.cuisine=cuisine


    def displayTiffin(self):

        print "Title:",self.title
        print "Description:",self.description
        print "email:",self.email
        print "phone:",self.phone
        print "Contact_name:",self.fname
        print "city:",self.city
        print "zipcode:",self.zipcode
        print "specialities:",self.specialities
        print "cuisine:",self.cuisine


def parse_tiffin(link):
    response = urllib.urlopen(link)
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('title').text
    description = ''
    ad_text = soup.find("span", {"class": "fad_text"})
    email = ''
    phone = ''
    city = ''
    zipcode = ''
    specialities = ''
    cuisine1 = None
    cuisine2 = None
    cuisine = ''

    fname = ''
    fad_zip = ''
    fad_city = ''
    if ad_text is not None:

        for x in ad_text.find_all("p"):
            description = description + x.text.strip()

        email_match = re.search(r'[\w\.-]+@[\w\.-]+', description)
        if email_match:
            email = email_match.group()

        phone_match = re.search(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", description)
        if phone_match:
            phone = phone_match.group()

        cuisine1_match = re.search('south\s*indian', description, re.IGNORECASE)
        if cuisine1_match:
            cuisine1 = cuisine1_match.group().lower()

        cuisine2_match = re.search('north\s*indian', description, re.IGNORECASE)
        if cuisine2_match:
            cuisine2 = cuisine2_match.group().lower()

        if cuisine1 is not None and cuisine2 is not None:
            cuisine = cuisine1 + "," + cuisine2
        elif cuisine1 is not None:
            cuisine = cuisine1
        elif cuisine2 is not None:
            cuisine = cuisine2
        else:
            cuisine = 'Unknown'

    if soup.find("span", {"class": "fname"}) is not None:
        fname = soup.find("span", {"class": "fname"}).text
    if soup.find("span", {"class": "fad_zip"}) is not None:
        fad_zip = soup.find("span", {"class": "fad_zip"}).text
    if soup.find("span", {"class": "fad_city"}) is not None:
        fad_city = soup.find("span", {"class": "fad_city"}).text

    my_tiffin = Tiffin(title, description, email, phone, fname, fad_city, fad_zip, specialities, cuisine)
    return my_tiffin
