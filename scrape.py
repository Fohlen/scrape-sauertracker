import os
from multiprocessing import Pool
import requests
import tqdm


def download_url(url):
    # assumes that the last segment after the / represents the file name
    # if url is abc/xyz/file.txt, the file name will be file.txt
    file_name_start_pos = url.rfind("/") + 1
    file_name = f"{url[file_name_start_pos:]}.json"

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        with open(file_name, "wt") as f:
            f.write(r.text)


def get_latest_game_id() -> int:
    r = requests.get("https://sauertracker.net/api/games/find")
    return r.json()["results"][0]["id"]


def get_latest_local_game_id() -> int:
    files = os.listdir()
    files = [f for f in files if f.endswith(".json")]
    game_ids = [f[-5] for f in files]
    return sorted(game_ids)[0] if len(game_ids) else 0


def scrape_sauertracker():
    latest_id = get_latest_game_id()
    latest_local_id = get_latest_local_game_id()
    diff = latest_id - latest_local_id
    files_to_download = [f"https://sauertracker.net/api/game/{id}" for id in range(latest_local_id, diff)]
    print(f"Obtaining {diff} games from SauerTracker")
    pool = Pool(processes=8)
    for _ in tqdm.tqdm(pool.imap_unordered(download_url, files_to_download), total=len(files_to_download)):
        pass


if __name__ == "__main__":
    print("Scraping the tracker")
    scrape_sauertracker()
