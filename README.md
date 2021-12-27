## aria2-python-script
为TrueNAS CORE的Aria2添加下载完成自动推送通知等功能。
### 基本功能
- 从“正在下载”删除任务时，自动删除未下载完文件、.aria2文件以及种子文件。
- BT任务下载完成时，自动删除种子。
- 任务下载完成时，自动推送通知到手机。
> 支持通过Bark和Server酱两种方式推送通知到手机。
### 如何使用
- 将scripts文件夹上传到aria2.conf目录下。
- 安装依赖模块

`pip install magneturi`

- 将device-key或send-key填入aria2.py

`"device_key": "your_device_key"`

`send_key = "your_send_key"`

- 在complete.py中打开或关闭消息推送

`#push2bark(get_contents())            #默认关闭，打开删除前面的"#"。`

`#push2serverchen(get_contents())      #默认关闭，打开删除前面的"#"。`

- 配置aria2.conf

`on-download-stop=/your_aria2.conf_path/scripts/stop.sh`

`on-download-complete=/your_aria2.conf_path/scripts/complete.sh`

- 重启Aria2
