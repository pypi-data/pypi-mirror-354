import json
import time
from typing import Callable, Optional, Dict, Any
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

import requests

from prismnlq.utils import download, unzip_tar


class NLQClient:
    def __init__(self, access_token, base_url: str = "https://nlq.ap-northeast-2.prism39.com"):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.session = requests.Session()

        # Set default headers
        if access_token:
            self.session.headers.update({
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            })

    def set_token(self, access_token: str):
        """Update the access token"""
        self.access_token = access_token
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

    def _parse_sse_line(self, line: str) -> Optional[Dict[str, str]]:
        """Parse a single SSE line"""
        line = line.strip()
        if not line or line.startswith(':'):
            return None

        if line.startswith('data: '):
            return {'type': 'data', 'content': line[6:]}
        elif line.startswith('event: '):
            return {'type': 'event', 'content': line[7:]}
        elif line.startswith('id: '):
            return {'type': 'id', 'content': line[4:]}
        elif line.startswith('retry: '):
            return {'type': 'retry', 'content': line[7:]}

        return None

    def _query_with_timeout(
            self,
            prompt: str,
            model: str,
            data_type: str,
            on_status: Optional[Callable[[str, str], None]],
            on_complete: Optional[Callable[[str, str], None]],
            on_error: Optional[Callable[[str, str], None]],
            debug: bool,
            timeout: int = 300  # 5 minutes default timeout
    ) -> Any:
        """Internal query method with timeout handling"""

        if not self.access_token:
            raise ValueError("Access token not set. Use set_token() or provide token in constructor.")

        # Prepare request data
        nlq_data = {
            "prompt": prompt,
            "model": model
        }

        url = f"{self.base_url}/api/v1/nlq"

        try:
            # Make SSE request with timeout
            response = self.session.post(
                url,
                json=nlq_data,
                stream=True,
                timeout=(30, timeout),  # (connect_timeout, read_timeout)
                headers={
                    "Accept": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }
            )

            if debug:
                print(f"Response status: {response.status_code}")
                print(f"Response headers: {dict(response.headers)}")

            # Check if request was successful
            if response.status_code != 200:
                error_msg = f"Request failed with status {response.status_code}: {response.text}"
                if on_error:
                    on_error("unknown", error_msg)
                return {"error": error_msg, "status_code": response.status_code}

            # Process SSE events with improved reliability
            current_event = None
            current_data = None
            events_received = []
            last_activity_time = time.time()

            # Track if we've seen any events to detect stalled connections
            activity_timeout = 60  # 60 seconds without any data = stalled

            def process_complete_event(event_type: str, data: str):
                """Process a complete event and return result if applicable"""
                nonlocal events_received

                if debug:
                    print(f"Processing complete event: {event_type}, data: {data}")

                try:
                    parsed_data = json.loads(data)
                except json.JSONDecodeError:
                    if debug:
                        print(f"Failed to parse JSON: {data}")
                    return None

                query_id = parsed_data.get("query_id", "unknown")
                events_received.append((event_type, parsed_data))

                if event_type == "status":
                    message = parsed_data.get("message", "")
                    print(f"Status 🟢: {message}")
                    if on_status:
                        on_status(query_id, message)
                    return None

                elif event_type == "complete":
                    download_url = parsed_data.get("download_url", "")
                    print(f"Complete 🎉: Received download URL")
                    if on_complete:
                        on_complete(query_id, download_url)
                    return download_url

                elif event_type == "error":
                    error_msg = parsed_data.get("error", "Unknown error")
                    print(f"Error 🔴: {error_msg}")
                    if on_error:
                        on_error(query_id, error_msg)
                    return {
                        "status": "error",
                        "query_id": query_id,
                        "error": error_msg
                    }

                return None

            # Process the stream with smaller chunks for better real-time processing
            buffer = ""
            for chunk in response.iter_content(chunk_size=64, decode_unicode=True):
                if chunk is None:
                    continue

                # Update activity timer
                last_activity_time = time.time()
                buffer += chunk

                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.rstrip('\r')  # Remove carriage return if present

                    if debug:
                        print(f"Processing line: {repr(line)}")

                    if line == '':
                        # Empty line indicates end of event
                        if current_event and current_data:
                            result = process_complete_event(current_event, current_data)

                            if current_event == 'complete' and result is not None:
                                print(f"✅ Successfully received complete event")
                                # Handle data processing based on data_type
                                if data_type == 'url':
                                    return result  # result is the download_url
                                else:
                                    file = download(result)  # result is the download_url
                                    dfs, metadata = unzip_tar(file, data_type)
                                    order = metadata.get("order")
                                    ret = []
                                    for idx, i in enumerate(order):
                                        data_i = dfs[f"{i}.parquet"]
                                        ret.append(data_i)
                                    return ret[0] if len(ret) == 1 else ret
                            elif current_event == 'error' and result is not None:
                                return result

                            # Reset for next event
                            current_event = None
                            current_data = None
                        continue

                    parsed = self._parse_sse_line(line)
                    if parsed is None:
                        continue

                    if parsed['type'] == 'event':
                        current_event = parsed['content']
                    elif parsed['type'] == 'data':
                        current_data = parsed['content']

                # Check for activity timeout
                if time.time() - last_activity_time > activity_timeout:
                    print(f"⚠️ No activity for {activity_timeout} seconds, connection may be stalled")
                    break

            # Process any remaining event after stream ends
            if current_event and current_data:
                print(f"📝 Processing final event: {current_event}")
                result = process_complete_event(current_event, current_data)

                if current_event == 'complete' and result is not None:
                    print(f"✅ Successfully processed final complete event")
                    if data_type == 'url':
                        return result
                    else:
                        file = download(result)
                        dfs, metadata = unzip_tar(file, data_type)
                        order = metadata.get("order")
                        ret = []
                        for idx, i in enumerate(order):
                            data_i = dfs[f"{i}.parquet"]
                            ret.append(data_i)
                        return ret[0] if len(ret) == 1 else ret
                elif current_event == 'error' and result is not None:
                    return result

            # Debug information about what we received
            print(f"🔍 Events received: {len(events_received)}")
            for i, (event_type, data) in enumerate(events_received):
                print(f"  {i + 1}. {event_type}: {data.get('message', data.get('error', 'Unknown'))}")

            # If we get here without a complete event, something went wrong
            return {
                "error": "No complete event received",
                "events_received": len(events_received),
                "last_event": events_received[-1] if events_received else None
            }

        except requests.exceptions.Timeout:
            error_msg = f"Request timed out after {timeout} seconds"
            print(f"⏰ {error_msg}")
            if on_error:
                on_error("unknown", error_msg)
            return {"error": error_msg}
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"🔌 {error_msg}")
            if on_error:
                on_error("unknown", error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"💥 {error_msg}")
            if on_error:
                on_error("unknown", error_msg)
            return {"error": error_msg}

    def query(
            self,
            prompt: str,
            model: str = "claude-3-5-sonnet-20241022",
            data_type: str = "pandas",
            on_status: Optional[Callable[[str, str], None]] = None,
            on_complete: Optional[Callable[[str, str], None]] = None,
            on_error: Optional[Callable[[str, str], None]] = None,
            debug: bool = False,
            max_retries: int = 3,
            timeout: int = 300
    ) -> Any:
        """
        Send NLQ request with retry logic and timeout handling

        Args:
            prompt: The natural language query
            model: The AI model to use
            data_type: The data type to use ('pandas', 'url', etc.)
            on_status: Callback for status updates (query_id, message)
            on_complete: Callback for completion (query_id, download_url)
            on_error: Callback for errors (query_id, error_message)
            debug: Enable debug output
            max_retries: Maximum number of retry attempts
            timeout: Timeout in seconds for the entire request

        Returns:
            - If successful: The processed data (DataFrame for 'pandas', URL for 'url', etc.)
            - If error: Dictionary with error information
        """

        for attempt in range(max_retries + 1):
            if attempt > 0:
                wait_time = min(2 ** attempt, 10)  # Exponential backoff, max 10 seconds
                print(f"🔄 Retry attempt {attempt}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)

            try:
                result = self._query_with_timeout(
                    prompt, model, data_type, on_status, on_complete, on_error, debug, timeout
                )

                # Check if we got a successful result
                if not isinstance(result, dict) or "error" not in result:
                    return result

                # If it's an error, check if it's retryable
                error_msg = result.get("error", "")
                if any(retryable in error_msg.lower() for retryable in [
                    "no complete event received",
                    "timeout",
                    "connection",
                    "network"
                ]):
                    if attempt < max_retries:
                        print(f"⚠️ Retryable error: {error_msg}")
                        continue

                # Non-retryable error or max retries reached
                return result

            except Exception as e:
                error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
                print(f"💥 {error_msg}")
                if attempt == max_retries:
                    return {"error": error_msg}

        return {"error": f"Failed after {max_retries + 1} attempts"}