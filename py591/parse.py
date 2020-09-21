#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""591 rental parser
"""

import argparse
import io
import json
import sys
from collections import OrderedDict

import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image

headers = {
    "User-agent": "Report abuse: me@frankchang.me",
}


def fetch_info(link):
    """Fetch utf-8 encoded bytes from given url

    Arguments:
        link: target URL

    Returns:
        source (bytes): UTF-8 encoded bytes
    """

    return requests.get(link, headers=headers).text.encode("utf-8")


def parse_label_list(soup):
    labels = soup.select("ul.clearfix.labelList.labelList-1")[0]
    labellist = []

    for li in labels.select("li.clearfix"):
        for div in li.select("div.one"):
            key = div.getText().replace(u" ", "")
            value = div.findNextSibling("div", {"class": "two"}).em.getText()
            labellist.append((key, value))

    return OrderedDict(labellist)


def parse_facility(soup):
    """Parse facility data from soup

    Arguments:
        soup: the soup object to parse from

    Returns:
        result (tuple): list of available facility and unavailable facility
    """

    facilities = []
    no_facilities = []

    facilityList = soup.select("ul.facility.clearfix")[0]
    for facility in facilityList.findChildren("li"):
        if "no" in facility.span["class"]:
            no_facilities.append(facility.getText())
        else:
            facilities.append(facility.getText())

    return (facilities, no_facilities)


def parse_photos(soup):
    """Parse photo URLs from soup

    Arguments:
        soup: the soup object to parse from

    Returns:
        URL list: list of image URLs
    """

    imgEles = soup.select("div.imgList")[0].findChildren("img")
    imgUrlList = []
    for img in imgEles:
        imgUrlList.append(img["src"].replace("_125x85.crop.jpg", "_765x517.water3.jpg"))

    return imgUrlList


def parse_info(soup):
    """Parse rent and detail descriptions from soup

    Arguments:
        soup: the soup object to parse from

    Returns:
        information (dict): parsed information
    """

    info = OrderedDict()

    infoSection = soup.select("div.detailInfo.clearfix")[0]
    priceSec = infoSection.select("div.price.clearfix")[0]
    explainSec = infoSection.select("div.explain")[0]
    attrs = infoSection.select("ul.attr li")

    price = priceSec.i.getText().replace(u" ", "").replace("\xa0", "").replace(u" ", "")
    explain = explainSec.getText().replace(u" ", "").replace("\xa0", "")
    info[u"租金"] = u"{0} ({1})".format(price, explain)

    for attr in attrs:
        info.update(
            (
                tuple(
                    attr.getText().replace(u"&nbsp;", "").replace("\xa0", "").split(":")
                ),
            )
        )

    return info


def parse_status(soup):
    """Parse the status text from the soup

    Arguments:
        soup: soup object to parse

    Returns:
        status text (string): status text
    """

    return (
        soup.select("div.houseIntro")[0]
        .getText()
        .replace("&nbsp;", " ")
        .replace("<br>", "\n")
        .replace(" ", "")
        .replace("\xa0", "")
        .replace("\r\n", "\n")
    )


def parse_phone_number(soup):
    """Parse the phone number of the contact from the soup

    Arguments:
        soup: soup object to parse

    Returns:
        phone number (string): the parsed phone number if the phone number existed; otherwise, None is returned
    """

    phoneImg = soup.select("span.num")
    if phoneImg[0].img:
        phoneImgUrl = phoneImg[0].img["src"].replace("//", "https://")
        rep = requests.get(phoneImgUrl, headers=headers).content
        image = Image.open(io.BytesIO(rep))

        return (
            pytesseract.image_to_string(image, lang="eng", config="--dpi 200")
            .strip()
            .replace(" ", "")
        )

    return None


def get_591_info(link):
    """Gather informations from the URL

    Arguments:
        link (string): target link to get information from.

    Returns:
        information (dict): gathered information
    """

    info = OrderedDict()

    raw = fetch_info(link)
    soup = BeautifulSoup(raw, "html.parser")
    facility_info = parse_facility(soup)

    info[u"標題"] = soup.select("span.houseInfoTitle")[0].getText()
    info[u"地址"] = soup.select("span.addr")[0].getText()
    info[u"網址"] = link
    info[u"照片"] = parse_photos(soup)
    info[u"聯絡方式"] = parse_phone_number(soup)

    info.update(parse_info(soup))
    info[u"房東提供"] = facility_info[0]
    info[u"房東不提供"] = facility_info[1]
    info.update(parse_label_list(soup))
    info[u"屋況"] = parse_status(soup)

    return info


def main():
    """591 CLI parser"""
    parser = argparse.ArgumentParser(
        description="Fetch data from 591 and return a json string"
    )
    parser.add_argument("url", metavar="url", nargs="+")

    args = parser.parse_args()
    info_list = []

    for link in args.url:
        info = get_591_info(link)
        info_list.append(info)

    if len(info_list) == 1:
        print(json.dumps(info_list[0], ensure_ascii=False, indent=4))
    else:
        print(json.dumps(info_list, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
