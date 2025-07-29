import httpx
import asyncio
import logging
import time
import base64

class SendAPI:
    def __init__(
        self,
        url: str,
        method: str = "POST",
        params: dict = None,
        json: dict = None,
        data: dict = None,
        files: dict = None,
        headers: dict = None,
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 1.5,
        async_mode: bool = True,
        auth_type: str = None,
        token: str = None,
        username: str = None,
        password: str = None,
        on_success: callable = None,
        on_error: callable = None,
        response_handler: callable = None,
        debug: bool = False
    ):
        self.url = url
        self.method = method.upper()
        self.params = params
        self.json = json
        self.data = data
        self.files = files
        self.headers = headers or {}
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.async_mode = async_mode
        self.auth_type = auth_type
        self.token = token
        self.username = username
        self.password = password
        self.on_success = on_success
        self.on_error = on_error
        self.response_handler = response_handler
        self.debug = debug

        if debug:
            logging.basicConfig(level=logging.DEBUG)

        self._apply_auth()

    def _apply_auth(self):
        if self.auth_type == "bearer" and self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        elif self.auth_type == "basic" and self.username and self.password:
            creds = f"{self.username}:{self.password}"
            encoded = base64.b64encode(creds.encode()).decode()
            self.headers["Authorization"] = f"Basic {encoded}"

    async def _send_async(self):
        attempt = 0
        delay = self.backoff_factor
        while attempt < self.retries:
            try:
                start_time = time.time()
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(
                        self.method,
                        self.url,
                        params=self.params,
                        json=self.json,
                        data=self.data,
                        files=self.files,
                        headers=self.headers,
                    )
                duration = time.time() - start_time
                response.raise_for_status()
                result = self._parse_response(response, duration)
                if self.on_success:
                    self.on_success(result)
                return result
            except httpx.RequestError as e:
                attempt += 1
                if self.debug:
                    logging.error(f"[Attempt {attempt}] {e}")
                if attempt >= self.retries and self.on_error:
                    self.on_error(e)
                    return self._error_response(e)
                await asyncio.sleep(delay)
                delay *= self.backoff_factor

    def _send_sync(self):
        attempt = 0
        delay = self.backoff_factor
        while attempt < self.retries:
            try:
                start_time = time.time()
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.request(
                        self.method,
                        self.url,
                        params=self.params,
                        json=self.json,
                        data=self.data,
                        files=self.files,
                        headers=self.headers,
                    )
                duration = time.time() - start_time
                response.raise_for_status()
                result = self._parse_response(response, duration)
                if self.on_success:
                    self.on_success(result)
                return result
            except httpx.RequestError as e:
                attempt += 1
                if self.debug:
                    logging.error(f"[Attempt {attempt}] {e}")
                if attempt >= self.retries and self.on_error:
                    self.on_error(e)
                    return self._error_response(e)
                time.sleep(delay)
                delay *= self.backoff_factor

    def _parse_response(self, response, duration):
        try:
            content = response.json()
        except Exception:
            # fallback to text if JSON fails
            content = response.text
        
        # If user provided a custom handler, process the content through it
        if self.response_handler:
            try:
                content = self.response_handler(content)
            except Exception as e:
                if self.debug:
                    logging.error(f"Error in response_handler: {e}")
                # fallback: just keep original content
                pass

        return {
            "success": True,
            "status_code": response.status_code,
            "duration": round(duration, 4),
            "data": content,
        }

    def _error_response(self, error):
        return {
            "success": False,
            "status_code": getattr(error.response, "status_code", None),
            "duration": None,
            "error": str(error),
        }

    def send(self):
        if self.async_mode:
            # return an asyncio Task (you must await this)
            return asyncio.create_task(self._send_async())
        else:
            return self._send_sync()

    # ---------- Shortcut class methods ----------

    @classmethod
    def get(cls, url, **kwargs):
        return cls(url=url, method="GET", **kwargs).send()

    @classmethod
    def post(cls, url, **kwargs):
        return cls(url=url, method="POST", **kwargs).send()

    @classmethod
    def put(cls, url, **kwargs):
        return cls(url=url, method="PUT", **kwargs).send()

    @classmethod
    def delete(cls, url, **kwargs):
        return cls(url=url, method="DELETE", **kwargs).send()

    @classmethod
    def patch(cls, url, **kwargs):
        return cls(url=url, method="PATCH", **kwargs).send()



# import asyncio

# async def main():
#     response = await SendAPI.get(
#         url="https://jsonplaceholder.typicode.com/users",
#         retries=5,
#         timeout=2,
#         async_mode=True,
#         debug=False,
#     )
#     print(response["data"])

# asyncio.run(main())