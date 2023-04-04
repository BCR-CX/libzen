import time
from urllib.parse import urlparse
from ._generic import _iterate_search


def wait_for_job(url, sleep_time=5):
    endpoint = urlparse(url).path
    if 'api/v2/job_statuses' not in endpoint:
        endpoint = 'api/v2/job_statuses/' + endpoint

    result = None
    while True:
        result = next(_iterate_search(endpoint, result_page_name='job_status'))

        if result['status'] in ['completed', 'failed', 'killed']:
            break

        time.sleep(sleep_time)

    return result
