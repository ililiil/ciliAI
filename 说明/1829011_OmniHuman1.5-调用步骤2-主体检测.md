# OmniHuman1.5-调用步骤2-主体检测

> 来源: https://www.volcengine.com/docs/85621/1829011

---

# 接口简介
检测图片中的主体，并支持返回主体对应的mask图。如果在视频生成时不需要指定主体说话，可以跳过该步骤。

# 接入说明

## 请求说明

|名称 |内容 |
|---|---|
|接口地址 |[https://visual.volcengineapi.com](https://visual.volcengineapi.com/) |
|请求方式 |POST |
|Content-Type |application/json |

### **请求参数**

#### **Query参数**
:::tip 拼接到url后的参数，示例：[https://visual.volcengineapi.com?Action=CVProcess&Version=2022-08-31](https://visual.volcengineapi.com?Action=CVProcess&Version=2022-08-31)

:::
|参数 |类型 |**可选/必选** |说明 |
|---|---|---|---|
|Action |string |必选 |接口名，取值：**CVProcess** |
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
| | | |取固定值: **jimeng_realman_avatar_object_detection** |
|image_url |string |必选 |人像图片URL链接 **（最多支持检测5个主体）**  |

### 返回参数

#### **通用返回参数**
请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)

#### **业务返回参数**
:::tip 重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::
|字段 |类型 |说明 |
|---|---|---|
|resp_data |JSON string |图片识别结果中各字段说明：|
| | ||
| | |* code：错误码，0表示成功|
| | |* status：是否包含主体，0表示不包含主体，1表示包含主体|
| | |* **object_detection_result.mask.url（重点关注此字段）** ：图片中主体对应的mask图URL列表。**URL列表顺序与输入图中主体按照mask的面积进行排序** **。URL有效期为1小时。如需预览mask图片，可以通过URL下载并手动修改图片文件名的格式后缀为.png，保存为.png后再查看。**  |

### 请求&返回完整示例
**请求示例：** 
```JSON
{
    "req_key": "jimeng_realman_avatar_object_detection