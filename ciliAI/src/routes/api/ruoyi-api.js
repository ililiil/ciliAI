/**
 * RuoYi API 模块
 * 对接 RuoYi 后端
 */

const BASE_URL = '/api'

/**
 * 认证相关 API
 */
export const authAPI = {
  // 登录
  login: (username, password) => {
    return fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    }).then(res => res.json())
  },

  // 获取用户信息
  getUserInfo: (token) => {
    return fetch(`${BASE_URL}/getInfo`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 注册
  register: (userData) => {
    return fetch(`${BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    }).then(res => res.json())
  }
}

/**
 * 邀请码 API
 */
export const inviteCodeAPI = {
  // 验证邀请码
  validate: (code, userId) => {
    return fetch(`${BASE_URL}/system/invitecode/validate?code=${code}&userId=${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res => res.json())
  },

  // 获取邀请码列表
  list: (token) => {
    return fetch(`${BASE_URL}/system/invitecode/list`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 生成邀请码
  generate: (params, token) => {
    return fetch(`${BASE_URL}/system/invitecode/batchGenerate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    }).then(res => res.json())
  }
}

/**
 * 算力 API
 */
export const powerAPI = {
  // 获取用户算力
  getByUserId: (userId, token) => {
    return fetch(`${BASE_URL}/system/computepower/user/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 算力充值
  recharge: (userId, amount, token) => {
    return fetch(`${BASE_URL}/system/computepower/recharge/${userId}?amount=${amount}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 算力消费
  consume: (userId, amount, token) => {
    return fetch(`${BASE_URL}/system/computepower/consume/${userId}?amount=${amount}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  }
}

/**
 * 作品 API
 */
export const worksAPI = {
  // 获取作品列表
  list: (params = {}, token) => {
    const query = new URLSearchParams(params)
    return fetch(`${BASE_URL}/works/list?${query}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 创建作品
  create: (workData, token) => {
    return fetch(`${BASE_URL}/works`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(workData)
    }).then(res => res.json())
  },

  // 获取作品详情
  getById: (id, token) => {
    return fetch(`${BASE_URL}/works/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 更新作品
  update: (id, workData, token) => {
    return fetch(`${BASE_URL}/works/${id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(workData)
    }).then(res => res.json())
  },

  // 删除作品
  delete: (id, token) => {
    return fetch(`${BASE_URL}/works/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  }
}

/**
 * AI 生成 API
 */
export const aiAPI = {
  // 文生图
  text2img: (params, token) => {
    return fetch(`${BASE_URL}/ai/text2img`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    }).then(res => res.json())
  },

  // 图生图
  img2img: (params, token) => {
    return fetch(`${BASE_URL}/ai/img2img`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    }).then(res => res.json())
  },

  // 视频生成
  video: (params, token) => {
    return fetch(`${BASE_URL}/ai/video`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    }).then(res => res.json())
  },

  // 查询任务状态
  getTaskStatus: (taskId, token) => {
    return fetch(`${BASE_URL}/ai/task/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  }
}

/**
 * 订单 API
 */
export const orderAPI = {
  // 创建订单
  create: (orderData, token) => {
    return fetch(`${BASE_URL}/order/create`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    }).then(res => res.json())
  },

  // 获取订单列表
  list: (params = {}, token) => {
    const query = new URLSearchParams(params)
    return fetch(`${BASE_URL}/order/list?${query}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 获取订单详情
  getByNo: (orderNo, token) => {
    return fetch(`${BASE_URL}/order/${orderNo}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 取消订单
  cancel: (id, token) => {
    return fetch(`${BASE_URL}/order/${id}/cancel`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  }
}

/**
 * 项目 API
 */
export const projectAPI = {
  // 获取项目列表
  list: (params = {}, token) => {
    const query = new URLSearchParams(params)
    return fetch(`${BASE_URL}/project/list?${query}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 创建项目
  create: (projectData, token) => {
    return fetch(`${BASE_URL}/project`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(projectData)
    }).then(res => res.json())
  },

  // 获取项目详情
  getById: (id, token) => {
    return fetch(`${BASE_URL}/project/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  },

  // 开始生成
  startGenerate: (id, token) => {
    return fetch(`${BASE_URL}/project/${id}/generate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }).then(res => res.json())
  }
}

export default {
  auth: authAPI,
  inviteCode: inviteCodeAPI,
  power: powerAPI,
  works: worksAPI,
  ai: aiAPI,
  order: orderAPI,
  project: projectAPI
}
