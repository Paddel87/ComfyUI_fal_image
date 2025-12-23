import time
import json
import requests
from typing import Tuple, Dict, Any

QUEUE_BASE = 'https://queue.fal.run'

class FalClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _headers(self):
        return {
            'Authorization': f'Key {self.api_key}',
            'Content-Type': 'application/json'
        }

    def submit(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f'{QUEUE_BASE}/{model_id}'
        resp = requests.post(url, headers=self._headers(), data=json.dumps(payload), timeout=30)
        if resp.status_code >= 400:
            raise RuntimeError(f'Submit failed: {resp.status_code} {resp.text}')
        return resp.json()

    def status(self, model_id: str, request_id: str, logs: bool = True) -> Dict[str, Any]:
        url = f'{QUEUE_BASE}/{model_id.split("/")[0]}/{model_id.split("/")[1]}/requests/{request_id}/status'
        params = {'logs': 1} if logs else {}
        resp = requests.get(url, headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def result(self, model_id: str, request_id: str) -> Dict[str, Any]:
        url = f'{QUEUE_BASE}/{model_id.split("/")[0]}/{model_id.split("/")[1]}/requests/{request_id}'
        resp = requests.get(url, headers=self._headers(), timeout=60)
        resp.raise_for_status()
        return resp.json()

    def run_with_polling(self, model_id: str, payload: Dict[str, Any], timeout_sec: int, retries: int) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        last_error = None
        attempt = 0
        while attempt <= retries:
            try:
                submit_resp = self.submit(model_id, payload)
                req_id = submit_resp.get('request_id') or submit_resp.get('gateway_request_id')
                if not req_id:
                    raise RuntimeError('No request_id returned')
                start = time.time()
                while True:
                    st = self.status(model_id, req_id, logs=True)
                    if st.get('status') == 'COMPLETED':
                        res = self.result(model_id, req_id)
                        return res, req_id, st
                    if st.get('status') == 'ERROR':
                        raise RuntimeError(f'Queue error: {st}')
                    if time.time() - start > timeout_sec:
                        raise TimeoutError('Timeout waiting for result')
                    time.sleep(0.8)
            except Exception as e:
                last_error = e
                time.sleep(min(2 ** attempt, 5))
                attempt += 1
        raise RuntimeError(f'Retries exhausted: {last_error}')

