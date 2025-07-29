# MCP Server Google News

A Model Context Protocol (MCP) server for fetching Google News articles with configurable language and region settings.

## Available Tools

### google_news_search

Search for news articles using a query.

Parameters:

- `query` (string, required): Search query
- `limit` (int, optional): Number of articles to fetch (default: 10)
- `hl` (string, optional): Language code (default: "ja")
- `gl` (string, optional): Geographic location code (optional)

### google_news_topics

Get news articles by topic.

Parameters:

- `topic_id` (string, optional): Topic ID (default: TOP)
- `limit` (int, optional): Number of articles to fetch (default: 10)
- `hl` (string, optional): Language code (default: "ja")
- `gl` (string, optional): Geographic location code (optional)

Available Topics:

- `TOP`: トップニュース (default)
- `NATION`: 国内
- `WORLD`: 国際
- `BUSINESS`: ビジネス
- `TECHNOLOGY`: テクノロジー
- `ENTERTAINMENT`: エンタメ
- `SPORTS`: スポーツ
- `SCIENCE`: 科学
- `HEALTH`: 健康

## Language and Region Codes

### Common Language Codes (hl parameter)

- `ja`: Japanese (default)
- `en`: English
- `zh-CN`: Chinese
- `fr`: French
- `de`: German
- `es`: Spanish
- `ko`: Korean

### Common Region Codes (gl parameter)

- `JP`: Japan
- `US`: United States
- `GB`: United Kingdom
- `CN`: China
- `FR`: France
- `DE`: Germany
- `KR`: South Korea

## Installation

### Using `uv` (Recommended)

No special installation is required when using `uv`. You can run `mcp-server-google-news` directly using `uvx`.

### Using PIP

Alternatively, you can install `mcp-server-google-news` using pip:

```sh
pip install mcp-server-google-news
```

After installation, you can run the script as follows:

```sh
mcp-server-google-news
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
{
  "mcpServers": {
    "google-news": {
      "command": "uvx",
      "args": ["mcp-server-google-news"]
    }
  }
}
```

</details>

### Configure for VS Code

For quick installation, use one of the one-click install buttons below...

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=google-news&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22google-news%22%5D%7D)

### Command Line Options

You can specify the following options when running the server:

- `--sse`: Enable Server-Sent Events transport (on/off)
- `--host`: Server bind address (default: localhost)
- `--port`: Server port number (default: 8000)
- `--log-level`: Logging verbosity (debug, info, warning, error)

## License

MIT
