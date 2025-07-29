# multi-channel

## 项目介绍
multi-channel is a test project


## 项目实现功能

* 实现游戏和渠道assets/libs/res/AndroidManifest.xml资源的动态合并
* 实现整体UI界面的可视化配置。
* 实现渠道资源的服务器下载功能。（注意：当前下载资源只是用于模拟下载功能，没有实际用途，需开发者自行配置）
* 支持渠道参数可视化差异性配置，及支持多种类型解析及修改，如xml/text/ini/pro/json等类型文件
* 支持游戏Icon和角标的可视化配置，及Icon和角标的合并
* 支持游戏闪屏可视化配置，及游戏闪屏和渠道闪屏逻辑兼容处理
* 支持游戏的包体输出路径，签名信息的可视化配置。
* 支持动态修改游戏的minSdk、TargetSdk、包名等配置
* 支持游戏第三方库多包名R文件资源引用配置,在渠道参数栏填写 R_package为字符数组["a","b"] 即可。
* 支持打包过程的日志信息显示及日志输出


## 项目功能使用示例

### 渠道资源包说明：
格式为：渠道名_渠道ID_渠道版本。 内置为渠道资源目录 

* assets 为渠道assets资源目录，与游戏assets目录合并
* config 为配置文件资源目录，可根据需求拓展
* icon 为渠道角标资源目录，与游戏自有Icon合并
* libs 为渠道.jar和.so文件资源目录，与游戏lib目录合并
* res 为渠道res资源目录,与游戏res资源目录合并
* splash 为渠道闪屏资源目录，打包时，拷贝到assets对应目录下
* wxcallback 为渠道处理微信登录、支付特殊处理的类文件，打包时会编译成jar文件，最终打包到游戏包内
* AndroidManifest.xml 为渠道配置文件，与游戏AndroidManifest.xml合并


