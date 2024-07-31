import requests


class HttpService:
    def __init__(
        self,
        base_url: str = None,
        default_headers=None,
    ) -> None:
        self.base_url = base_url if base_url is not None else ""
        self.default_headers = default_headers if default_headers is not None else {}

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
    ) -> requests.Response:
        headers = (
            {**self.default_headers, **headers} if headers else self.default_headers
        )
        url = self.base_url + (endpoint or "/")
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body,
            timeout=timeout,
        )
        return response

    def request_json(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
        status_force_list=None,
        total=3,
    ):
        response = self.request(
            endpoint,
            method=method,
            params=params,
            body=body,
            headers=headers,
            timeout=timeout,
            status_force_list=status_force_list,
            total=total,
        )
        return response.json()

    def request_html(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
        status_force_list=None,
        total=3,
    ):
        response = self.request(
            endpoint,
            method=method,
            params=params,
            body=body,
            headers=headers,
            timeout=timeout,
            status_force_list=status_force_list,
            total=total,
        )
        return response.text

    def request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
        status_force_list=None,
        total=3,
    ):
        if status_force_list is None:
            status_force_list = []

        for _ in range(total):
            try:
                response = self._request(
                    endpoint,
                    method=method,
                    params=params,
                    body=body,
                    headers=headers,
                    timeout=timeout,
                )

                if response.status_code in status_force_list:
                    print(
                        f"🔄 [{response.elapsed.total_seconds() if response else None}s] {method}: {self.base_url}{endpoint} - retrying... ({_+1}) (code: wrong status_code)"
                    )
                    continue

                print(
                    f"✅ [{response.elapsed.total_seconds() if response else None}s] {method}: {self.base_url}{endpoint} - OK!"
                )

                return response
            except requests.exceptions.Timeout:
                print(
                    f"⛔️ [{timeout if timeout else None}] {method}: {self.base_url}{endpoint} - retrying... ({_+1}) (code: Timeout)"
                )
                continue
            except requests.exceptions.ConnectionError:
                print(
                    f"⛔️ [{timeout if timeout else None}] {method}: {self.base_url}{endpoint} - stopped ({_+1}) (code: ConnectionError)"
                )
                pass
        return None
