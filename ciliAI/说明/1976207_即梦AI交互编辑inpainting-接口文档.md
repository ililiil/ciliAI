# 即梦AI交互编辑inpainting-接口文档

> 来源: https://www.volcengine.com/docs/85621/1976207

---

# 接口简介
即梦「局部重绘」「消除笔」同款图像编辑功能：用户可通过涂抹、选区等方式建立重绘区域，将相应mask图及文本prompt传入模型，即可重新编辑生成图片。
本能力支持涂抹消除，和涂抹编辑场景，在消除的场景，输入prompt文本为删除即可；在涂抹编辑场景，可以用自然语言描述预期生成的内容，涉及文字内容的修改建议讲修改后的文字放在“”双引号内，会提升准确率
 

# 接入说明
在智能视觉控制台，[开通服务](https://console.volcengine.com/ai/ability/detail/2)后调用
![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_1611095f5809701bac2948d71da18b38.png =944x) 

# 接口说明

## 限制条件

|名称 |内容 |
|---|---|
|输入图要求 |1. 图片格式：仅支持JPEG、PNG格式，建议使用JPEG格式；|
| |2. 图片文件大小：最大 4.7MB，图片分辨率：最大 4096 * 4096。 |

## 请求说明

|名称 |内容 |
|---|---|
|接口地址 |[https://visual.volcengineapi.com](https://visual.volcengineapi.com/) |
|请求方式 |POST |
|Content-Type |application/json |

## 提交任务

### **提交任务请求参数**

#### **Query参数**
:::tip 拼接到url后的参数，示例：[https://visual.volcengineapi.com?Action=CVSync2AsyncSubmitTask&Version=2022-08-31](https://visual.volcengineapi.com?Action=CVSync2AsyncSubmitTask&Version=2022-08-31)

:::
|参数 |类型 |**可选/必选** |说明 |
|---|---|---|---|
|Action |string |必选 |接口名，取值：**CVSync2AsyncSubmitTask** |
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
| | | |取固定值: **jimeng_image2image_dream_inpaint** |
|binary_data_base64 |array of string |必选（二选一） |图片文件base64编码，需输入**2**张图片|
| | | ||
| | | |* 第一张为原图|
| | | |* 第二张为涂抹后的mask图。mask图为单通道灰度图，其中原图保持部分像素值为0（即黑色区域），待重绘部分像素值为255（即白色区域） |
|image_urls |array of string |^^|图片文件URL，需输入**2**张图片|
| | | ||
| | | |* 第一张为原图|
| | | |* 第二张为涂抹后的mask图。mask图为单通道灰度图，其中原图保持部分像素值为0（即黑色区域），待重绘部分像素值为255（即白色区域） |
|prompt |string |必选 |用于编辑图像的提示词，支持中英文，建议长度 删除即可|
| | | |* 在涂抹编辑场景，可以用自然语言描述预期生成的内容，涉及文字内容的修改建议讲修改后的文字放在“”双引号内，会提升准确率 |
|seed |int |可选 |随机种子，作为确定扩散初始状态的基础（-1表示随机）。若随机种子为相同正整数且其他参数均一致，则生成内容极大概率效果一致|
| | | |默认值：101  |

### 提交任务返回参数

#### **通用返回参数**
请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)

#### **业务返回参数**
:::tip 重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::
|字段 |类型 |说明 |
|---|---|---|
|task_id |string |任务ID，用于查询结果 |

### 提交任务请求&返回完整示例
**请求示例：** 
```JSON
{
    "req_key": "jimeng_image2image_dream_inpaint