#!/usr/bin/env python3
#
# Maubot server sanity checker
# ©Sebastian Spaeth & contributors
# SPDX-License-Identifier: AGPL-3.0-or-later

import argparse
import logging
import requests
import sys
from os import urandom
from typing import Optional, Any

class JWTAuth:
    """A JWT Auth server"""
    def __init__(self, baseurl: str):
        self.baseurl = baseurl

    def test_health(self) -> bool:
        assert self.baseurl, "JWT baseurl not yet set"
        try:
            url = f"{self.baseurl}/healthz"
            r = requests.get(url, headers = MatrixServer.req_headers)
        except requests.exceptions.ConnectionError as e:
            if ("[Errno 11001] getaddrinfo failed" in str(e) or     # Windows
                "[Errno -2] Name or service not known" in str(e) or # Linux
                "[Errno 8] nodename nor servname " in str(e)):      # OS X
                s = f"𐄂 DNS Error resolving host {self.baseurl}"
                logging.error(s)
        else:
            logging.debug("  JWTauth healtz url: %s", self.baseurl)
            if r.status_code == 404:
                logging.warning("𐄂 jwtauth healthz endpoint does not exist at %s (404)", url)
            elif r.status_code != 200:
                logging.error("𐄂 jwtauth healthz http error %s",
                              r.status_code)
            else:
                #status code 200, all is well!
                if not "Access-Control-Allow-Origin" in r.headers:
                    logging.debug("  jwt has no CORS header (that is OK)")
                logging.info("✔ JWTauth responds")
                return True
        return False

    def test_sfuget(self, mserver: Optional['MatrixServer'] = None,
                    token: Optional[str] = None):
        """token is the Openid token"""
        res = True

        # First test as unauthed user
        try:
            url = f"{self.baseurl}/sfu/get"
            r = requests.get(url, headers = MatrixServer.req_headers)
        except requests.exceptions.ConnectionError as e:
            # 1) Windows 2) # Linux 3) # OS X
            if ("[Errno 11001] getaddrinfo failed" in str(e) or
                "[Errno -2] Name or service not known" in str(e) or
                "[Errno 8] nodename nor servname " in str(e)):
                s = f"𐄂 DNS Error resolving host {self.baseurl}"
                logging.error(s)
                res = False
        else:
            if not "Access-Control-Allow-Origin" in r.headers:
                logging.debug("  jwt has no CORS header (that is OK)")
            if r.status_code == 405:
                logging.debug("✔ jwt /sfu/get without auth returns (405). This is good!")
            else:
                logging.error("𐄂 jwt /sfu/get without aut returns (%d)",
                              r.status_code)
                res = False

        if not res:
            logging.warning("𐄂 jwt /sfu/get (unauth) failed (BAD), not trying anything else")
            return res
        elif not (mserver and token):
            logging.debug("  jwt: no credentials passed, not trying authed requests")
            return res

        # Next, test as authed user
        data = {"room":"!DFGDFG:cloud.de",
                "openid_token":
                  {"access_token": token,
                   "expires_in":3600,
                   "matrix_server_name": mserver.servername,
                   "token_type":"Bearer"},
                  "device_id":"1234"}
        try:
            url = f"{self.baseurl}/sfu/get"
            r = requests.post(url, headers = MatrixServer.req_headers,
                              json=data)
        except requests.exceptions.ConnectionError as e:
            if ("[Errno 11001] getaddrinfo failed" in str(e) or     # Windows
                "[Errno -2] Name or service not known" in str(e) or # Linux
                "[Errno 8] nodename nor servname " in str(e)):      # OS X
                s = f"𐄂 DNS Error resolving host {self.baseurl}"
                logging.error(s)
                res = False
        else:
            if r.status_code != 200:
                logging.error("𐄂 /sfu/get (auth) returned unexpected result (%d): %s", r.status_code, r.text)
                return False
            # YAY! success
            s="✔ /sfu/get succeeded. Use the below information to test your livekit SFU on https://livekit.io/connection-test\n  %s"
            logging.info(s, r.text)
        return res


#-----------------------------------------------------------------------
class MatrixServer:
    """
    A Matrix server (that we want to test)

    notable instance attributes:
        .servername
        .federation_baseurl
        .client_baseurl
        .livekits: list of livekit JWTAuth servers (or None)
    """
    livekits: Optional[list[JWTAuth]] = None # overriden by instance
    req_headers = {"User-Agent": "Mozilla/5.0 (Linux; x64)"}
    # suppress overly verbose python requests logging
    logging.getLogger("urllib3").setLevel(logging.INFO)

    def __init__(self, servername: str,
                 args: Optional[argparse.Namespace] = None) -> None:
        self.args = args
        self.servername: str = servername
        self.federation_baseurl: Optional[str] = None
        self.client_baseurl: Optional[str] = None
        self.livekits: Optional[list[JWTAuth]]

    @staticmethod
    def get_mxid_localpart(mxid: str):
        """Return the localpart of a full MXID"""
        if mxid[0] != "@":
            raise ValueError("MXID '{mxid}' does not start with @")
        return mxid[1:].split(':')[0]

    @staticmethod
    def get_mxid_servername(mxid: str):
        """Return the servername of a full MXID"""
        return mxid.split(':')[1]

    def parse_livekit_json(self, livekit_json: Optional[list]) \
            -> Optional[bool]:
        """Parses client well-known livekit parts and initiates self.livekits

        Returns True (success), False (no Livekit) or None (Error)"""
        self.livekits = []
        if livekit_json is None:
            self.livekits = None
            return False
        #json of wellknown_client["org.matrix.msc4143.rtc_foci"]
        for livekit in livekit_json:
            if type(livekit) != dict:
                logging.error("𐄂 well-known livekit entry is no array of dicts but a %s ?! Fishy", type(livekit))
                return None
            if not "type" in livekit or livekit["type"]!="livekit":
                logging.info("𐄂 You got a non-Livekit SFU configured (type "
                              "'%s' !='livekit') ?!", livekit.get("type", ""))
                continue
            if not "livekit_service_url" in livekit:
                logging.info("𐄂 MatrixRTC SFU misses livekit_service_url")
                continue
            self.livekits.append(JWTAuth(livekit["livekit_service_url"]))
        return len(self.livekits) > 0

    def get_server_baseurl(self, quiet:bool=False) -> Optional[str]:
        """Queries federation endpoint base URL

        Returns and also stores the resulting baseurl in self.server_baseurl
        This should not be throwing exceptions, but returns None in case of
        failure"""
        wellknown_server = None
        try:
            url = f"https://{self.servername}/.well-known/matrix/server"
            r = requests.get(url, headers = MatrixServer.req_headers)
            r.raise_for_status() # raise e.g. on 404
            wellknown_server = r.json()
        except requests.exceptions.ConnectionError as e:
            if ("[Errno 11001] getaddrinfo failed" in str(e) or     # Windows
                "[Errno -2] Name or service not known" in str(e) or # Linux
                "[Errno 8] nodename nor servname " in str(e)):      # OS X
                s = f"DNS Error resolving host {self.servername}"
                logging.error(s)
                self.federation_baseurl = None
                return self.federation_baseurl
        except requests.exceptions.HTTPError as e:
            if not quiet:
                if e.response.status_code == 404:
                    logging.warning("𐄂 No server well-known exists (404)")
                else:
                    logging.error("𐄂 Server well-known error %s", str(e))
        except requests.exceptions.JSONDecodeError as e:
            if not quiet:
                logging.error("𐄂 Server well known is no valid json")
        else:
            self.federation_baseurl = "https://" + wellknown_server["m.server"]
            if not quiet:
                logging.debug("  Federation url: %s", self.federation_baseurl)
                logging.info("✔ Server well-known exists")

        # use default address in case of failed well-known
        if self.federation_baseurl is None:
            self.federation_baseurl = f"https://{self.servername}:8448"
            if not quiet:
                logging.info("  Assuming federation url: %s", self.federation_baseurl)

        return self.federation_baseurl


    def get_client_baseurl(self, quiet:bool = False) -> Optional[str]:
        """Queries client endpoint base URL

        Returns and also stores the resulting baseurl in self.client_baseurl
        This should not be throwing exceptions, but returns None in case of
        failure"""
        wellknown_client: dict = {}
        self.client_baseurl = None
        try:
            url = f"https://{self.servername}/.well-known/matrix/client"
            r = requests.get(url, headers = MatrixServer.req_headers)
            r.raise_for_status() # raise e.g. on 404
            if not quiet and not "Access-Control-Allow-Origin" in r.headers:
                logging.error("𐄂 Client well-known has no CORS header")
            elif not quiet and r.headers["Access-Control-Allow-Origin"] != "*":
                logging.error("𐄂 Client well-known has no proper CORS header: '%s'",
                              r.headers["Access-Control-Allow-Origin"])
            elif not quiet:
                logging.info("✔ Client well-known exists and has proper CORS header")
            wellknown_client = r.json()
        except requests.exceptions.ConnectionError as e:
            if ("[Errno 11001] getaddrinfo failed" in str(e) or     # Windows
                "[Errno -2] Name or service not known" in str(e) or # Linux
                "[Errno 8] nodename nor servname " in str(e)):      # OS X
                s = f"DNS Error resolving host {self.servername}"
                logging.error(s)
                return self.client_baseurl
        except requests.exceptions.HTTPError as e:
            if not quiet and e.response.status_code == 404:
                logging.warning("𐄂 No client well-known exists (404)")
            elif not quiet:
                logging.error("𐄂 Client well-known error %s", str(e))
        except requests.exceptions.JSONDecodeError as e:
            if not quiet:
                logging.error("𐄂 Client well known is no valid json")
        else:
            self.client_baseurl = wellknown_client["m.homeserver"]["base_url"]
            if not quiet: logging.debug("  Client url: %s", self.client_baseurl)

        if self.client_baseurl is None:
            # use default address in case of previous error
            self.client_baseurl = f"https://{self.servername}"
            if not quiet: logging.info("  Assuming client url: %s", self.client_baseurl)

        # Retrieve array of livekit instances or None
        livekit_json = wellknown_client.get("org.matrix.msc4143.rtc_foci",
                                            None)
        self.parse_livekit_json(livekit_json)
        return self.client_baseurl

    def get_server_version(self, quiet:bool=False) -> str:
        try:
            url = f"{self.federation_baseurl}/_matrix/federation/v1/version"
            r = requests.get(url, headers = MatrixServer.req_headers)
            r.raise_for_status() # raise e.g. on 404
            server_version = r.json()
            if not quiet and not "Access-Control-Allow-Origin" in r.headers:
                logging.error("𐄂 Server version endpoint has no CORS header")
            elif not quiet and r.headers["Access-Control-Allow-Origin"] != "*":
                logging.error("𐄂 Server version endpoint has no proper CORS header: '%s'", r.headers["Access-Control-Allow-Origin"])
        except requests.exceptions.HTTPError as e:
            if not quiet:
                if e.response.status_code == 404:
                    logging.warning("𐄂 No server version document exists (404)")
                else:
                    logging.error("𐄂 Server version error %s", str(e))
            return ""
        except requests.exceptions.JSONDecodeError as e:
            if not quiet:
                logging.error("𐄂 Server version response is no valid json")
            return ""

        # server_version is "server" dict with a dict "name", "version".
        server_version = server_version.get("server", None)
        if not quiet:
            logging.info("✔ Server version: %s (%s)", server_version["name"],
                         server_version["version"])
            logging.info("✔ Federation API endpoints seem to work fine")

        return f"{server_version['name']} ({server_version['version']})"

    def test_client_endpoint(self, quiet: bool = False) -> bool:
        """Tests a client endpoint to see if that works well"""
        res = True # Success result
        try:
            url = f"{self.client_baseurl}/_matrix/client/versions"
            r = requests.get(url, headers = MatrixServer.req_headers)
            r.raise_for_status() # raise e.g. on 404
            client_version = r.json()
            if not quiet and not "Access-Control-Allow-Origin" in r.headers:
                logging.error("𐄂 Client version endpoint has no CORS header")
            elif not quiet and r.headers["Access-Control-Allow-Origin"] != "*":
                logging.error("𐄂 Client version endpoint has no proper CORS header: '%s'", r.headers["Access-Control-Allow-Origin"])
        except requests.exceptions.HTTPError as e:
            if not quiet:
                if e.response.status_code == 404:
                    logging.warning("𐄂 No Client versions document exists (404)")
                else:
                    logging.error("𐄂 Client versions document error %s", str(e))
            res = False
        except requests.exceptions.JSONDecodeError as e:
            if not quiet:
                logging.error("𐄂 Client version response is no valid json")
            res = False
        if res and not quiet:
            logging.info("✔ Client API endpoints seem to work fine")
        elif not quiet:
            logging.info("𐄂 Client API endpoint problem (no versions document)")
        return res

    def get_user_openid_token(self) -> Optional[str]:
        """POST /_matrix/client/v3/user/{userId}/openid/request_token"""
        assert self.args and "user" in self.args and "token" in self.args, \
            "No user and token credentials"
        assert self.client_baseurl, "client base url not yet determined"

        try:
            url = f"{self.client_baseurl}/_matrix/client/v3/user/{self.args.user}/openid/request_token"
            headers = {"Authorization": f"Bearer {self.args.token}"}
            headers.update(MatrixServer.req_headers)
            data: dict = {}
            r = requests.post(url, json = data, headers = headers)
            r.raise_for_status() # raise e.g. on 404
            response = r.json()
        except requests.exceptions.HTTPError as e:
            logging.error("Error when trying to retrieve a user Openid token, response was %s", r.text)
            raise e
        else:
            # Success, return openid access token
            return response.get("access_token", None)

    def test_rtc(self) -> bool:
        """Test MatrixRTC setup"""
        assert self.client_baseurl is not None, "need to call get_client_baseurl before"
        res = True
        rtcuserServer: Optional[MatrixServer] = None
        openid_token = None # only unauth testing if we don't get one

        if self.livekits:
            logging.info("✔ MatrixRTC SFU configured")
        else:
            logging.info("  No MatrixRTC SFU configured")

        if self.args is None or self.args.user is None or self.args.token is None:
            # No credentials given, only testing unauthed request
            rtcuserServer = None
        else:
            # retrieve valid openid token
            # Retrieve a valid user's openid token for use with the jwt service
            m_server = MatrixServer.get_mxid_servername(self.args.user)
            rtcuserServer = MatrixServer(m_server, args=self.args)
            rtcuserServer.get_server_baseurl(quiet=True)
            rtcuserServer.get_client_baseurl(quiet=True)
            openid_token = rtcuserServer.get_user_openid_token()
            logging.debug("  OpenID token to use for jwt is %s", openid_token)

        if self.livekits is None:
            return True # nothing to do

        for jwtauth in self.livekits:
            if not jwtauth.test_health():
                res = False
            if not jwtauth.test_sfuget(mserver = rtcuserServer,
                                       token = openid_token):
                res = False
        return res

    def test_open_reg(self) -> bool:
        """Tests if the server is open for registration and complain

        We don't do very deep testing though.
        returns False if open registration or guest access seems possible"""
        assert self.client_baseurl, "client base url not yet determined"
        res = True
        r: Optional[requests.Response]= None
        try:
            url = f"{self.client_baseurl}/_matrix/client/v3/register"
            data: dict = {'password':'1234',
                          'username': str(urandom(12).hex())}
            r = requests.post(url, json = data, headers = MatrixServer.req_headers)
            r.raise_for_status() # raise e.g. on 403
        except requests.exceptions.HTTPError as e:
            if r is not None and r.status_code != 403:
                logging.warning("𐄂 Direct open registration might not be forbidden!")
                res = False
        # Next test for guest access
        try:
            url = f"{self.client_baseurl}/_matrix/client/v3/register"
            params: dict = {'kind':'guest'}
            data = {'password':'1234',
                          'username': str(urandom(12).hex())}
            r = requests.post(url, params = params, json = data,
                              headers = MatrixServer.req_headers)
        except requests.exceptions.HTTPError as e:
            pass
        if r is not None and r.status_code != 403:
            logging.warning("𐄂 Guest access might not be forbidden (returned %d)!",
                            r.status_code)
            res = False
        if res:
            logging.debug("✔ Direct registration and guest access forbidden per se 👍")
        return res

    def test(self) -> bool:
        logging.debug("Testing server %s", self.servername)
        if self.get_server_baseurl() is None:
            return False
        self.get_client_baseurl()
        self.get_server_version()
        self.test_client_endpoint()
        self.test_rtc()
        self.test_open_reg()
        return True


def handle_cmd_opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # no debug output
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-u', '--user', metavar='MXID', help=
                        """user for the MatrixRTC testing, either as
                        @USER:DOMAIN.COM or as USER. In the latter case,
                        the user belongs to the server being tested.""")
    parser.add_argument('-t', '--token', help="auth token to be used for <MXID> for MatrixRTC testing")
    parser.add_argument('servername')
    args = parser.parse_args()
    if args.user and not args.user.startswith('@'):
        if ':' not in args.user:
            args.user = "@" + args.user + ":" + args.servername
        else:
            logging.error("Invalid local username '%s' given-", args.user)
            sys.exit(0)
    return args

def main():
    logging.basicConfig(datefmt="", format="{message}",
                        style="{",
                        level=logging.DEBUG)
    args = handle_cmd_opts()
    if args.quiet:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    tms = MatrixServer(args.servername, args)
    tms.test()

if __name__ == "__main__":
    main()
