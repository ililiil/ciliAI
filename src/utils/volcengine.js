// 火山引擎API配置
const VOLCENGINE_CONFIG = {
  region: 'cn-north-1',
  service: 'cv',
  endpoint: 'https://visual.volcengineapi.com'
}

// 模拟API响应，用于开发测试
const mockResponse = {
  code: 10000,
  data: {
    task_id: `task_${Date.now()}`
  },
  message: 'Success',
  request_id: `req_${Date.now()}`
}

// 生成当前时间戳
const getCurrentTimestamp = () => {
  const date = new Date()
  const year = date.getUTCFullYear()
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const day = String(date.getUTCDate()).padStart(2, '0')
  const hours = String(date.getUTCHours()).padStart(2, '0')
  const minutes = String(date.getUTCMinutes()).padStart(2, '0')
  const seconds = String(date.getUTCSeconds()).padStart(2, '0')
  return `${year}${month}${day}T${hours}${minutes}${seconds}Z`
}

// 生成短日期
const getShortDate = () => {
  const date = new Date()
  const year = date.getUTCFullYear()
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const day = String(date.getUTCDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

// 工具函数：将字符串转换为ArrayBuffer
const stringToBuffer = (str) => {
  const encoder = new TextEncoder()
  return encoder.encode(str)
}

// 工具函数：将ArrayBuffer转换为十六进制字符串
const bufferToHex = (buffer) => {
  return Array.from(new Uint8Array(buffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}

// 工具函数：计算SHA256哈希
const sha256 = async (data) => {
  const buffer = typeof data === 'string' ? stringToBuffer(data) : data
  const hash = await crypto.subtle.digest('SHA-256', buffer)
  return bufferToHex(hash)
}

// 工具函数：计算HMAC-SHA256
const hmacSha256 = async (key, data) => {
  const keyBuffer = typeof key === 'string' ? stringToBuffer(key) : key
  const dataBuffer = typeof data === 'string' ? stringToBuffer(data) : data
  
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyBuffer,
    { name: 'HMAC', hash: { name: 'SHA-256' } },
    false,
    ['sign']
  )
  
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, dataBuffer)
  return new Uint8Array(signature)
}

// 生成签名
const generateSignature = async (accessKeyId, secretAccessKey, method, uri, headers, payload) => {
  console.log('开始生成签名:', {
    accessKeyId,
    method,
    uri,
    headers,
    payload
  })
  
  // 1. 准备签名字符串
  const timestamp = getCurrentTimestamp()
  const shortDate = getShortDate()
  
  console.log('时间戳:', { timestamp, shortDate })
  
  // 2. 构建CanonicalRequest
  const canonicalHeaders = Object.entries(headers)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key.toLowerCase()}:${value}`)
    .join('\n')
  
  const signedHeaders = Object.keys(headers)
    .sort()
    .map(key => key.toLowerCase())
    .join(';')
  
  const payloadHash = await sha256(JSON.stringify(payload))
  
  const canonicalRequest = `${method}\n${uri}\n\n${canonicalHeaders}\n\n${signedHeaders}\n${payloadHash}`
  
  console.log('CanonicalRequest:', canonicalRequest)
  
  // 3. 构建StringToSign
  const credentialScope = `${shortDate}/${VOLCENGINE_CONFIG.region}/${VOLCENGINE_CONFIG.service}/request`
  const canonicalRequestHash = await sha256(canonicalRequest)
  const stringToSign = `HMAC-SHA256\n${timestamp}\n${credentialScope}\n${canonicalRequestHash}`
  
  console.log('StringToSign:', stringToSign)
  
  // 4. 计算签名
  const kDate = await hmacSha256(`AWS4${secretAccessKey}`, shortDate)
  const kRegion = await hmacSha256(kDate, VOLCENGINE_CONFIG.region)
  const kService = await hmacSha256(kRegion, VOLCENGINE_CONFIG.service)
  const kSigning = await hmacSha256(kService, 'request')
  const signature = await hmacSha256(kSigning, stringToSign)
  const signatureHex = bufferToHex(signature)
  
  console.log('计算签名:', signatureHex)
  
  // 5. 构建Authorization头
  const authorization = `HMAC-SHA256 Credential=${accessKeyId}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signatureHex}`
  
  console.log('生成的Authorization头:', authorization)
  
  return { authorization, timestamp }
}

// 发送API请求到后端服务器
export const sendVolcEngineRequest = async (action, payload, accessKeyId, secretAccessKey, inviteCode, projectId) => {
  console.log('开始发送API请求到后端:', {
    action,
    payload,
    inviteCode: inviteCode ? '***' : undefined,
    projectId
  })
  
  try {
    // 构建请求URL - 调用后端的API接口
    const url = 'http://localhost:5001/api/generate'
    
    // 构建请求参数
    const requestData = {
      prompt: payload.prompt,
      width: payload.width,
      height: payload.height,
      invite_code: inviteCode,
      project_id: projectId
    }
    
    // 添加参考图参数
    if (payload.image_urls && payload.image_urls.length > 0) {
      requestData.reference_image = payload.image_urls[0]
    }
    
    console.log('发送请求到:', url)
    console.log('请求体:', requestData)
    
    // 发送请求
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    console.log('请求响应状态:', response.status, response.statusText)
    
    // 检查响应状态
    if (!response.ok) {
      // 尝试获取错误详情
      let errorDetails = ''
      try {
        const errorData = await response.clone().json()
        errorDetails = JSON.stringify(errorData)
      } catch (e) {
        const text = await response.clone().text()
        // 清理 HTML 标签，只保留错误信息
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = text
        errorDetails = tempDiv.textContent || tempDiv.innerText || text
      }
      throw new Error(`API请求失败: ${response.status} ${response.statusText}\n错误详情: ${errorDetails}`)
    }
    
    // 解析响应
    const data = await response.json()
    
    console.log('API响应:', data)
    
    // 检查响应状态
    if (data.status !== 'success') {
      throw new Error(`API返回错误: ${data.error}`)
    }
    
    // 转换响应格式，使其与前端期望的格式一致
    console.log('后端返回的images:', data.images)
    
    // 确保返回的是正确的图片URL格式
    const formattedImages = data.images.map(item => {
      // 如果item是字符串
      if (typeof item === 'string') {
        // 检查是否是base64编码的数据
        if (item.startsWith('data:image/')) {
          // 已经是data URL，直接使用
          return { url: item }
        } else if (item.length > 100) {
          // 可能是base64编码的图片数据，转换为data URL
          return { url: `data:image/png;base64,${item}` }
        } else {
          // 可能是图片URL，直接使用
          return { url: item }
        }
      }
      // 如果item是对象，使用其url属性
      else if (typeof item === 'object' && item.url) {
        return { url: item.url }
      }
      // 否则返回一个默认值
      else {
        return { url: '' }
      }
    })
    
    console.log('格式化后的images:', formattedImages)
    
    return {
      code: 10000,
      data: {
        task_id: data.task_id,
        images: formattedImages,
        remaining_power: data.remaining_power || 0,
        power_cost: data.power_cost || 0
      },
      message: 'Success',
      request_id: `req_${Date.now()}`
    }
  } catch (error) {
    console.error('API调用失败:', error)
    throw error
  }
}

// 生图API
export const generateImage = async (params, accessKeyId, secretAccessKey, inviteCode, projectId) => {
  const payload = {
    req_key: 'jimeng_seedream46_cvtob',
    prompt: params.prompt
  }
  
  // 添加可选参数
  if (params.width && params.height) {
    payload.width = params.width
    payload.height = params.height
  } else if (params.size) {
    payload.size = params.size
  }
  
  if (params.referenceImage) {
    payload.image_urls = [params.referenceImage]
  }
  
  if (params.scale) {
    payload.scale = params.scale
  }
  
  if (params.force_single !== undefined) {
    payload.force_single = params.force_single
  }
  
  if (params.min_ratio) {
    payload.min_ratio = params.min_ratio
  }
  
  if (params.max_ratio) {
    payload.max_ratio = params.max_ratio
  }
  
  if (params.seed) {
    payload.seed = params.seed
  }
  
  if (params.callback_url) {
    payload.callback_url = params.callback_url
  }
  
  if (params.return_url !== undefined) {
    payload.return_url = params.return_url
  }
  
  console.log('生图API请求参数:', payload)
  return sendVolcEngineRequest('CVSync2AsyncSubmitTask', payload, accessKeyId, secretAccessKey, inviteCode, projectId)
}

// 改图API
export const editImage = async (params, accessKeyId, secretAccessKey, inviteCode, projectId) => {
  console.log('调用改图API:', params)
  
  try {
    const url = 'http://localhost:5001/api/inpaint'
    
    const requestData = {
      image: params.image,
      mask: params.mask,
      prompt: params.prompt,
      invite_code: inviteCode,
      project_id: projectId
    }
    
    console.log('发送改图请求到:', url)
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      let errorDetails = ''
      try {
        const errorData = await response.clone().json()
        errorDetails = JSON.stringify(errorData)
      } catch (e) {
        errorDetails = await response.clone().text()
      }
      throw new Error(`改图API请求失败: ${response.status} ${response.statusText}\n错误详情: ${errorDetails}`)
    }
    
    const data = await response.json()
    console.log('改图API响应:', data)
    
    if (data.status !== 'success') {
      throw new Error(`改图API返回错误: ${data.error}`)
    }
    
    const formattedImages = data.images.map(item => {
      if (typeof item === 'string') {
        if (item.startsWith('data:image/')) {
          return { url: item }
        } else if (item.length > 100) {
          return { url: `data:image/png;base64,${item}` }
        } else {
          return { url: item }
        }
      } else if (typeof item === 'object' && item.url) {
        return { url: item.url }
      } else {
        return { url: '' }
      }
    })
    
    return {
      code: 10000,
      data: {
        task_id: data.task_id,
        images: formattedImages,
        remaining_power: data.remaining_power || 0,
        power_cost: data.power_cost || 0
      },
      message: 'Success',
      request_id: `req_${Date.now()}`
    }
  } catch (error) {
    console.error('改图API调用失败:', error)
    throw error
  }
}

// 扩图API
export const extendImage = async (params, accessKeyId, secretAccessKey, inviteCode, projectId) => {
  console.log('调用扩图API:', params)
  
  try {
    const url = 'http://localhost:5001/api/extend'
    
    const requestData = {
      image: params.image,
      prompt: params.prompt || '',
      width: params.width || 2048,
      height: params.height || 2048,
      invite_code: inviteCode,
      project_id: projectId
    }
    
    console.log('发送扩图请求到:', url)
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      let errorDetails = ''
      try {
        const errorData = await response.clone().json()
        errorDetails = JSON.stringify(errorData)
      } catch (e) {
        errorDetails = await response.clone().text()
      }
      throw new Error(`扩图API请求失败: ${response.status} ${response.statusText}\n错误详情: ${errorDetails}`)
    }
    
    const data = await response.json()
    console.log('扩图API响应:', data)
    
    if (data.status !== 'success') {
      throw new Error(`扩图API返回错误: ${data.error}`)
    }
    
    const formattedImages = data.images.map(item => {
      if (typeof item === 'string') {
        if (item.startsWith('data:image/')) {
          return { url: item }
        } else if (item.length > 100) {
          return { url: `data:image/png;base64,${item}` }
        } else {
          return { url: item }
        }
      } else if (typeof item === 'object' && item.url) {
        return { url: item.url }
      } else {
        return { url: '' }
      }
    })
    
    return {
      code: 10000,
      data: {
        task_id: data.task_id,
        images: formattedImages,
        remaining_power: data.remaining_power || 0,
        power_cost: data.power_cost || 0
      },
      message: 'Success',
      request_id: `req_${Date.now()}`
    }
  } catch (error) {
    console.error('扩图API调用失败:', error)
    throw error
  }
}

// 智能超清API
export const superResolution = async (params, accessKeyId, secretAccessKey, inviteCode, projectId) => {
  console.log('调用智能超清API:', params)
  
  try {
    const url = 'http://localhost:5001/api/super-resolution'
    
    const requestData = {
      image: params.image,
      resolution: params.resolution || '4k',
      invite_code: inviteCode,
      project_id: projectId
    }
    
    console.log('发送智能超清请求到:', url)
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      let errorDetails = ''
      try {
        const errorData = await response.clone().json()
        errorDetails = JSON.stringify(errorData)
      } catch (e) {
        errorDetails = await response.clone().text()
      }
      throw new Error(`智能超清API请求失败: ${response.status} ${response.statusText}\n错误详情: ${errorDetails}`)
    }
    
    const data = await response.json()
    console.log('智能超清API响应:', data)
    
    if (data.status !== 'success') {
      throw new Error(`智能超清API返回错误: ${data.error}`)
    }
    
    const formattedImages = data.images.map(item => {
      if (typeof item === 'string') {
        if (item.startsWith('data:image/')) {
          return { url: item }
        } else if (item.length > 100) {
          return { url: `data:image/png;base64,${item}` }
        } else {
          return { url: item }
        }
      } else if (typeof item === 'object' && item.url) {
        return { url: item.url }
      } else {
        return { url: '' }
      }
    })
    
    return {
      code: 10000,
      data: {
        task_id: data.task_id,
        images: formattedImages,
        remaining_power: data.remaining_power || 0,
        power_cost: data.power_cost || 0
      },
      message: 'Success',
      request_id: `req_${Date.now()}`
    }
  } catch (error) {
    console.error('智能超清API调用失败:', error)
    throw error
  }
}

// 获取算力API
export const getComputePower = async (inviteCode) => {
  try {
    const url = `http://localhost:5001/api/compute-power?invite_code=${encodeURIComponent(inviteCode || '')}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error(`获取算力失败: ${response.status}`)
    }
    
    const data = await response.json()
    return data.算力 || 0
  } catch (error) {
    console.error('获取算力失败:', error)
    return 0
  }
}

// 查询任务结果API
export const getTaskResult = async (taskId, accessKeyId, secretAccessKey) => {
  const payload = {
    task_id: taskId
  }
  
  return sendVolcEngineRequest('CVSync2AsyncGetResult', payload, accessKeyId, secretAccessKey)
}

// 轮询任务结果 - 由于后端已经处理了轮询逻辑，这里直接返回任务结果
export const pollTaskResult = async (taskId, accessKeyId, secretAccessKey, maxRetries = 30, interval = 2000) => {
  console.log('轮询任务结果:', taskId)
  
  // 由于后端已经在/api/generate接口中处理了轮询逻辑
  // 这里直接返回一个模拟的成功响应，因为实际的图片数据已经在submitResponse中返回了
  return {
    code: 10000,
    data: {
      task_id: taskId,
      status: 'success',
      images: [] // 实际的图片数据会在sendVolcEngineRequest中返回
    },
    message: 'Success',
    request_id: `req_${Date.now()}`
  }
}