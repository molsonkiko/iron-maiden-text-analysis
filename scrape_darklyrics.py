import re
import requests
from bs4 import BeautifulSoup as bs


def get_album_soups(artist):
    '''Assuming that the artist is on darklyrics (probably true for most heavy
metal bands), scrapes each webpage for an album associated with that artist.
Returns a dict mapping album titles to BeautifulSoup objects containing the
HTML for that album's webpage.
    '''
    artist = ''.join(artist.lower().split())
    first_letter = artist[0]
    baseurl = f"http://www.darklyrics.com/{first_letter}/{artist}.html"
    resp = requests.get(baseurl)
    resp.raise_for_status()
    soup = bs(resp.text, 'html.parser')
    song_link_selector = 'div.album a'
    song_links = soup.select(song_link_selector)
    album_soups = {}
    for link in song_links:
        album = link.get_attribute_list('href')[0].split('/')[-1]
        album = re.sub('\.html#\d+', '', album)
        if album not in album_soups:
            alblink = f'http://www.darklyrics.com/lyrics/{artist}/{album}.html#1'
            albsoup = bs(requests.get(alblink).text, 'html.parser')
            album_soups[album] = albsoup
            
    return album_soups
    

def get_song_data(album_soups):
    '''Get a list of dicts with the album name, the year (int), the number in 
    the album (int), the song title, 
    and the lyrics (if any) for each song in every album found'''
    songdata = []
    songs_seen = set()
    for albsoup in album_soups.values():
        title = None
        this_song = {}
        lyrics = None
        title_year = albsoup.select_one('h2').text
        # print(title_year)
        # e.g., "Iron Maiden" (1980)
        album_title, year = re.findall('\"(.+)\".+\((\d+)\)', title_year)[0]
        year = int(year)
        song_num = None
        song = None
        all_lyrics = albsoup.select_one('div.lyrics')
        for child in all_lyrics.children:
            if child.name == 'h3':
                # song title heading
                if song:
                    songdata.append(song)
                title = re.sub('^\d+\.', '', child.text).strip()
                song_num = int(re.findall('^\d+',  child.text)[0])
                stripped_title = re.sub('\(.+\)', '', title).strip()
                # gets rid of things like "Public Enema Number One (Live)"
                # by converting them to the base song ("Public Enema Number One")
                if stripped_title in songs_seen:
                    song = None
                else:
                    songs_seen.add(title)
                    song = {
                        'album': album_title,
                        'year': year,
                        'num': song_num,
                        'title': title,
                        'lyrics': '',
                    }
                continue
            if not song:
                continue
            if title and not hasattr(child, 'text'):
                # if it had text, that would mean that it was an HTML element
                # nested inside div.lyrics (e.g., an album title, the "thanks"
                # section where the contributer thanks people who helped).
                # All the lyrics are on the same level - they're direct
                # children of div.lyrics.
                text = child.strip()
                if text:
                    song['lyrics'] += text + '\\n'
        if song:
            songdata.append(song)
            
    return songdata
    

def store_songs_tsv(songdata, fname):
    '''Writes the return value of get_song_data to a tab-separated variables (TSV) file with five columns: 
    album title, album year, song number in album, song title,
    and song lyrics. All newlines in the song lyrics are replaced with '\\n'.
    '''
    with open(fname, 'w', encoding='utf-8') as f:
        f.write('\t'.join(songdata[0].keys()) + '\n')
        for song in songdata:
            f.write('\t'.join(str(x) for x in song.values()) + '\n')
            

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('artist', help='The name of the artist with lyrics to be scraped')
    parser.add_argument('fname', nargs='?', help='Name of file to write TSV file to. If not supplied, dump the output to stdout as JSON string.')
    args = parser.parse_args()
    soups = get_album_soups(args.artist)
    songdata = get_song_data(soups)
    if args.fname:
        store_songs_tsv(songdata, args.fname)
    else:
        import json
        print(json.dumps(songdata))