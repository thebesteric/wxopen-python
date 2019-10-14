import datetime
import json
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from client.domain import wxerror
from settings import WX_OPEN_CONFIG, WX_OPEN_THIRD_CONFIG
from cache.cache import get_cache_instance
import constants

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
    access_token = content.get(constants.ACCESS_TOKEN)
    if access_token:
        memory_cache.set(constants.ACCESS_TOKEN, access_token)
        logger.info('Get ACCESS_TOKEN succeed: %s' % ('*' * 6))
    else:
        errcode = str(content.get('errcode'))
        logger.error('Get ACCESS_TOKEN failed: %s: %s' % (errcode, wxerror.ERROR_CODE.get(errcode)))


def get_component_access_token():
    """
    令牌（component_access_token）是第三方平台接口的调用凭据。
    令牌的获取是有限制的，每个令牌的有效期为 2 小时，请自行做好令牌的管理，在令牌快过期时（比如1小时50分），重新调用接口获取。
    如未特殊说明，令牌一般作为被调用接口的 GET 参数 component_access_token 的值使用

    正确返回： {"component_access_token": "COMPONENT_ACCESS_TOKEN", "expires_in": 7200}
    错误返回： {"errcode": 40013, "errmsg": "invalid appid"}
    """

    url = 'https://api.weixin.qq.com/cgi-bin/component/api_component_token'
    data = {'component_appid': WX_OPEN_THIRD_CONFIG['COMPONENT_APP_ID'],
            'component_appsecret': WX_OPEN_THIRD_CONFIG['COMPONENT_APP_SECRET'],
            'component_verify_ticket': memory_cache.get(constants.COMPONENT_VERIFY_TICKET)}
    content = json.loads(requests.post(url, json=data).content.decode('utf8'))
    component_access_token = content.get(constants.COMPONENT_ACCESS_TOKEN)
    if component_access_token:
        memory_cache.set(constants.COMPONENT_ACCESS_TOKEN, component_access_token)
        logger.info('Get COMPONENT_ACCESS_TOKEN succeed: %s' % ('*' * 6))
    else:
        errcode = str(content.get('errcode'))
        logger.error('Get ACCESS_TOKEN failed: %s: %s' % (errcode, wxerror.ERROR_CODE.get(errcode)))


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


def task_client_start():
    scheduler = BackgroundScheduler()
    # 每 5400s 执行一次
    scheduler.add_job(get_access_token, 'interval', seconds=5400, next_run_time=datetime.datetime.now())
    scheduler.start()


def task_third_start():
    scheduler = BackgroundScheduler()
    # 每 5400s 执行一次
    scheduler.add_job(get_component_access_token, 'interval', seconds=5400, next_run_time=datetime.datetime.now())
    scheduler.start()