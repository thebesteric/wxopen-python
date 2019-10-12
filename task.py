import datetime
import json
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from client.domain import wxerror
from settings import WX_OPEN_CONFIG
from cache.cache import get_cache_instance
from constants import ACCESS_TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

memory_cache = get_cache_instance('default')


def get_access_token():
    """
    获取微信中的：access_token

    正确返回： {"access_token": "ACCESS_TOKEN", "expires_in": 7200}
    错误返回： {"errcode": 40013, "errmsg": "invalid appid"}
    """

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}' \
        .format(app_id=WX_OPEN_CONFIG['APP_ID'], app_secret=WX_OPEN_CONFIG['APP_SECRET'])
    content = json.loads(requests.get(url).content.decode('utf-8'))
    access_token = content.get(ACCESS_TOKEN)
    if access_token:
        memory_cache.set(ACCESS_TOKEN, access_token)
        logger.info('Get ACCESS_TOKEN succeed: %s' % ('*' * 6))
    else:
        errcode = str(content.get('errcode'))
        logger.error('Get ACCESS_TOKEN failed: %s: %s' % (errcode, wxerror.ERROR_CODE.get(errcode)))


def task_start():
    """
    任务调度
    interval: 间隔调度（每隔多久执行）
    weeks (int) – number of weeks to wait
    days (int) – number of days to wait
    hours (int) – number of hours to wait
    minutes (int) – number of minutes to wait
    seconds (int) – number of seconds to wait
    start_date (datetime | str) – starting point for the interval calculation
    end_date (datetime | str) – latest possible date/time to trigger on
    timezone (datetime.tzinfo | str) – time zone to use for the date/time calculations
    """
    scheduler = BackgroundScheduler()
    # 每 5400s 执行一次
    scheduler.add_job(get_access_token, 'interval', seconds=5400, next_run_time=datetime.datetime.now())
    scheduler.start()
