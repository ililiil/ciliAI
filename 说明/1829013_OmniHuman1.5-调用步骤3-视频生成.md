# OmniHuman1.5-调用步骤3-视频生成

> 来源: https://www.volcengine.com/docs/85621/1829013

---

# 接口简介
OmniHuman1.5（即梦同源数字人模型），该模型可根据用户上传的**单张图片+音频**，生成与图片对应的**视频效果**。支持输入任意画幅包含人物或其他主体（宠物、动漫等）的图片，结合音频，生成高质量的视频。
人物的情绪、动作与音频具有强关联性，支持通过提示词（prompt）对画面、动作、运镜进行调整。同时OmniHuman1.5对动漫、宠物等形象支持较好，允许指定讲话人/主体，可广泛应用于内容表达、唱歌和表演等场景。
相较于上一代模型，OmniHuman1.5 在**运动自然度和结构稳定性**提升明显，在**人物/主体的运动表现力和画面质量上更优。** 可以广泛应用于制作剧情对话、多人对话/对唱、商品交互、漫剧等内容。对比其他视频通用模型，OmniHuman 数字人大模型在**人物/主体的剧情演绎效果**上极具优势。

# 接入说明

## 请求说明

|名称 |内容 |
|---|---|
|接口地址 |[https://visual.volcengineapi.com](https://visual.volcengineapi.com/) |
|请求方式 |POST |
|Content-Type |application/json |

## 提交任务

### **提交任务请求参数**
**Query参数**
:::tip 拼接到url后的参数，示例：[https://visual.volcengineapi.com?Action=CVSubmitTask&Version=2022-08-31](https://visual.volcengineapi.com?Action=CVSubmitTask&Version=2022-08-31)

:::
|参数 |类型 |**可选/必选** |说明 |
|---|---|---|---|
|Action |string |必选 |接口名，取值：**CVSubmitTask** |
|Version |string |必选 |版本号，取值：2022-08-31 |

#### **Header参数**
:::warning
本服务固定值：**Region为cn-north-1，Service为cv**
:::
主要用于鉴权，详见 [公共参数](https://www.volcengine.com/docs/6369/67268) - 签名参数 - 在Header中的场景部分

#### **Body参数**
:::warning
业务请求参数，放到request.body中，MIME-Type为**application/json**

:::
|名称 |类型 |必选 |描述 |
|---|---|---|---|
|req_key |string |必选 |服务标识|
| | | |取固定值: **jimeng_realman_avatar_picture_omni_v15** |
|image_url |string |必选 |人像图片URL链接 |
|mask_url |array of string |可选 |mask图URL列表|
| | | |如果需要指定图片中的某个主体说话，可通过**调用步骤2：主体检测**获取对应主体的mask图传入 |
|audio_url |string |必选 |音频URL|
| | | |音频时长必须小于60秒，过长情况下提交任务正常，查询任务会报错如下：|
| | | |```JSON|
| | | |{|
| | | |    "code": 50215,|
| | | |    "data": null,|
| | | |    "message": "Input invalid for this service.