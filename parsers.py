import requests
from bs4 import BeautifulSoup
import utils


def matches_parser():
    matches = []
    r = requests.get('https://fc-zenit.ru/')
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    roots = soup.find_all('div', {'class': 'game-card-block__slide'})
    previous = True
    for root in roots[:2]:
        score = ""
        date = root.find('div', {'class': 'game-card__date'}).string
        teams = []
        for team in root.find_all('div', {'class': 'side'}):
            teams.append(team.span.string)
        if previous:
            score = root.find('div', {'class': 'table-score__score-main'}).text
            score = score.replace('\n', '').replace(' ', '')
            previous = False
        tournament = root.find('div', {'class': 'game-card__info'}).find_all('span')[0].text
        stadium = root.find('div', {'class': 'game-card__info'}).find_all('span')[1].text
        if score == "":
            match = 'Ближайший матч\n\n' + \
                    'Дата матча: ' + date + '\n' + \
                    'Матч: ' + teams[0] + ' - ' + teams[1] + '\n' + \
                    'Турнир: ' + tournament + '\n' + \
                    'Стадион: ' + stadium
        else:
            match = 'Прошедший матч\n\n' + \
                    'Дата матча: ' + date + '\n' + \
                    'Матч: ' + teams[0] + ' - ' + teams[1] + '\n' + \
                    'Счёт: ' + score + '\n' + \
                    'Турнир: ' + tournament + '\n' + \
                    'Стадион: ' + stadium
        matches.append(match)
    return matches


def news_parser():
    all_news = []
    r = requests.get('https://fc-zenit.ru/news/')
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find_all('div', {'class': 'row'})[3]
    cnt = 0
    for news in root.find_all('a'):
        if news.get('href') is None:
            continue
        if cnt == utils.MAX_NEWS_CNT:
            break
        if news.get('href') is not None:
            link = news.get('href')
            if not 'https://fc-zenit.ru' in link:
                link = 'https://fc-zenit.ru' + link
            title = news.find('div', {'class': 'news-block__title'}).string
            all_news.append([link, title])
            cnt += 1
    return all_news


def table_parser():
    table = "Команда    Очки\n"
    r = requests.get('https://fc-zenit.ru/zenit/tables/year_304/')
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find('div', {'id': 'TablescoreTable_1113111'})
    for place in range(1, utils.TEAMS_CNT + 1):
        cur_row = root.find('div', {'data-teams': str(place)})
        cur_team = cur_row.find('span', {'class': 'tablescore__link'}).span.string.strip()
        cur_points = cur_row.find('div', {'data-param': 'score'}).string
        table += str(place) + ') ' + \
                 cur_team + ': ' + \
                 cur_points + '\n'
        # print(cur_team, (30 - len(cur_team) - len(str(place))))
    return table


def photo_parser():
    all_photo = []
    r = requests.get('https://fc-zenit.ru/photo/')
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find('ul', {'class': 'photos__list'})
    cnt = 0
    for photo in root.find_all('a'):
        if photo.get('href') is None:
            continue
        if cnt == utils.MAX_PHOTO_CNT:
            break
        if photo.get('href') is not None:
            link = photo.get('href')
            if not 'https://fc-zenit.ru' in link:
                link = 'https://fc-zenit.ru' + link
            if link in all_photo:
                continue
            all_photo.append(link)
            cnt += 1
    return all_photo


def players_parser():
    all_players = []
    r = requests.get('https://fc-zenit.ru/zenit/players/')
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find('div', {'class': 'players-list__inner'})
    for player in root.find_all('div', {'class': 'card-player__body'}):
        name = player.find('a', {'class': 'card-player__name'}).string
        role = player.find('span', {'class': 'card-player__descr-text'}).string
        all_players.append([name, role])
    return all_players