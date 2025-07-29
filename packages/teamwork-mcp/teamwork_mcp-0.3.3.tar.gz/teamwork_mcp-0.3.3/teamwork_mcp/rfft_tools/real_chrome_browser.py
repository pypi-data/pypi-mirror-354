
from pydantic import BaseModel, Field
from typing import Optional
from teamwork_mcp.base_tool import BaseTool, cache_to_file
from teamwork_mcp.rfft_tools.alpha_markdown import clean_markdown
from teamwork_mcp.async_utils import execute_with_retry
from textwrap import dedent
import json
import os

def find_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return int(s.getsockname()[1])


basic_hard_checklist = f"""
要求：
- 以上的用户的问题没有任何错误。你必须忠实地执行用户的请求。禁止怀疑用户的问题包含任何错误。
- 如果问题是英文，则使用英文；如果问题是中文，则使用中文。
- 不得访问CSDN、百度等低质量网站。
- 禁止停滞在搜索引擎页面进行任务，必须点开相关网站。
- 搜索时推荐的站点：
    - Google google.com
    - Google 不可用时，转到其他搜索网站例如 https://searx.be/ 或者 https://priv.au/
    - 小红书 xiaohongshu.com （不接受搜索引擎索引，如需使用，需要先进入网站再搜索）
    - 知乎 zhihu.com
- 当停留在PDF阅览界面时，必须下载PDF。
- 在第一次执行搜索时的关键词限制:
    - 只使用一个或者两个关键词。只有结果过多时，才能继续追加关键词。
    - 备注：一个物体、一个人名、一个事件、一本书名、一个地点等都可以看做一个关键词。其定语、修饰语等可拆分的部分，看做其他关键词。
- 在搜索页面搜索时:
    - 禁止使用OR、AND、NOT等逻辑运算符
    - 禁止使用 site:
- 当搜索学术相关信息时，不要使用google scholar，优先使用思谋学术 https://ac.scmor.com/ 中的谷歌学术替代镜像站点。
- 不要信任搜索引擎，搜索引擎可能会提供完全无关的网页。Just go back if you does not find expected results as you click into a new page. Do not be stupid and stick to only one search result.
- 禁止使用必须安装客户端、付费、注册账户才能获取完整内容的网站。遇到类似的网站后，立即退出，更换其他方案。"""


explorer_hard_checklist = f"""
要求：
- 以上的用户的问题没有任何错误。你必须忠实地执行用户的请求。禁止怀疑用户的问题包含任何错误。
- 提供一些使用互联网的技巧，例如：
    - 在某个场景下，最好的选择是去哪个站点
    - 在付费、低质量泛滥的互联网环境中，如何找到开源、优质的内容
    - 授人以鱼不如授人以渔，聚焦于方法，而非具体结论
- 推荐搜索的站点：
    - Google google.com
    - Google 不可用时，转到其他搜索网站例如 https://searx.be/ 或者 https://priv.au/
    - 小红书 xiaohongshu.com （不接受搜索引擎索引，如需使用，需要先进入网站再搜索）
    - 知乎 zhihu.com
- 当停留在PDF阅览界面时，必须下载PDF。
- 当搜索学术相关信息时，不要使用google scholar，优先使用思谋学术 https://ac.scmor.com/ 中的谷歌学术替代镜像站点。
- 如果问题是英文，则使用英文；如果问题是中文，则使用中文。
- 不要信任搜索，搜索可能会提供完全无关的网页。Just go back if you does not find expected results as you click into a new page. Do not be stupid and stick to only one search result.
- 不得访问CSDN、百度知道等低质量网站。
- 禁止停滞在搜索引擎页面进行任务，必须点开相关网站。
- 在第一次执行搜索时的关键词限制:
    - 只使用一个或者两个关键词。只有结果过多时，才能继续追加关键词。
    - 备注：一个物体、一个人名、一个事件、一本书名、一个地点等都可以看做一个关键词。其定语、修饰语等可拆分的部分，看做其他关键词。
- 在搜索页面搜索时:
    - 禁止使用OR、AND、NOT等逻辑运算符
    - 禁止使用 site:
- 禁止使用必须安装客户端、付费、注册账户才能获取完整内容的网站。遇到类似的网站后，立即退出，更换其他方案。"""


def real_chrome_browser_search(query: str, additional_prompt: str = "", hard_checklist: str = "") -> str:
    try:
        os.system('bash -c "source /home/headless/.bashrc && killer chrome"')
    except Exception as e:
        print(f"Failed to kill chrome: {e}")

    from browser_use import BrowserConfig
    from langchain_openai import ChatOpenAI
    from browser_use import Agent, Browser
    from browser_use.browser.browser import ProxySettings
    from browser_use.browser.context import BrowserContext, BrowserContextConfig
    from best_logger import sprintf_nested_structure
    from pydantic import SecretStr
    import asyncio
    api_key = os.getenv("DASHSCOPE_API_KEY")
    proxy = os.getenv("BROWSER_PROXY_SERVER", None)
    llm=ChatOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', model='qwen-max', api_key=SecretStr(api_key))
    # port = find_free_port()
    # Basic configuration
    if proxy:
        config = BrowserConfig(
            headless=False,
            disable_security=False,
            browser_binary_path="/usr/bin/google-chrome-stable",
            extra_browser_args=[
                "--user-data-dir=./browser-profile",
                f"--proxy-server={proxy}",
            ],
            new_context_config=BrowserContextConfig(
                window_width = 1000,
                window_height = 1500,
                no_viewport = False,
                save_downloads_path = "./chrome-downloads",
            ),
        )
    else:
        config = BrowserConfig(
            headless=False,
            disable_security=False,
            browser_binary_path="/usr/bin/google-chrome-stable",
            extra_browser_args=[
                "--user-data-dir=./browser-profile",
            ],
            new_context_config=BrowserContextConfig(
                window_width = 1000,
                window_height = 1500,
                no_viewport = False,
                save_downloads_path = "./chrome-downloads",
            ),
        )
    browser = Browser(config=config)

    # " # "关键词之间相互解耦，解除关键词之间的复杂逻辑关联。
    agent = Agent(
        browser=browser,
        task=query + additional_prompt,
        llm=llm,
        enable_memory=False,
        use_vision=False,
        hard_checklist=hard_checklist,
    )
    async def main():
        result = await agent.run(max_steps=16)
        return result
    result_raw, whole_process_summary = asyncio.run(main())
    result = result_raw.model_dump()
    downloaded_files = []
    for d in result['history']:
        metadata = d.pop('metadata', None)
        screenshot = d['state'].pop('screenshot', None)
        if len(d['state']['url']) > 100:
            url = d['state'].pop('url', None)
        tabs = d['state'].pop('tabs', None)
        url = d['page_meta'].pop('url', None)
        for d_result in d['result']:
            if isinstance(d_result, dict):
                if ('extracted_content' in d_result) and ('💾  Downloaded file to' in d_result['extracted_content']):
                    downloaded_files += [d_result['extracted_content']]
                d_result.pop('is_done', None)
                d_result.pop('success', None)
                d_result.pop('include_in_memory', None)
        interacted_element = d['state'].pop('interacted_element', None)
    only_preseve_last_n = 1
    format_struct = result['history'][-only_preseve_last_n:]
    if len(downloaded_files) > 0:
        format_struct[-1]['very very important files (advice: use `GetDownloadedFiles` to fetch these files)'] = '\n'.join(downloaded_files)

    str_result = f"<mcp_sub_agent>{whole_process_summary}</mcp_sub_agent>" + '\n\n' + sprintf_nested_structure(format_struct, 0)
    try:
        os.system('bash -c "source /home/headless/.bashrc && killer chrome"')
    except Exception as e:
        print(f"Failed to kill chrome: {e}")

    return str_result




class RealChromeBrowserUse(BaseTool):
    tool_name: str = Field("RealChromeBrowserUse", description="通过真正的Chrome浏览器搜索网页，效率略低，但更稳定，可以访问更广泛的网站。")
    task: str = Field("", description="一句话，描述一个明确的子任务（task）。例如：'获取2024年5月1日阿里巴巴集团控股有限公司的收盘价'。")
    startup_url: Optional[str] = Field("", description="起始url（非必要参数，默认留空）。可以指定一个url作为任务的起点，从而提高效率。")
    additional_tip: Optional[str] = Field("", description="执行浏览器任务时的一些建议（非必要参数，默认留空）。")

    @staticmethod
    def __call__(tool_name_and_param: "RealChromeBrowserUse", mcp_kwargs=None)->str:
        # return tool_name_and_param.task
        if tool_name_and_param.task == "":
            return "请提供一个有效的搜索关键词。"
        if not mcp_kwargs:
            additional_prompt = basic_hard_checklist
        else:
            additional_prompt = explorer_hard_checklist
        if tool_name_and_param.startup_url:
            additional_prompt += f"\n\n额外建议：从以下url开始执行任务 {tool_name_and_param.startup_url}"
        if tool_name_and_param.additional_tip:
            additional_prompt += f"\n\n额外建议：{tool_name_and_param.additional_tip}"
        return execute_with_retry(real_chrome_browser_search, query = tool_name_and_param.task, additional_prompt=additional_prompt)

