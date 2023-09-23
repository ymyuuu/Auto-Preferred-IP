# Preferred-IP 自动更新DNS解析

Preferred-IP 是一个用于自动更新DNS解析记录的工具，旨在帮助您始终使用最佳的IP地址来提高您的域名性能和可用性。这个工具可以特别对需要快速响应变化的网站和应用程序非常有用，因为它确保了您的域名将始终指向性能最佳的服务器IP地址。

<img width="1427" alt="image" src="https://github.com/ymyuuu/Preferred-IP/assets/135582157/fc8b8303-03ae-479a-9a39-bb5578058b38">



## 为什么需要 Preferred-IP？

### 1. 提高网站性能

使用最佳的IP地址可以加速网站加载速度，提高用户体验。Preferred-IP 可以自动监测并更新IP地址，确保您的网站始终在性能最佳的服务器上运行。

### 2. 提高可用性

如果您的服务器出现故障或不可用，Preferred-IP 可以自动将流量路由到备用IP地址，从而提高了可用性和冗余性。

### 3. 自动化DNS管理

Preferred-IP 自动更新DNS解析记录，无需手动干预。这意味着您不必担心手动修改DNS设置，特别是在服务器IP地址发生变化时。

### 4. 多地区性能优化

Preferred-IP 允许您根据不同地区和运营商选择最佳的IP地址，以确保在全球范围内提供高性能的服务。

## 如何使用 Preferred-IP？

要使用 Preferred-IP 自动更新DNS解析工具，只需按照以下步骤进行简单的配置：

### 1. Fork 本仓库

首先，在GitHub上复制这个仓库到您自己的GitHub账户下，这将创建一个您自己的仓库的副本。

### 2. 配置环境变量

环境变量是用来存储敏感信息和配置选项的。在您的 GitHub 仓库中，按照以下步骤设置这些环境变量：

#### a. 打开仓库设置

在您的 GitHub 仓库页面上，点击页面上方的 "Settings" 选项卡。

#### b. 进入 "Secrets" 部分

在 "Settings" 选项卡下，选择左侧的 "Secrets" 选项，然后点击 "New repository secret" 按钮。

#### c. 添加 `DOMAINS` 环境变量

首先，添加一个名为 `DOMAINS` 的环境变量，用于指定您要更新的域名和子域名信息。请按照以下格式输入域名和子域名的信息：

```json
{
  "example.com": {
    "www": ["CM", "CU"],
    "blog": ["CT"]
  }
}
```

这个示例中，`example.com` 是主域名，`www` 和 `blog` 是子域名，而 `CM`、`CU` 和 `CT` 是DNS解析的线路。您可以根据自己的需求进行配置。

#### d. 添加 `SECRETID` 和 `SECRETKEY` 环境变量

接下来，添加两个环境变量，分别为 `SECRETID` 和 `SECRETKEY`。这些变量用于存储您的腾讯云API密钥，以便 Preferred-IP 工具能够访问并修改DNS记录。

#### e. 添加 `DOMAINSV6` 环境变量（可选）

如果您需要更新IPv6记录，可以添加一个名为 `DOMAINSV6` 的环境变量，并以与 `DOMAINS` 相同的格式提供IPv6域名和子域名信息。

#### f. 保存环境变量

确保您的环境变量设置正确，然后点击 "Add secret" 按钮以保存它们。

### 3. 修改定时任务（可选）

默认情况下，GitHub Actions会按照您的配置每10分钟运行一次脚本。如果您希望更改此频率，请编辑workflow文件中的 `schedule` 部分。

### 4. 启动GitHub Actions

一旦您完成了上述配置，GitHub Actions将会自动开始工作。脚本会定期检查最新的优选IP，并更新DNS解析记录。

这样，您就可以详细配置 Preferred-IP 工具并设置必要的环境变量，以便自动更新DNS解析记录。希望这些说明有助于您更好地使用这个工具。如果您需要进一步的帮助或有任何问题，请随时提问或查看项目的文档。

## 配置TTL 和其他参数

在 Preferred-IP 工具中，您可以配置TTL以及其他相关参数，以满足您的需求。这些参数通常在脚本中进行配置，您可以在 YAML 文件中找到它们。以下是如何配置它们的步骤：

#### 1. 打开脚本

在您的 GitHub 仓库中，找到包含 Preferred-IP 脚本的文件（通常是 `Preferred-IP.py`），然后打开它以编辑。

#### 2. 找到配置参数

在脚本的开头部分，通常会有一个包含配置参数的部分。这些参数是以字典（例如 `CONFIG`）的形式定义的。

#### 3. 配置TTL

在配置参数中，找到名为 `TTL` 的参数，通常它是一个整数，表示DNS记录的TTL值。您可以根据需要修改此值，以更改DNS记录的TTL。例如：

```python
TTL = 600  # 将TTL设置为600秒（10分钟）
```

#### 4. 配置其他参数

在配置参数中，还可以找到其他与DNS解析和优选IP相关的参数。例如，您可以配置以下参数：

- `RECORD_TYPE`：DNS记录的类型，通常是 "A"

 或 "AAAA"（IPv4或IPv6）。这个参数通常由脚本的命令行参数指定。

- `AFFECT_NUM`：影响的DNS记录数量，根据您的需求设置。

#### 5. 保存脚本

完成配置后，请保存脚本文件。

### 配置TTL的最佳实践

在配置TTL时，通常需要考虑一些最佳实践：

- TTL 时间应该根据您的需求和实际情况进行调整。较短的TTL（例如几分钟）可以帮助您更快地更新DNS记录，但可能会增加DNS服务器的负载。较长的TTL（例如一天或更长）可以减轻DNS服务器的负载，但更新DNS记录的响应速度可能较慢。

- 考虑您的网站流量和内容的变化频率。如果您的网站内容变化不频繁，可以使用较长的TTL。如果您的网站需要快速响应变化，可以使用较短的TTL。

- 如果您有特定的性能要求，可以根据地区和运营商选择不同的TTL值。例如，可以为中国地区使用较短的TTL，为其他地区使用较长的TTL。

请根据您的具体需求和情况配置TTL以及其他参数，以确保您的DNS解析记录与您的应用程序和网站的性能和可用性要求相匹配。
<img width="1201" alt="image" src="https://github.com/ymyuuu/Preferred-IP/assets/135582157/8430e5d3-4868-4eef-9634-dc91a7fb88c3">

---

**注意事项：**

- 请确保保护您的腾讯云API密钥（`SECRETID` 和 `SECRETKEY`），不要将其泄露。

- 使用GitHub Actions可能会消耗您的GitHub Action分钟数，确保您有足够的资源支持定期更新DNS记录。

- 如果出现任何问题或错误消息，您可以在GitHub Actions的日志中查找更多信息。

Preferred-IP 是一个强大的工具，可以帮助您提高网站性能、可用性和自动化DNS管理。希望这个工具对您有所帮助。如果您需要进一步的支持或有任何问题，请查看项目的文档或随时提问。

## 许可证

本项目采用 MIT 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。

感谢你的使用！如果你对这个项目有任何改进或建议，也欢迎贡献代码或提出问题。