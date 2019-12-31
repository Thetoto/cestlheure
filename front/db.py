from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from datetime import datetime
from calendar import monthrange

from .models import CestLheure


# Fetch last c'est l'heure message
def get_latest_cestlheure():
    return CestLheure.objects.latest()


def get_stars():
    global_score = get_query_by_month()
    winner = {}
    for i in global_score:
        if i["month"] not in winner or winner[i["month"]]["total"] <= i["total"]:
            winner[i["month"]] = i
    result = {}
    for i in winner:
        if datetime.now().year == i.year and datetime.now().month == i.month:
            continue
        if winner[i]["message__author"] not in result:
            result[winner[i]["message__author"]] = {
                "stars": 1,
                "player": winner[i]
            }
        else:
            result[winner[i]["message__author"]]["stars"] += 1
    final_list = list(result.values())
    final_list.sort(key=lambda x: x["stars"], reverse=True)
    return final_list


# Fetch global score of every users
def get_global_score():
    return CestLheure.objects \
        .values('message__author', 'message__author__name', 'message__author__photo_url') \
        .annotate(total=Count('message__author')) \
        .order_by('-total')


# Fetch score by day by users for selected month
def get_query_by_day(selected_month):
    return CestLheure.objects \
        .filter(exact_date__gte=selected_month, exact_date__lt=selected_month + relativedelta(months=+1)) \
        .annotate(day=TruncDay('message__time')) \
        .values('day', 'message__author', 'message__author__name', 'message__author__color') \
        .annotate(total=Count('day')) \
        .order_by('day')


# Fetch score by month by users
def get_query_by_month():
    return CestLheure.objects \
        .annotate(month=TruncMonth('message__time')) \
        .values('month', 'message__author', 'message__author__name', 'message__author__color',
                'message__author__photo_url') \
        .annotate(total=Count('month')) \
        .order_by('month')


def color_variant(hex, factor=0.5):
    (r, g, b) = tuple(int(hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    r = 255 - (255 - r) * (1 - factor)
    g = 255 - (255 - g) * (1 - factor)
    b = 255 - (255 - b) * (1 - factor)
    return "#%02x%02x%02x" % (int(r), int(g), int(b))


# Function to prepare data for ChartJS
def chart_ready_by_day(year, month):
    date = datetime(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    labels = list(range(1, monthrange(year, month)[1] + 1))

    if datetime.now().year == date.year and datetime.now().month == date.month:
        numdays = datetime.now().day
    else:
        _, numdays = monthrange(year, month)

    by_day = list(get_query_by_day(date))
    datasets = {}
    for i in by_day:
        if i["message__author"] not in datasets:
            datasets[i["message__author"]] = {
                "label": i["message__author__name"],
                "data": [],
                "fill": False,
                "backgroundColor": color_variant(i["message__author__color"]),
                "borderColor": i["message__author__color"]
            }
        last = datasets[i["message__author"]]["data"][-1] if len(datasets[i["message__author"]]["data"]) > 0 else 0
        while len(datasets[i["message__author"]]["data"]) < i["day"].day:
            datasets[i["message__author"]]["data"].append(last)
        datasets[i["message__author"]]["data"][i["day"].day - 1] = last + i["total"]

    for i in datasets:
        while len(datasets[i]["data"]) < numdays:
            datasets[i]["data"].append(datasets[i]["data"][-1])
    return {"datasets": list(datasets.values()), "labels": labels}


# Function to prepare data for ChartJS
def chart_ready_by_month():
    first = CestLheure.objects.earliest().exact_date.astimezone().replace(day=1, hour=0, minute=0, second=0,
                                                                          microsecond=0)
    now = datetime.now().astimezone().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    labels = []
    while first <= now:
        labels.append(f"{'0' if first.month < 10 else ''}{first.month}/{first.year}")
        first += relativedelta(months=+1)

    by_month = list(get_query_by_month())
    datasets = {}
    for i in by_month:
        if i["message__author"] not in datasets:
            datasets[i["message__author"]] = {
                "label": i["message__author__name"],
                "data": [None] * len(labels),
                "fill": False,
                "backgroundColor": color_variant(i["message__author__color"]),
                "borderColor": i["message__author__color"]
            }
        str_of_month = f"{'0' if i['month'].month < 10 else ''}{i['month'].month}/{i['month'].year}"
        datasets[i["message__author"]]["data"][labels.index(str_of_month)] = i["total"]

    return {"datasets": list(datasets.values()), "labels": labels}