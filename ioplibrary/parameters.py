COVERS_DIR = "covers"
UNAVAILABLE_COVER_URL = f"{COVERS_DIR}/unavailable.jpg"
EXCLUSION_SET = {"buy", "book", "amazon"}
SKIP_SET = {"download", "free"}

DDG_API_URL = "https://duckduckgo-image-search.p.rapidapi.com/search/image"
DDG_API_HEADERS = {
    "content-type": "application/octet-stream",
    "X-RapidAPI-Key": "8a98f92c5dmshb5a0997c0356c99p1b84f1jsn97ea86a64ca6",
    "X-RapidAPI-Host": "duckduckgo-image-search.p.rapidapi.com",
}
