<div align="center">
<a href="https://yuanqi.tencent.com/" target="_blank" rel="noopener">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://open-agents-web-cdn-prd.hunyuan.tencent.com/public/bf6b0f00a2e660e0e35d.png" />
    <img alt="Framelink" src="https://open-agents-web-cdn-prd.hunyuan.tencent.com/public/bf6b0f00a2e660e0e35d.png" />
  </picture>
</a>

  <h1>元器插件 MCP 服务器</h1>
  <h3>为您的元器插件提供 mcp 访问能力。<br/>一次性在任何智能体框架中集成。</h3>
  <a href="https://github.com/GLips/Figma-Context-MCP/blob/main/LICENSE">
    <img alt="MIT 许可证" src="https://img.shields.io/github/license/GLips/Figma-Context-MCP" />
  </a>
</div>
<br/>
<p align="center">
  <a href="https://yuanqi.tencent.com/">元器</a>官方插件上下文协议(MCP)服务器，支持与强大的元器智能体交互。允许MCP客户端如<a href="https://www.anthropic.com/claude">Claude Desktop</a>、<a href="https://www.cursor.so">Cursor</a>、<a href="https://codeium.com/windsurf">Windsurf</a>、<a href="https://github.com/openai/openai-agents-python">OpenAI Agents</a>等进行集成。
</p>

## 快速开始使用 MCP 客户端

1. 从[元器智能体平台](https://yuanqi.tencent.com/)获取你需要插件的 API 密钥。
2. 安装`uv`（Python包管理器），使用`curl -LsSf https://astral.sh/uv/install.sh | sh`安装或查看`uv` [仓库](https://github.com/astral-sh/uv)获取其他安装方法。
3. **重要提示: 每个元器插件的ID和密钥都不相同**，两者需要匹配，否则会有 `token验证失败` 的错误

### Claude Desktop

前往`Claude > Settings > Developer > Edit Config > claude_desktop_config.json`包含以下内容：

```
{
  "mcpServers": {
    "YuanQiAgent": {
      "command": "uvx",
      "args": [
        "hunyuan-search"
      ],
      "env": {
        "API_KEY": "填写你调用的元器插件Token"
      }
    }
  }
}
```

⚠️ 注意：API_KEY需要与插件匹配。如果出现“token验证失败”错误，请检查您的API_KEY和插件。
如果你使用Windows，你需要在Claude Desktop中启用"开发者模式"才能使用MCP服务器。点击左上角汉堡菜单中的"Help"，然后选择"Enable Developer Mode"。

### Cursor

前往`Cursor -> Preferences -> Cursor Settings -> MCP -> Add new global MCP Server`添加上述配置。


## Transport

我们仅支持 stdio 传输方式
