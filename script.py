token_v2 = "your_token_id"
page_url = "notion_url"
root_dir = "root_dir"
from notion.client import NotionClient
from md2notion.upload import upload
from notion.block import PageBlock
import io
from pathlib import Path
import glob
from tqdm import tqdm

client = NotionClient(token_v2=token_v2)
page = client.get_block(notion_url)

for fname in tqdm(glob.glob("{root_dir}/**/*.md", recursive=True)):
    with open(fname, "r", encoding="utf-8") as mdFile:

        md_txt = mdFile.read().split("\n")
        page_title = md_txt[0].replace("#", "").strip()
        md_txt = "\n".join(md_txt[1:-1])

        mdFile = io.StringIO(md_txt)
        mdFile.__dict__["name"] = fname #Set this so we can resolve images later
        newPage = page.children.add_new(PageBlock, title=page_title)

        def convertImagePath(imagePath, mdFilePath):
            decodedImagePath = urllib.parse.unquote(imagePath)
            ret = Path(mdFilePath).parent / Path(decodedImagePath)
            return ret
        upload(mdFile, newPage, imagePathFunc=convertImagePath)
