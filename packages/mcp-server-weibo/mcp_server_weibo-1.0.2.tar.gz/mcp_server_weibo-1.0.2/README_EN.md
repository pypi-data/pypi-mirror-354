# Weibo MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server for fetching Weibo user information, posts, and search functionality. This server helps retrieve detailed user information, posts, and perform user searches on Weibo.

<a href="https://glama.ai/mcp/servers/@qinyuanpei/mcp-server-weibo">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@qinyuanpei/mcp-server-weibo/badge" alt="Weibo Server MCP server" />
</a>

[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/qinyuanpei-mcp-server-weibo-badge.png)](https://mseep.ai/app/qinyuanpei-mcp-server-weibo)

## Installation

From source code:

```json
{
  "mcpServers": {
    "weibo": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/qinyuanpei/mcp-server-weibo.git",
        "mcp-server-weibo"
      ]
    }
  }
}
```
From package manager:

```json
{
  "mcpServers": {
    "weibo": {
      "command": "uvx",
      "args": ["mcp-server-weibo"],
    }
  }
}
```
From Docker:
```bash
docker build -t mcp-server-weibo .
docker run -d --name mcp-server-weibo -p 4200:4200 mcp-server-weibo
```
Reference config:
```json
{
  "mcpServers": {
    "weibo": {
      "url": "http://localhost:4200/mcp",
    }
  }
}
```

## Components

### Tools

#### search_users(keyword, limit)
Description: Search for Weibo users

Example return value:

  ```json
  [
    {
      "id": 1749127163,
      "screen_name": "Lei Jun",
      "profile_image_url": "https://tvax1.sinaimg.cn/crop.0.0.1080.1080.180/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg?KID=imgbed,tva&Expires=1749109677&ssig=QzOuVFBlRp",
      "profile_url": "https://m.weibo.cn/u/1749127163?",
      "description": "Chairman of Xiaomi, Chairman of Kingsoft. Angel investor as a hobby.",
      "follow_count": 1562,
      "followers_count": "26.71M",
      "avatar_hd": "https://wx1.sinaimg.cn/orj480/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg",
      "verified": true,
      "verified_reason": "Founder, Chairman and CEO of Xiaomi; Chairman of Kingsoft; Angel investor.",
      "gender": "m"
    }
  ]
  ```

#### get_profile(uid)
Description: Get detailed user information

Example return value:

  ```json
  {
    "id": 1749127163,
    "screen_name": "Lei Jun",
    "profile_image_url": "https://tvax1.sinaimg.cn/crop.0.0.1080.1080.180/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg?KID=imgbed,tva&Expires=1749109733&ssig=5OrMoqbwcY",
    "profile_url": "https://m.weibo.cn/u/1749127163?",
    "description": "Chairman of Xiaomi, Chairman of Kingsoft. Angel investor as a hobby.",
    "follow_count": 1562,
    "followers_count": "26.71M",
    "avatar_hd": "https://wx1.sinaimg.cn/orj480/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg",
    "verified": true,
    "verified_reason": "Founder, Chairman and CEO of Xiaomi; Chairman of Kingsoft; Angel investor.",
    "gender": "m"
  }
  ```

#### get_feeds(uid, limit)
Description: Get user posts

Example return value:

  ```json
  [
    {
      "id": 5167970394572058,
      "text": "This year marks the 15th anniversary of Xiaomi's founding.<br />Back in 2014, 11 years ago, we started our chip R&D journey.<br /><br />In September 2014, the Surge project was launched. In 2017, Xiaomi's first mobile phone chip 'Surge S1' was officially unveiled, targeting the mid-to-high-end market. Later, due to various reasons, we encountered setbacks and suspended the development of SoC large chips. But we still kept the spark of chip R&D alive and turned to the 'small chip' route. Later, Xiaomi Surge ...<a href=\"/status/5167970394572058\">Full text</a>",
      "source": "Xiaomi 15S Pro",
      "created_at": "Mon May 19 11:00:21 +0800 2025",
      "user": {
        "id": 1749127163,
        "screen_name": "Lei Jun",
        "profile_image_url": "https://tvax1.sinaimg.cn/crop.0.0.1080.1080.180/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg?KID=imgbed,tva&Expires=1749109794&ssig=29j5mGcswB",
        "profile_url": "https://m.weibo.cn/u/1749127163?",
        "description": "Chairman of Xiaomi, Chairman of Kingsoft. Angel investor as a hobby.",
        "follow_count": 1562,
        "followers_count": "26.71M",
        "avatar_hd": "https://wx1.sinaimg.cn/orj480/001Un9Srly8i1p6mooym8j60u00u10tu02.jpg",
        "verified": true,
        "verified_reason": "Founder, Chairman and CEO of Xiaomi; Chairman of Kingsoft; Angel investor.",
        "gender": "m"
      },
      "comments_count": 10183,
      "attitudes_count": 141025,
      "reposts_count": 5884,
      "raw_text": "",
      "region_name": "Posted in Beijing",
      "pics": [
        {
          "thumbnail": "https://wx2.sinaimg.cn/orj360/001Un9Srly1i1k4dr5djgj60u04gp7wh02.jpg",
          "large": "https://wx2.sinaimg.cn/large/001Un9Srly1i1k4dr5djgj60u04gp7wh02.jpg"
        }
      ],
      "videos": {}
    }
  ]
  ```

- #### get_hot_search(limit)
Description: Get Weibo hot search

Example return value:

  ```json
  [
    {
      "id": 0,
      "trending": 0,
      "description": "Explore Chinese civilization with the General Secretary",
      "url": "https://m.weibo.cn/search?containerid=100103type%3D1%26t%3D10%26q%3D%23%E8%B7%9F%E7%9D%80%E6%80%BB%E4%B9%A6%E8%AE%B0%E6%8E%A2%E5%AF%BB%E4%B8%AD%E5%8D%8E%E6%96%87%E6%98%8E%23&stream_entry_id=51&isnewpage=1&extparam=seat%3D1%26stream_entry_id%3D51%26c_type%3D51%26filter_type%3Drealtimehot%26pos%3D0%26cate%3D10103%26dgr%3D0%26q%3D%2523%25E8%25B7%259F%25E7%259D%2580%25E6%2580%25BB%25E4%25B9%25A6%25E8%25AE%25B0%25E6%258E%25A2%25E5%25AF%25BB%25E4%25B8%25AD%25E5%258D%258E%25E6%2596%2587%25E6%2598%258E%2523%26display_time%3D1749098276%26pre_seqid%3D17490982767230055147"
    },
    {
      "id": 3,
      "trending": 591855,
      "description": "It is recommended to stay away from romantic-style friendships",
      "url": "https://m.weibo.cn/search?containerid=100103type%3D1%26t%3D10%26q%3D%E5%BB%BA%E8%AE%AE%E5%A4%A7%E5%AE%B6%E8%A6%81%E8%BF%9C%E7%A6%BB%E6%81%8B%E7%88%B1%E5%BC%8F%E5%8F%8B%E6%83%85&stream_entry_id=31&isnewpage=1&extparam=seat%3D1%26dgr%3D0%26c_type%3D31%26cate%3D5001%26realpos%3D12%26stream_entry_id%3D31%26lcate%3D5001%26q%3D%25E5%25BB%25BA%25E8%25AE%25AE%25E5%25A4%25A7%25E5%25AE%25B6%25E8%25A6%2581%25E8%25BF%259C%25E7%25A6%25BB%25E6%2581%258B%25E7%2588%25B1%25E5%25BC%258F%25E5%258F%258B%25E6%2583%2585%26pos%3D11%26band_rank%3D12%26flag%3D1%26filter_type%3Drealtimehot%26display_time%3D1749098276%26pre_seqid%3D17490982767230055147"
    }
  ]
  ```

#### search_content(keyword, limit, page)
Description: Search Weibo posts

Example return value:

  ```json
  [
    {
      "id": 5174033353539603,
      "text": "<a  href=\"https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%9C%B0%E9%9C%87%E9%A2%84%E8%AD%A6%23&isnewpage=1\" data-hide=\"\"><span class=\"surl-text\">#EarthquakeWarning#</span></a> According to the China Earthquake Early Warning Network, at 04:31, an earthquake of about magnitude 4.7 occurred near Heqing, Dali, Yunnan (E100.1, N26.3). The warning network issued an early warning to Kunming 73 seconds before the seismic waves arrived, with an estimated intensity of 0.7. You can download the ICL 'Earthquake Warning' APP to receive warnings and get more services. Domestic mobile phones can also enable the built-in earthquake warning function in the operating system.",
      "source": "Earthquake Warning",
      "created_at": "Thu Jun 05 04:32:22 +0800 2025",
      "user": {
        "id": 2867810960,
        "screen_name": "Chengdu High-tech Disaster Mitigation Institute",
        "profile_image_url": "https://tvax3.sinaimg.cn/crop.0.0.996.996.180/aaef5290ly8gdig1jpisaj20ro0romxi.jpg?KID=imgbed,tva&Expires=1749110036&ssig=JEEuM0wUxA",
        "profile_url": "https://m.weibo.cn/u/2867810960?",
        "description": "Founded after the Wenchuan earthquake, focusing on disaster warning technology R&D, achievement transformation and application.",
        "follow_count": 307,
        "followers_count": "345K",
        "avatar_hd": "https://wx3.sinaimg.cn/orj480/aaef5290ly8gdig1jpisaj20ro0romxi.jpg",
        "verified": true,
        "verified_reason": "Chengdu High-tech Disaster Mitigation Institute",
        "gender": "m"
      },
      "comments_count": 33,
      "attitudes_count": 53,
      "reposts_count": 1,
      "raw_text": "",
      "region_name": "Beijing",
      "pics": [],
      "videos": {}
    }
  ]
  ```

### Resources   

None

### Prompts

None

## Requirements

- Python >= 3.10
- httpx >= 0.24.0

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Disclaimer

For more information, see the Chinese README (`README.md`).

This project is not affiliated with Weibo and is intended for learning and research purposes only.