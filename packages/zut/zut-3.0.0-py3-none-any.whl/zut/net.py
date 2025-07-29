import json
import logging
import re
import socket
import ssl
import struct
from http.client import HTTPResponse
from io import IOBase
from ipaddress import AddressValueError, IPv4Address, IPv6Address, ip_address
from threading import Thread
from time import sleep, time
from typing import Any, MutableMapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import (ParseResult, quote, quote_plus, unquote, urlencode,
                          urlparse, urlunparse)
from urllib.request import Request, urlopen

from zut import DelayedStr, get_logger
from zut.json import ExtendedJSONEncoder

_logger = get_logger(__name__)


#region URLs

def build_url(result: ParseResult|None = None, *, scheme: str = '', hostname: str|IPv4Address|IPv6Address|None = None, port: int|None = None, username: str|None = None, password: str|DelayedStr|None = None, path: str|None = None, params: str|None = None, query: str|None = None, fragment: str|None = None, noquote = False, hide_password = False):
    if result:
        if scheme == '' and result.scheme:
            scheme = result.scheme
        if hostname is None and result.hostname is not None:
            hostname = unquote(result.hostname)
        if port is None and result.port is not None:
            port = result.port
        if username is None and result.username is not None:
            username = unquote(result.username)
        if password is None and result.password is not None:
            password = unquote(result.password)
        if path is None and result.path is not None:
            path = unquote(result.path)
        if params is None and result.params is not None:
            params = unquote(result.params)
        if query is None and result.query is not None:
            query = unquote(result.query)
        if fragment is None and result.fragment is not None:
            fragment = unquote(result.fragment)

    netloc = build_netloc(hostname=hostname, port=port, username=username, password=password, noquote=noquote, hide_password=hide_password)

    if noquote:
        actual_query = query
    else:
        if isinstance(query, dict):
            actual_query = urlencode(query)
        elif isinstance(query, list):
            named_parts = []
            unnamed_parts = []
            for part in query:
                if isinstance(part, tuple):
                    named_parts.append(part)
                else:
                    unnamed_parts.append(part)
            actual_query = urlencode(named_parts, quote_via=quote_plus)
            actual_query += ('&' if actual_query else '') + '&'.join(quote_plus(part) for part in unnamed_parts)
        else:
            actual_query = query

    return urlunparse((scheme or '', netloc or '', (path or '') if noquote else quote(path or ''), (params or '') if noquote else quote_plus(params or ''), actual_query or '', (fragment or '') if noquote else quote_plus(fragment or '')))


def build_netloc(*, hostname: str|IPv4Address|IPv6Address|None = None, port: int|None = None, username: str|None = None, password: str|DelayedStr|None = None, noquote = False, hide_password = False):
    netloc = ''
    if username or hostname:
        if username:
            netloc += username if noquote else quote_plus(username)
            password = DelayedStr.ensure_value(password)
            if password:
                if hide_password:
                    password = '***'
                else:
                    if not noquote:
                        password = quote_plus(password) # type: ignore
                netloc += f':{password}'
            netloc += '@'

        if hostname:
            if isinstance(hostname, IPv4Address):
                netloc += hostname.compressed
            elif isinstance(hostname, IPv6Address):
                netloc += f"[{hostname.compressed}]"
            else:
                ipv6 = None
                if ':' in hostname:
                    try:
                        ipv6 = IPv6Address(hostname)
                    except AddressValueError:
                        pass

                if ipv6:
                    netloc += f"[{ipv6.compressed}]"
                else:
                    netloc += hostname if noquote else quote_plus(hostname)

            if port:
                if not (isinstance(port, int) or (isinstance(port, str) and re.match(r'^\d+$', port))):
                    raise ValueError(f"invalid type for port: {type(port)}")
                netloc += f':{port}'
    elif port:
        raise ValueError("Argument 'port' cannot be given without a hostname")
    elif password:
        raise ValueError("Argument 'password' cannot be given without a username")

    return netloc


def hide_url_password(url: str, *, always_password = False):
    r = urlparse(url)
    password = r.password
    if not password and always_password:
        password = '***'
    return build_url(scheme=r.scheme, hostname=r.hostname, port=r.port, username=r.username, password=password, path=r.path, params=r.params, query=r.query, fragment=r.fragment, noquote=True, hide_password=True)

#endregion


#region Network

def get_host_ip() -> str:
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_linux_default_gateway_ip(iface: str|None = None):
    with open("/proc/net/route") as fp:
        for line in fp:
            fields = line.strip().split()
            
            if iface and fields[0] != iface:
                continue

            if fields[1] != '00000000' or not int(fields[3], 16) & 2: # if not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def resolve_host(host: str, *, timeout: float|None = None, ip_version: int|None = None) -> list[str]:
    """
    Make a DNS resolution with a timeout.
    """
    try:
        # If host is already an ip address, return it
        ip = ip_address(host)
        if not ip_version or ip.version == ip_version:
            return [ip.compressed]
    except ValueError:
        pass
    
    if ip_version is None:
        family = 0
    elif ip_version == 4:
        family = socket.AddressFamily.AF_INET
    elif ip_version == 6:
        family = socket.AddressFamily.AF_INET6
    else:
        raise ValueError(f"Invalid ip version: {ip_version}")

    addresses = []
    exception = None

    def target():
        nonlocal addresses, exception
        try:
            for af, socktype, proto, canonname, sa in socket.getaddrinfo(host, port=0, family=family):
                addresses.append(sa[0])
        except BaseException as err:
            exception = err

    if timeout is not None:
        thread = Thread(target=target, daemon=True)
        thread.start()
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError(f"Name resolution for host \"{host}\" timed out")

    else:
        target()

    if exception:
        err = NameError(str(exception))
        err.name = host
        raise err
        
    return addresses


_wpad_proxy = None
_wpad_proxy_requested = False

def get_wpad_proxy(*, timeout: float = 1.0) -> str|None:
    global _wpad_proxy, _wpad_proxy_requested
    if _wpad_proxy_requested:
        return _wpad_proxy
    
    try:
        wpad_ip = resolve_host('wpad', timeout=1)[0]
    except Exception as err: #timeout or out of range
        _logger.debug("wpad resolution: %s", err)
        _wpad_proxy = None
        _wpad_proxy_requested = True
        return _wpad_proxy
    
    wpad_url = f"http://{wpad_ip}/wpad.dat"
    
    request = Request(wpad_url)
    response: HTTPResponse
    try:
        with urlopen(request, timeout=timeout) as response:
            _logger.debug("WPAD response: %s %s - Content-Type: %s", response.status, response.reason, response.headers.get('Content-Type'))
            body = response.read().decode('utf-8')
    except HTTPError as err:
        _logger.error(f"Cannot retrieve WPAD: HTTP {err.status} {err.reason}")
        _wpad_proxy = None
        _wpad_proxy_requested = True
        return _wpad_proxy
    except URLError as err:
        _logger.error(f"Cannot retrieve WPAD: {err.reason}")
        _wpad_proxy = None
        _wpad_proxy_requested = True
        return _wpad_proxy
    
    _wpad_proxy = None
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith('//') or line in {'{', '}', 'function FindProxyForURL(url, host)'}:
            continue
        else:
            m = re.match(r'^return\s*"PROXY\s*(?P<host>[^\s"\:]+)\:(?P<port>\d+)".*', line, re.IGNORECASE)
            if m:
                _wpad_proxy = f"http://{m['host']}:{m['port']}"
                break
    
    _wpad_proxy_requested = True
    return _wpad_proxy


def check_host_port(hostport: tuple[str,int]|list[tuple[str,int]], *, timeout: float|None = None) -> tuple[str,int]|None:
    """
    Check whether at least one of the given host and port is open.

    If yes, return the first opened (host, port). Otherwise return None.
    """
    if isinstance(hostport, tuple):
        hostport = [hostport]

    opened: list[tuple[str,int]] = []

    def target(host: str, port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            if result == 0:
                _logger.debug("Host %s, port %s: opened", host, port)
                opened.append((host, port))
            else:
                _logger.debug("Host %s, port %s: NOT opened", host, port)
            sock.close()
        except Exception as err:
            _logger.debug("Host %s, port %s: %s", host, port, err)

    threads: list[Thread] = []
    for host, port in hostport:
        thread = Thread(target=target, args=[host, port], daemon=True)
        thread.start()
        threads.append(thread)

    # Wait for all threads
    if timeout is not None:
        stop_time = time() + timeout
        while time() < stop_time:
            if any(t.is_alive() for t in threads):
                sleep(0.1)
            else:
                break
    else:
        for thread in threads:
            thread.join()

    # Return
    if opened:
        return opened[0]
    else:
        return None

#endregion


#region API client

class ApiClient:
    """
    A JSON API client using only Python standard library.
    """

    base_url : str|None = None
    timeout: float|None = None
    """ Timeout in seconds. """

    force_trailing_slash: bool = False

    default_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json; charset=utf-8',
    }

    json_encoder_cls: type[json.JSONEncoder] = ExtendedJSONEncoder
    json_decoder_cls: type[json.JSONDecoder] = json.JSONDecoder
    
    print_error_maxlen = 400

    no_ssl_verify = False


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # necessary to allow this class to be used as a mixin
        self._logger = get_logger(type(self).__module__ + '.' + type(self).__name__)
        self._ssl_context = None
        if self.no_ssl_verify or kwargs.get('no_ssl_verify'):
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE


    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        pass


    def get(self, endpoint: str|None = None, *, params: dict|None = None, headers: MutableMapping[str,str]|None = None):
        return self.request(endpoint, method='GET', params=params, headers=headers)


    def post(self, endpoint: str|None = None, data = None, *, params: dict|None = None, headers: MutableMapping[str,str]|None = None, content_type: str|None = None, content_length: int|None = None, content_filename: str |None= None):
        return self.request(endpoint, data, method='POST', params=params, headers=headers, content_type=content_type, content_length=content_length, content_filename=content_filename)
    

    def put(self, endpoint: str|None = None, data = None, *, params: dict|None = None, headers: MutableMapping[str,str]|None = None, content_type: str|None = None, content_length: int|None = None, content_filename: str |None= None):
        return self.request(endpoint, data, method='PUT', params=params, headers=headers, content_type=content_type, content_length=content_length, content_filename=content_filename)
   

    def request(self, endpoint: str|None = None, data = None, *, method = None, params: dict|None = None, headers: MutableMapping[str,str]|None = None, content_type: str|None = None, content_length: int|None = None, content_filename: str|None = None) -> dict[str,Any]:
        url = self.prepare_url(endpoint, params=params)

        all_headers = self.get_request_headers(url)
        if headers:
            for key, value in headers.items():
                all_headers[key] = value
                if key == 'Content-Type' and not content_type:
                    content_type = value
                elif key == 'Content-Length' and content_length is None:
                    content_length = int(value) if isinstance(value, str) else value
                elif key == 'Content-Disposition' and not content_filename:
                    m = re.search(r'attachment\s*;\s*filename\s*=\s*(.+)', value)
                    if m:
                        content_filename = m[1].strip()

        if content_type:
            all_headers['Content-Type'] = content_type
        if content_length is not None:
            all_headers['Content-Length'] = str(content_length)
        if content_filename:
            all_headers['Content-Disposition'] = f"attachment; filename={content_filename}"
                
        if data is not None:
            if not method:
                method = 'POST'

            if isinstance(data, IOBase) or (content_type and not 'application/json' in content_type):
                # keep data as is: this is supposed to be an uploaded file
                if not content_type:
                    content_type = 'application/octet-stream'
            else:
                data = json.dumps(data, ensure_ascii=False, cls=self.json_encoder_cls).encode('utf-8')
            
            self._logger.debug('%s %s', method, url)
            request = Request(url,
                method=method,
                headers=all_headers,
                data=data,
            )
        else:
            if not method:
                method = 'GET'
            
            self._logger.debug('%s %s', method, url)
            request = Request(url,
                method=method,
                headers=all_headers,
            )

        try:
            response: HTTPResponse
            with urlopen(request, timeout=self.timeout, context=self._ssl_context) as response:
                if self._logger.isEnabledFor(logging.DEBUG):
                    content_type = response.headers.get('content-type', '-')
                    self._logger.debug('%s %s %s %s', response.status, url, response.length, content_type)
                return self.get_dict_response(response)
            
        except HTTPError as error:
            with error:
                http_data = self.get_dict_or_str_response(error)
            raise ApiClientError(error, http_data, message_maxlen=self.print_error_maxlen) from None

        except Exception as error:
            raise ApiClientError(error, message_maxlen=self.print_error_maxlen) from None


    def prepare_url(self, endpoint: str|None, *, params: dict|None = None, base_url: str|None = None):
        if endpoint is None:
            endpoint = ''

        if not base_url and self.base_url:
            base_url = self.base_url

        if '://' in endpoint or not base_url:
            url = endpoint
            
        else:            
            if endpoint.startswith('/'):
                if base_url.endswith('/'):                    
                    endpoint = endpoint[1:]
            else:
                if not base_url.endswith('/') and endpoint:
                    endpoint = f'/{endpoint}'
            
            if self.force_trailing_slash and not endpoint.endswith('/'):
                endpoint = f'{endpoint}/'

            url = f'{base_url}{endpoint}'

        if params:
            url += "?" + urlencode(params)
        
        return url
    

    def get_request_headers(self, url: str) -> MutableMapping[str,str]:
        headers = {**self.default_headers}
        return headers


    def get_dict_or_str_response(self, response: HTTPResponse|HTTPError) -> dict|str:
        result = self._decode_response(response)
        if isinstance(result, Exception):
            return str(result)
        return result


    def get_dict_response(self, response: HTTPResponse|HTTPError) -> dict:
        result = self._decode_response(response)
        if isinstance(result, Exception):
            raise result from None        
        return result


    def _decode_response(self, response: HTTPResponse|HTTPError) -> dict|Exception:
        rawdata = response.read()
        try:
            strdata = rawdata.decode('utf-8')
        except UnicodeDecodeError:
            strdata = str(rawdata)
            return ApiClientError("Invalid UTF-8", strdata, message_maxlen=self.print_error_maxlen)
        
        try:
            result = json.loads(strdata, cls=self.json_decoder_cls)
        except json.JSONDecodeError:
            return ApiClientError("Not JSON", strdata, message_maxlen=self.print_error_maxlen)
        
        if not isinstance(result, dict):
            return ApiClientError("Not dict", strdata, message_maxlen=self.print_error_maxlen)
        
        return result
        

class ApiClientError(Exception):
    def __init__(self, error: str|Exception, data: dict|str|None = None, *, message_maxlen: int|None = 400):
        self.prefix: str
        self.code_nature: str|None = None
        self.code: int|None = None

        if isinstance(error, HTTPError):
            self.prefix = error.reason
            self.code = error.status
            self.code_nature = 'status'
        elif isinstance(error, URLError):
            self.prefix = str(error.reason) if not isinstance(error.reason, str) else error.reason
            self.code = error.errno
            self.code_nature = 'errno'
        elif isinstance(error, str):
            self.prefix = error
        else:
            self.prefix = f"[{type(error).__name__}] {error}"

        self.data = data
        self.message_maxlen = message_maxlen
        super().__init__(self._prepare_message())


    def _prepare_message(self):
        message = self.prefix

        if self.code:
            message = (message + ' ' if message else '') + f"[{self.code_nature or 'code'}: {self.code}]"
        
        if self.data:
            if isinstance(self.data, dict):
                for key, value in self.data.items():
                    message = (message + '\n' if message else '') + f"{key}: {value}"
            else:
                message = (message + '\n' if message else '') + str(self.data)

        self.full_message = message
    
        if self.message_maxlen is not None and len(self.full_message) > self.message_maxlen:
            return self.full_message[0:self.message_maxlen] + '…'
        else:
            return self.full_message

#endregion
