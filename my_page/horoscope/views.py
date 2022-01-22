from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
import lxml
import datetime

# Create your views here.

zodiac_dict = {
    'aries': 'Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).',
    'taurus': 'Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).',
    'gemini': 'Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).',
    'cancer': 'Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).',
    'leo': ' Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).',
    'virgo': 'Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).',
    'libra': 'Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).',
    'scorpio': 'Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).',
    'sagittarius': 'Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).',
    'capricorn': 'Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).',
    'aquarius': 'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).',
    'pisces': 'Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта).',
}

zodiac_type_dict = {
    'fire': ['aries', 'leo', 'sagittarius'],
    'earth': ['taurus', 'virgo', 'capricorn'],
    'air': ['gemini', 'libra', 'aquarius'],
    'water': ['cancer', 'scorpio', 'pisces'],
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
}

now = datetime.datetime.now().strftime('%d-%m-%Y')

def info_by_type(request):
    type_zodiac = list(zodiac_type_dict)
    li_elements = ''
    for zod_typ in type_zodiac:
        redirect_path = reverse('horoscope-type', args=[zod_typ])
        li_elements += f'<li> <a href= {redirect_path}> {zod_typ.title()} </a> </li>'
    response = f"""
    <ul>
    {li_elements}
    </ul>
    """
    return HttpResponse(response)


def get_info_by_type(request, sign_type: str):
    type_zodiac = zodiac_type_dict.get(sign_type)
    li_elements = ''
    for typ in type_zodiac:
        redirect_path = reverse('horoscope-name', args=[typ])
        li_elements += f'<li> <a href= {redirect_path}> {typ.title()} </a> </li>'
    response = f"""
    <ul>
    {li_elements}
    </ul>
    """
    return HttpResponse(response)


def index(request):
    zodiacs = list(zodiac_dict)
    # f'<li> <a href= {redirect_path}> {sign.title()} </a> </li>'
    context = {
        'zodiacs': zodiacs,
    }
    return render(request, 'horoscope/index.html', context=context)


def get_info_about_sign_zodiac(request, sign_zodiac: str):
    url = f'https://orakul.com/horoscope/astrologic/more/{sign_zodiac}/today.html'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    hor_info = soup.find('div', class_='horoBlock').text.strip()
    zodiacs = list(zodiac_dict)
    description = zodiac_dict.get(sign_zodiac)
    data = {
        'description_zodiac': description,
        'sign': sign_zodiac,
        'zodiacs': zodiacs,
        'sign_name': description.split()[0],
        'hor_info_today': hor_info,
        'date': now,
    }
    return render(request, 'horoscope/info_zodiac.html', context=data)


def get_info_about_sign_zodiac_by_number(request, sign_zodiac: int):
    zodiacs = list(zodiac_dict)
    if sign_zodiac > len(zodiacs):
        return HttpResponseNotFound(f'Incorrect number of zodiac: {sign_zodiac}')
    name_zodiac = zodiacs[sign_zodiac-1]
    redirect_url = reverse('horoscope-name', args=[name_zodiac])
    return HttpResponseRedirect(redirect_url)
