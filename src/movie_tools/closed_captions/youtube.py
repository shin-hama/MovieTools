# -*- coding: utf-8 -*-

# Sample Python code for youtube.captions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from dataclasses import dataclass, asdict
import io
import os
import pickle

from dacite import from_dict
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = "client_secrets.json"


@dataclass
class CaptionSnippet:
    videoId: str
    lastUpdated: str
    trackKind: str
    language: str
    name: str
    audioTrackType: str
    isCC: bool
    isLarge: bool
    isEasyReader: bool
    isDraft: bool
    isAutoSynced: bool
    status: str


@dataclass
class UploadCaptionSnippet:
    videoId: str
    language: str
    name: str
    isDraft: bool = False


@dataclass
class Caption:
    kind: str
    etag: str
    id: str
    snippet: CaptionSnippet


@dataclass
class CaptionResponse:
    kind: str
    etag: str
    items: list[Caption]


class YouTubeClient:
    def __init__(self):
        # Get credentials and create an API client
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    def get_captions(self):
        request = self.youtube.captions().list(part="id,snippet", videoId="iSQCc_1CiyE")
        response = request.execute()

        res = from_dict(CaptionResponse, response)
        return res

    def get_caption(self, id: str) -> bytes:
        request = self.youtube.captions().download(id=id)
        fh = io.BytesIO()

        download = MediaIoBaseDownload(fh, request)
        complete = False
        while not complete:
            status, complete = download.next_chunk()
        return fh.getvalue()

    def upload_caption(self, caption: bytes, snippet: UploadCaptionSnippet):
        request = self.youtube.captions().insert(
            part="snippet",
            body={"snippet": asdict(snippet)},
            media_body=MediaInMemoryUpload(caption),
        )
        response = request.execute()

        print(response)
        return response

    def delete_caption(self, id: str):
        request = self.youtube.captions().delete(id=id)
        request.execute()


if __name__ == "__main__":
    client = YouTubeClient()
    video_id = "iSQCc_1CiyE"
    # captions = client.get_captions()
    # print(captions)
    data = client.get_caption("MRglHYjRG6_L71lEOICdvvyhJRApqRxZ")
    snippet = UploadCaptionSnippet(language="fr", name="France", videoId=video_id)
    client.upload_caption(data, snippet)
