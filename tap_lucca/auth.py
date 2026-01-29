import requests
from singer_sdk.authenticators import OAuthAuthenticator

class LuccaAuthenticator(OAuthAuthenticator):


    @property
    def oauth_request_body(self) -> dict:
        return f"client_id={self.client_id}&client_secret={self.client_secret}&scope={self.oauth_scopes}&grant_type=client_credentials"





