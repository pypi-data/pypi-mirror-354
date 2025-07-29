import os

import click
import httpx
from mcp.server import FastMCP

mcp = FastMCP('vision-stat')
base_url = 'https://ls.e20.com.cn'
headers = {'Authorization': 'Bearer {}'.format(os.getenv('AUTH_TOKEN')), 'clientChannel': 'WEB'}


@mcp.tool()
def get_event_statistic():
    """获取按年统计的报警总数"""
    url = f'{base_url}/api/videoStat/alarmTypeYear'
    return httpx.get(url, headers=headers, timeout=10).json()


@mcp.tool()
def get_top10_machines():
    """获取报警数量最高的一体机/设备"""
    url = f'{base_url}/api/videoStat/machine/alarmTop10'
    return httpx.get(url, headers=headers, timeout=10).json()


@mcp.tool()
def get_industry_statistic():
    """获取一体机/设备在不同行业的应用数量统计"""
    url = f'{base_url}/api/videoStat/machine/industryStat'
    return httpx.get(url, headers=headers, timeout=10).json()


@mcp.tool()
def get_manufacturer_statistic():
    """获取一体机/设备的制造商数量统计"""
    url = f'{base_url}/api/videoStat/machine/manufacturerStat'
    return httpx.get(url, headers=headers, timeout=10).json()


@mcp.tool()
def get_province_statistic():
    """获取一体机/设备的省份应用数量统计"""
    url = f'{base_url}/api/videoStat/machine/provinceStat'
    return httpx.get(url, headers=headers, timeout=10).json()


@mcp.tool()
def get_region_statistic():
    """获取一体机/设备的区域应用数量统计"""
    url = f'{base_url}/api/videoStat/machine/regionStat'
    return httpx.get(url, headers=headers, timeout=10).json()


@click.command()
@click.option('-p', '--port', default=8000, help='Port to listen on for SSE')
@click.option(
    '-t',
    '--transport',
    type=click.Choice(['stdio', 'sse', 'streamable_http', 'mcp']),
    default='stdio',
    help='Transport type',
)
def main(port: int, transport: str) -> int:
    if transport == "streamable_http":
        mcp.run(transport="streamable-http")
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
    return 0
