import json
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element

from requests import Session

from .constants import (
    ENCLOSURE_URL,
    INCLUDE_PODCAST_IDS,
    OVERCAST_ID,
    SMART,
    SORTING,
    TITLE,
    USER_REC_DATE,
)
from .exceptions import (
    AuthFailedError,
    OpmlFetchError,
    WrongPasswordError,
)
from .utils import _parse_date_or_none


def auth_and_save_cookies(email: str, password: str, auth_json: str) -> None:
    """Authenticate to Overcast and save cookies to a JSON file."""
    session = Session()
    response = session.post(
        "https://overcast.fm/login?then=account",
        data={"email": email, "password": password},
        allow_redirects=False,
    )

    if "Incorrect password" in response.text:
        raise WrongPasswordError
    cookies = session.cookies.get_dict()
    if "o" not in cookies:
        raise AuthFailedError

    print("Authenticated successfully. Saving session.")
    auth_json_path = Path(auth_json)
    if auth_json_path.exists():
        auth_data = json.loads(auth_json_path.read_text())
    else:
        auth_data = {}
    auth_data["overcast"] = cookies
    auth_json_path.write_text(json.dumps(auth_data, indent=4) + "\n")


def _session_from_json(auth_json_path: str) -> Session:
    with Path(auth_json_path).open() as f:
        cookies = json.load(f)["overcast"]
        session = Session()
        session.cookies.update(cookies)
        return session


def _session_from_cookie(cookie: str) -> Session:
    session = Session()
    session.cookies.update({"o": cookie, "qr": "-"})
    return session


def fetch_opml(session: Session, archive_dir: Path | None) -> str:
    """Fetch OPML from Overcast and optionally save OPML to an archive directory."""
    response = session.get(
        "https://overcast.fm/account/export_opml/extended",
        timeout=None,
    )
    if not response.ok:
        raise OpmlFetchError(dict(response.headers))
    response_text = response.text
    if archive_dir:
        archive_dir.mkdir(parents=True, exist_ok=True)
        now = int(datetime.now(tz=UTC).timestamp())
        archive_dir.joinpath(f"overcast-{now}.opml").write_text(response_text)
    return response_text


def _iso_date_or_none(dictionary: dict, key: str) -> str | None:
    if key in dictionary:
        return _parse_date_or_none(dictionary[key])
    return None


def extract_playlists_from_opml(root: Element) -> Iterable[dict]:
    for playlist in root.findall(
        "./body/outline[@text='playlists']/outline[@type='podcast-playlist']",
    ):
        if INCLUDE_PODCAST_IDS in playlist.attrib:
            yield {
                TITLE: playlist.attrib[TITLE],
                SMART: int(playlist.attrib[SMART]),
                SORTING: playlist.attrib[SORTING],
                INCLUDE_PODCAST_IDS: f"[{playlist.attrib[INCLUDE_PODCAST_IDS]}]",
            }


def extract_feed_and_episodes_from_opml(
    root: Element,
) -> Iterable[tuple[dict, list[dict]]]:
    for feed in root.findall("./body/outline[@text='feeds']/outline[@type='rss']"):
        episodes = []
        feed_attrs: dict[str, Any] = feed.attrib.copy()
        feed_attrs[OVERCAST_ID] = int(feed_attrs[OVERCAST_ID])
        feed_attrs["subscribed"] = feed_attrs.get("subscribed", False) == "1"
        feed_attrs["notifications"] = feed_attrs.get("notifications", False) == "1"
        feed_attrs["overcastAddedDate"] = _iso_date_or_none(
            feed_attrs,
            "overcastAddedDate",
        )
        del feed_attrs["type"]
        del feed_attrs["text"]

        for episode_xml in feed.findall("./outline[@type='podcast-episode']"):
            ep_attrs: dict[str, Any] = episode_xml.attrib.copy()
            ep_attrs[OVERCAST_ID] = int(ep_attrs[OVERCAST_ID])
            ep_attrs[ENCLOSURE_URL] = ep_attrs[ENCLOSURE_URL].split("?")[0]

            ep_attrs["feedId"] = feed_attrs["overcastId"]
            ep_attrs["played"] = ep_attrs.get("played", False) == "1"
            ep_attrs["userDeleted"] = ep_attrs.get("userDeleted", False) == "1"
            ep_attrs["progress"] = (
                None
                if (progress := ep_attrs.get("progress")) is None
                else int(progress)
            )
            ep_attrs["userUpdatedDate"] = _iso_date_or_none(ep_attrs, "userUpdatedDate")
            ep_attrs[USER_REC_DATE] = _iso_date_or_none(
                ep_attrs,
                USER_REC_DATE,
            )
            ep_attrs["pubDate"] = _iso_date_or_none(ep_attrs, "pubDate")
            del ep_attrs["type"]

            episodes.append(ep_attrs)

        yield feed_attrs, episodes
