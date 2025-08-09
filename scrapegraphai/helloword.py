from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

graph_config = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 1,
        "format": "json",  # Ollama needs the format to be specified explicitly
        "model_tokens": 2000,  # depending on the model set context length
        "base_url": "http://localhost:11434",
        # set ollama URL of the local host (YOU CAN CHANGE IT, if you have a different endpoint
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        "base_url": "http://localhost:11434",  # set ollama URL
    }
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

smart_scraper_graph = SmartScraperGraph(
    prompt="Gets the content of all the subpages of the current page.",
    # also accepts a string with the already downloaded HTML code
    source="https://www.wenxue88.com/zhishenshinei/index.html",
    config=graph_config
)

if __name__ == '__main__':
    result = smart_scraper_graph.run()
    print(result)

# {'Title': '置身事内', 'Sub-title': '兰小欢, 兰小欢', 'Chapters': [{'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0100.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0101.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0102.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0103.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0104.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0105.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0200.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0201.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0202.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0203.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0204.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0205.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0300.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0301.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0302.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0303.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0304.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0305.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0400.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0401.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0402.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0403.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0404.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0405.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0500.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0501.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0502.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0503.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0504.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0505.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0600.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0601.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0602.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0603.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0604.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0605.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0700.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0701.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0702.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0703.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0704.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0705.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0800.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0801.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0802.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0803.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0804.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0805.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0900.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0901.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0902.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0903.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0904.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn0905.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1000.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1001.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1002.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1003.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1004.html', 'ChapterNumber': 'NA'}, {'URL': 'https://www.wenxue88.com/zhishenshinei/zssn1005.html', 'ChapterNumber': 'NA'}], 'tags': ['novel', 'chinese literature', 'jin yong']}
