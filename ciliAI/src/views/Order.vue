<template>
  <div class="order-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">接单广场</h1>
      <button class="publish-btn" @click="showPublishModal = true" v-show="false">发布商单</button>
    </div>

    <!-- 标签筛选 -->
    <div class="filter-tabs">
      <div
        v-for="tab in tabs"
        :key="tab.value"
        class="tab-item"
        :class="{ active: activeTab === tab.value }"
        @click="handleTabChange(tab.value)"
      >
        {{ tab.label }}
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <div v-if="filteredOrders.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
            <line x1="3" x2="21" y1="9" y2="9"></line>
            <line x1="9" x2="9" y1="21" y2="9"></line>
          </svg>
        </div>
        <p class="empty-text">暂无作品</p>
      </div>

      <div v-else class="order-grid">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="order-card"
          @click="viewOrderDetail(order)"
        >
          <div class="order-image">
            <img :src="getImageUrl(order)" :alt="order.title" @error="handleImageError($event, order)">
            <div class="order-status" :class="order.status">{{ getStatusText(order.status) }}</div>
          </div>
          <div class="order-info">
            <h3 class="order-title">{{ order.title }}</h3>
            <div class="order-meta">
              <span class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2v20"></path>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
                {{ order.price }}
              </span>
              <span class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {{ order.deadline }}
              </span>
              <span class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
                已联系: {{ order.contactCount }}
              </span>
            </div>
            <div class="order-footer">
              <div class="order-tags">
                <span v-for="tag in order.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <span class="contact-btn" @click.stop="handleContact(order)">立即联系&gt;</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 联系弹窗 -->
  <el-dialog
    v-model="showContactModal"
    title="联系方式"
    width="450px"
    class="contact-dialog"
  >
    <div class="contact-content" v-if="selectedOrder">
      <div class="qrcode-wrapper">
        <img 
          :src="getQrcodeUrl(selectedOrder.qrcode)" 
          alt="企业微信二维码" 
          class="qrcode-image"
          @error="handleQrcodeError($event)"
        >
      </div>
      <div class="contact-info">
        <h3 class="order-title">{{ selectedOrder.title }}</h3>
        <p class="contact-tip">请扫描上方二维码添加企业微信</p>
        <p class="contact-note">添加时请注明"接单"，我们的商务人员会尽快与您联系</p>
      </div>
    </div>
    <div v-else class="contact-empty">
      <el-empty description="暂无联系方式" />
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showContactModal = false">关闭</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 发布商单弹窗 -->
  <el-dialog
    v-model="showPublishModal"
    title="发布商单"
    width="600px"
    class="publish-dialog"
  >
    <!-- 提示信息 -->
    <div class="warning-box">
      <el-icon><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" x2="12" y1="9" y2="13"></line><line x1="12" x2="12.01" y1="17" y2="17"></line></svg></el-icon>
      <div class="warning-text">
        <p>首次发布商单需要完成企业资质审核</p>
        <p>请准备好营业执照、剧本版权证明等资料，提交后我们的商务团队会与您联系。</p>
      </div>
    </div>

    <el-form :model="publishForm" label-position="top">
      <!-- 商单标题 -->
      <el-form-item label="商单标题 *">
        <el-input v-model="publishForm.title" placeholder="例如：都市爱情短剧《心动时刻》"></el-input>
      </el-form-item>

      <!-- 短剧类型 -->
      <el-form-item label="短剧类型 *">
        <el-select v-model="publishForm.type" placeholder="请选择短剧类型">
          <el-option label="都市" value="都市"></el-option>
          <el-option label="古装" value="古装"></el-option>
          <el-option label="科幻" value="科幻"></el-option>
          <el-option label="其他" value="其他"></el-option>
        </el-select>
      </el-form-item>

      <!-- 收益相关 -->
      <div class="form-row">
        <el-form-item label="保底收益(元) *">
          <el-input v-model="publishForm.minProfit" type="number" placeholder="0"></el-input>
        </el-form-item>
        <el-form-item label="分成比例(%) *">
          <el-input v-model="publishForm.shareRatio" type="number" placeholder="0"></el-input>
        </el-form-item>
        <el-form-item label="算力补贴(算力) *">
          <el-input v-model="publishForm.powerSubsidy" type="number" placeholder="0"></el-input>
        </el-form-item>
      </div>

      <!-- 时间相关 -->
      <div class="form-row">
        <el-form-item label="抢单开始时间 *">
          <el-date-picker v-model="publishForm.startTime" type="datetime" placeholder="抢单开始时间"></el-date-picker>
        </el-form-item>
        <el-form-item label="抢单截止时间 *">
          <el-date-picker v-model="publishForm.endTime" type="datetime" placeholder="抢单截止时间"></el-date-picker>
        </el-form-item>
      </div>

      <!-- 制作周期 -->
      <el-form-item label="制作周期（天） *">
        <el-input v-model="publishForm.period" type="number" placeholder="0"></el-input>
      </el-form-item>

      <!-- 试镜剧本 -->
      <el-form-item label="试镜剧本 *">
        <el-input v-model="publishForm.auditionScript" type="textarea" placeholder="输入试镜剧本内容，供创作者试镜使用" rows="4"></el-input>
      </el-form-item>

      <!-- 商单描述 -->
      <el-form-item label="商单描述 *">
        <el-input v-model="publishForm.description" type="textarea" placeholder="详细描述项目需求、风格要求、成片时长等信息" rows="4"></el-input>
      </el-form-item>

      <!-- 剧本上传 -->
      <el-form-item label="剧本上传">
        <el-upload
          class="script-upload"
          :action="''"
          :auto-upload="false"
          :on-change="handleScriptUpload"
          :file-list="scriptFileList"
          accept=".pdf,.doc,.docx"
        >
          <el-button type="primary">上传剧本文件</el-button>
          <template #tip>
            <div class="el-upload__tip">支持 PDF、DOC、DOCX 格式</div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 封面上传 -->
      <el-form-item label="封面上传 *">
        <div class="cover-upload-container">
          <el-upload
            class="cover-upload"
            :action="''"
            :auto-upload="false"
            :on-change="handleCoverUpload"
            :file-list="coverFileList"
            :show-file-list="false"
            accept=".jpg,.jpeg,.png"
          >
            <template #default>
              <div class="cover-upload-trigger" v-if="!uploadedCoverUrl">
                <el-button type="primary" size="large">
                  <el-icon><Upload /></el-icon>
                  上传封面
                </el-button>
                <div class="cover-upload-hint">支持 JPG、PNG 格式，建议尺寸 500x892</div>
              </div>
              <div class="cover-preview" v-else>
                <img :src="uploadedCoverUrl" alt="封面预览" class="cover-preview-image">
                <div class="cover-preview-overlay">
                  <el-button type="primary" size="small" @click.stop="removeCover">更换封面</el-button>
                </div>
              </div>
            </template>
          </el-upload>
        </div>
      </el-form-item>

      <!-- 联系方式 -->
      <el-form-item label="联系方式">
        <el-upload
          class="qrcode-upload"
          :action="''"
          :auto-upload="false"
          :on-change="handleQrcodeUpload"
          :file-list="qrcodeFileList"
          accept=".jpg,.jpeg,.png"
        >
          <el-button type="primary">上传企业微信二维码</el-button>
          <template #tip>
            <div class="el-upload__tip">支持 JPG、PNG 格式</div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 参与条件 -->
      <el-form-item label="参与条件">
        <div class="participation-options">
          <el-button :class="{ active: publishForm.participation === 'all' }" @click="publishForm.participation = 'all'">
            <el-icon v-if="publishForm.participation === 'all'"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></el-icon>
            全员可参与
          </el-button>
          <el-button :class="{ active: publishForm.participation === 'member' }" @click="publishForm.participation = 'member'">
            <el-icon v-if="publishForm.participation === 'member'" class="check-icon"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></el-icon>
            登录用户
          </el-button>
        </div>
      </el-form-item>

      <!-- 版权声明 -->
      <el-form-item>
        <el-checkbox v-model="publishForm.copyright" disabled>默认版权声明：剧本版权归需求方所有</el-checkbox>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showPublishModal = false">取消</el-button>
        <el-button type="primary" class="submit-btn" @click="handleSubmit">提交审核</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, inject } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElEmpty } from 'element-plus'

const inviteCode = inject('currentInviteCode')

// 标签选项
const tabs = [
  { label: '全部', value: 'all' },
  { label: '待开始', value: 'pending' },
  { label: '招募中', value: 'recruiting' },
  { label: '已结束', value: 'ended' }
]

const activeTab = ref('all')

// 订单数据 - 从后端API获取
const orders = ref([])

// 轮询间隔（毫秒）
const POLL_INTERVAL = 5000

// 定时器 ID
let pollTimer = null

// 图片缓存破坏参数
const imageCacheBuster = ref(Date.now())

// 初始化订单数据 - 从后端API获取
const initOrders = async () => {
  try {
    const response = await fetch('/api/orders')
    const result = await response.json()
    
    if (result.status === 'success') {
      orders.value = result.data.list
      console.log('订单数据已从后端加载，共', result.data.list.length, '条')
    } else {
      console.error('获取订单数据失败:', result.message)
      orders.value = []
    }
  } catch (error) {
    console.error('获取订单数据失败:', error)
    orders.value = []
  }
}

// 刷新订单数据
const refreshOrders = async () => {
  try {
    const response = await fetch('/api/orders')
    const result = await response.json()
    
    if (result.status === 'success') {
      const newOrders = result.data.list
      
      const hasChanges = JSON.stringify(newOrders) !== JSON.stringify(orders.value)
      
      if (hasChanges) {
        orders.value = newOrders
        imageCacheBuster.value = Date.now()
        console.log('订单数据已从后端更新，共', newOrders.length, '条')
      }
    } else {
      console.error('获取订单数据失败:', result.message)
      orders.value = []
    }
  } catch (error) {
    console.error('刷新订单数据失败:', error)
    orders.value = []
  }
}

// 启动轮询
const startPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
  pollTimer = setInterval(refreshOrders, POLL_INTERVAL)
  console.log('订单数据轮询已启动，间隔:', POLL_INTERVAL / 1000, '秒')
}

// 停止轮询
const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
    console.log('订单数据轮询已停止')
  }
}

// 获取带缓存破坏的图片 URL
const getImageUrl = (order) => {
  if (!order.image) {
    console.warn('订单没有图片:', order)
    return ''
  }
  
  try {
    const url = new URL(order.image)
    url.searchParams.set('_cb', imageCacheBuster.value)
    return url.toString()
  } catch (error) {
    console.error('图片 URL 无效:', order.image, error)
    return order.image
  }
}

// 获取二维码图片 URL
const getQrcodeUrl = (qrcode) => {
  if (!qrcode) {
    return ''
  }
  
  try {
    // 如果已经是完整URL，直接返回
    if (qrcode.startsWith('http://') || qrcode.startsWith('https://')) {
      return qrcode
    }
    
    // 如果是相对路径，添加基础URL
    if (qrcode.startsWith('/uploads/')) {
      return `http://localhost:5001${qrcode}`
    }
    
    // 如果是base64图片，直接返回
    if (qrcode.startsWith('data:')) {
      return qrcode
    }
    
    // 其他情况，尝试添加基础URL
    return `http://localhost:5001${qrcode.startsWith('/') ? '' : '/'}${qrcode}`
  } catch (error) {
    console.error('二维码 URL 处理失败:', error)
    return qrcode
  }
}

// 处理二维码图片加载失败
const handleQrcodeError = (e) => {
  console.warn('二维码图片加载失败')
  // 隐藏图片或显示占位符
  e.target.style.display = 'none'
  e.target.parentElement.classList.add('qrcode-error')
}

// 组件挂载时初始化
onMounted(async () => {
  await initOrders()
  startPolling()
})

// 组件卸载时清理
onUnmounted(() => {
  stopPolling()
})

// 监听 activeTab 变化，确保数据最新
watch(activeTab, () => {
  refreshOrders()
})

// 处理图片加载失败
const handleImageError = (e, order) => {
  console.warn('图片加载失败:', order.image)
  // 使用占位图片，避免无限循环
  if (e.target.src !== '/placeholder.png') {
    e.target.src = '/placeholder.png'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待开始',
    'recruiting': '招募中',
    'ended': '已结束'
  }
  return statusMap[status] || status
}

// 根据选中标签筛选订单
const filteredOrders = computed(() => {
  if (activeTab.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === activeTab.value)
})

// 切换标签
const handleTabChange = (tab) => {
  activeTab.value = tab
}

// 查看订单详情 - 用户端只显示联系信息
const viewOrderDetail = (order) => {
  console.log('查看订单详情:', order)
  selectedOrder.value = order
  showContactModal.value = true
}

// 发布商单弹窗
const showPublishModal = ref(false)

// 文件上传相关
const scriptFileList = ref([])
const coverFileList = ref([])
const qrcodeFileList = ref([])
const uploadedCoverUrl = ref('')
const uploadedQrcodeUrl = ref('')

// 处理剧本上传
const handleScriptUpload = (file) => {
  console.log('剧本文件:', file)
  scriptFileList.value = [file]
}

// 处理封面上传
const handleCoverUpload = (file) => {
  console.log('封面文件:', file)
  coverFileList.value = [file]
  
  // 读取文件并转换为 URL
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedCoverUrl.value = e.target.result
    console.log('封面已读取:', uploadedCoverUrl.value)
  }
  reader.readAsDataURL(file.raw)
}

// 移除封面
const removeCover = () => {
  uploadedCoverUrl.value = ''
  coverFileList.value = []
}

// 处理二维码上传
const handleQrcodeUpload = (file) => {
  console.log('二维码文件:', file)
  qrcodeFileList.value = [file]
  
  // 读取文件并转换为 URL
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedQrcodeUrl.value = e.target.result
    console.log('二维码已读取:', uploadedQrcodeUrl.value)
  }
  reader.readAsDataURL(file.raw)
}

// 联系弹窗
const showContactModal = ref(false)
const selectedOrder = ref(null)

// 发布商单表单数据
const publishForm = ref({
  title: '',
  type: '都市',
  minProfit: 0,
  shareRatio: 0,
  powerSubsidy: 0,
  startTime: '',
  endTime: '',
  period: 0,
  auditionScript: '',
  description: '',
  contactInfo: '',
  participation: 'all',
  copyright: true
})

// 提交审核
const handleSubmit = async () => {
  console.log('提交审核:', publishForm.value)
  
  if (!publishForm.value.title) {
    alert('请输入商单标题')
    return
  }
  
  if (!uploadedCoverUrl.value) {
    alert('请上传封面图片')
    return
  }
  
  const newOrder = {
    invite_code: inviteCode.value,
    title: publishForm.value.title,
    image: uploadedCoverUrl.value,
    qrcode: uploadedQrcodeUrl.value || `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=weixin://wxid_${Date.now()}`,
    price: publishForm.value.minProfit ? `¥${publishForm.value.minProfit}` : '¥0',
    deadline: publishForm.value.endTime ? new Date(publishForm.value.endTime).toLocaleDateString() : '待定',
    status: 'recruiting',
    tags: [publishForm.value.type || '其他'],
    description: publishForm.value.description || '',
    contact_info: publishForm.value.contactInfo || '',
    min_profit: publishForm.value.minProfit || 0,
    share_ratio: publishForm.value.shareRatio || 0,
    power_subsidy: publishForm.value.powerSubsidy || 0,
    period: publishForm.value.period || 0
  }
  
  try {
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newOrder)
    })
    
    const result = await response.json()
    
    if (result.status === 'success') {
      newOrder.id = result.order_id
      
      const existingOrders = JSON.parse(localStorage.getItem('admin_orders') || '[]')
      existingOrders.unshift(newOrder)
      localStorage.setItem('admin_orders', JSON.stringify(existingOrders))
      
      console.log('订单已创建并保存到后端:', newOrder)
      refreshOrders()
      
      publishForm.value = {
        title: '',
        type: '都市',
        minProfit: 0,
        shareRatio: 0,
        powerSubsidy: 0,
        startTime: '',
        endTime: '',
        period: 0,
        auditionScript: '',
        description: '',
        contactInfo: '',
        participation: 'all',
        copyright: true
      }
      
      scriptFileList.value = []
      coverFileList.value = []
      qrcodeFileList.value = []
      uploadedCoverUrl.value = ''
      uploadedQrcodeUrl.value = ''
      
      showPublishModal.value = false
      
      alert('商单发布成功！')
    } else {
      alert('发布失败: ' + (result.message || '未知错误'))
    }
  } catch (error) {
    console.error('订单创建失败:', error)
    alert('订单创建失败，请重试')
  }
}

// 处理联系按钮点击
const handleContact = (order) => {
  selectedOrder.value = order
  showContactModal.value = true
}
</script>

<style scoped>
.order-container {
  padding: 24px;
  min-height: 100%;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #425D5F;
  margin: 0;
}

.publish-btn {
  background-color: #425D5F;
  color: #F8F7F2;
  border: none;
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.publish-btn:hover {
  background-color: #FAA943;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(250, 169, 67, 0.3);
}

/* 标签筛选 */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #333;
}

.tab-item {
  padding: 8px 20px;
  font-size: 14px;
  color: #999;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  background-color: transparent;
}

.tab-item:hover {
  color: #425D5F;
  background-color: rgba(250, 169, 67, 0.1);
}

.tab-item.active {
  color: #F8F7F2;
  background-color: #425D5F;
  font-weight: 500;
}

/* 内容区域 */
.content-area {
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #425D5F;
}

.empty-icon {
  margin-bottom: 16px;
  color: #425D5F;
}

.empty-text {
  font-size: 14px;
  color: #425D5F;
  margin: 0;
}

/* 订单网格 */
.order-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* 订单卡片 */
.order-card {
  background-color: #BACACB;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.order-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.order-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.order-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.order-card:hover .order-image img {
  transform: scale(1.05);
}

.order-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  font-size: 12px;
  border-radius: 4px;
  font-weight: 500;
}

.order-status.recruiting {
  background-color: #425D5F;
  color: #F8F7F2;
}

.order-status.pending {
  background-color: #FDE7A2;
  color: #425D5F;
}

.order-status.ended {
  background-color: #BACACB;
  color: #425D5F;
}

.order-info {
  padding: 16px;
}

.order-title {
  font-size: 16px;
  font-weight: 600;
  color: #425D5F;
  margin: 0 0 12px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.order-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #425D5F;
}

.meta-item svg {
  color: #425D5F;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.order-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  background-color: rgba(250, 169, 67, 0.15);
  color: #425D5F;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 4px;
}

.contact-btn {
  background-color: rgba(250, 169, 67, 0.15);
  color: #425D5F;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.contact-btn:hover {
  background-color: #425D5F;
  color: #F8F7F2;
}

/* 上传组件样式 */
.cover-upload :deep(.el-upload-list__item) {
  margin-top: 10px;
  border: 1px solid #425D5F;
  border-radius: 4px;
  padding: 8px;
  transition: all 0.3s ease;
}

.cover-upload :deep(.el-upload-list__item:hover) {
  border-color: #FAA943;
}

.cover-upload :deep(.el-upload-list__item-thumbnail) {
  object-fit: cover;
  border-radius: 4px;
}

.script-upload :deep(.el-upload-list) {
  margin-top: 10px;
}

.qrcode-upload :deep(.el-upload-list) {
  margin-top: 10px;
}

.el-upload__tip {
  color: #666;
  font-size: 12px;
  margin-top: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .order-container {
    padding: 16px;
  }

  .page-title {
    font-size: 20px;
  }

  .filter-tabs {
    gap: 6px;
  }

  .tab-item {
    padding: 6px 14px;
    font-size: 13px;
  }

  .order-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .order-grid {
    grid-template-columns: 1fr;
  }
}

/* 发布商单弹窗样式 */
.publish-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 4px !important;
  --el-dialog-title-color: #425D5F !important;
}

.publish-dialog .el-dialog__header {
  border-bottom: 1px solid #BACACB;
  padding: 16px 20px;
}

.publish-dialog .el-dialog__title {
  color: #425D5F;
  font-size: 16px;
  font-weight: 600;
}

.publish-dialog .el-dialog__body {
  padding: 20px;
  max-height: 80vh;
  overflow-y: auto;
  background-color: #F8F7F2;
}

.publish-dialog .el-dialog__footer {
  border-top: 1px solid #BACACB;
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background-color: #F8F7F2;
}

/* 强制覆盖Element Plus对话框背景色 */
.publish-dialog .el-dialog {
  background-color: #F8F7F2 !important;
  border-radius: 4px !important;
  overflow: hidden;
}

/* 强制覆盖对话框内容区域背景色 */
.publish-dialog .el-dialog .el-dialog__body {
  background-color: #F8F7F2 !important;
}

.publish-dialog .el-dialog .el-dialog__header {
  background-color: #F8F7F2 !important;
}

.publish-dialog .el-dialog .el-dialog__footer {
  background-color: #F8F7F2 !important;
}

/* 更高特异性的选择器 */
.el-overlay .el-overlay-dialog .publish-dialog .el-dialog {
  background-color: #F8F7F2 !important;
}

/* 针对Element Plus的特定结构 */
[data-id*="publish-dialog"] .el-dialog,
.el-dialog[data-view="publish-dialog"],
.publish-dialog[data-view] .el-dialog {
  background-color: #F8F7F2 !important;
}

/* 警告框 */
.warning-box {
  background-color: rgba(250, 169, 67, 0.2);
  border: 1px solid #FAA943;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.warning-box .el-icon {
  color: #FAA943;
  margin-top: 2px;
  font-size: 16px;
}

.warning-text {
  flex: 1;
}

.warning-text p {
  margin: 0 0 4px 0;
  color: #FAA943;
  font-size: 14px;
  line-height: 1.4;
}

.warning-text p:last-child {
  margin-bottom: 0;
}

/* 表单行 */
.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.form-row .el-form-item {
  flex: 1;
  margin-bottom: 0;
}

/* 表单标签 */
.publish-dialog .el-form-item__label {
  color: #425D5F;
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 8px;
  padding: 0;
}

/* 表单输入框 */
.publish-dialog .el-input__wrapper {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 4px;
  padding: 10px 12px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.publish-dialog .el-input__wrapper:hover {
  border-color: #425D5F;
  box-shadow: none;
}

.publish-dialog .el-input__wrapper.is-focus {
  border-color: #425D5F;
  box-shadow: 0 0 0 1px rgba(66, 93, 95, 0.2);
}

.publish-dialog .el-input__inner {
  color: #425D5F;
  font-size: 14px;
}

.publish-dialog .el-input__inner::placeholder {
  color: #425D5F;
}

/* 选择器 */
.publish-dialog .el-select__wrapper {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 4px;
  padding: 10px 12px;
  box-shadow: none;
}

.publish-dialog .el-select__wrapper:hover {
  border-color: #425D5F;
  box-shadow: none;
}

.publish-dialog .el-select__wrapper.is-focused {
  border-color: #425D5F;
  box-shadow: 0 0 0 1px rgba(66, 93, 95, 0.2);
}

.publish-dialog .el-select__placeholder {
  color: #425D5F;
  font-size: 14px;
}

.publish-dialog .el-select__caret {
  color: #425D5F;
}

.publish-dialog .el-select__selected-item {
  color: #425D5F;
}

/* 日期选择器 */
.publish-dialog .el-date-editor {
  --el-date-editor-width: 100%;
}

.publish-dialog .el-date-editor .el-input__wrapper {
  width: 100%;
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 4px;
  padding: 10px 12px;
}

.publish-dialog .el-date-editor .el-input__inner {
  color: #425D5F;
}

.publish-dialog .el-date-editor .el-input__prefix {
  color: #425D5F;
}

/* 文本域 */
.publish-dialog .el-textarea__inner {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 4px;
  padding: 10px 12px;
  color: #425D5F;
  font-size: 14px;
  resize: none;
  transition: all 0.3s ease;
  min-height: 80px;
}

.publish-dialog .el-textarea__inner:hover {
  border-color: #425D5F;
}

.publish-dialog .el-textarea__inner:focus {
  border-color: #425D5F;
  box-shadow: 0 0 0 1px rgba(66, 93, 95, 0.2);
}

.publish-dialog .el-textarea__inner::placeholder {
  color: #425D5F;
}

/* 上传区域 */
.upload-area {
  border: 1px dashed #BACACB;
  border-radius: 4px;
  padding: 24px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #F8F7F2;
}

.upload-area:hover {
  border-color: #425D5F;
  background-color: rgba(66, 93, 95, 0.05);
}

.upload-icon {
  font-size: 28px;
  color: #425D5F;
  margin-bottom: 10px;
}

.upload-text p {
  margin: 0;
  color: #425D5F;
  font-size: 14px;
}

.upload-text p:last-child {
  font-size: 12px;
  color: #425D5F;
  margin-top: 4px;
}

.cover-upload {
  border-style: dotted;
}

.cover-upload-container {
  width: 100%;
}

.cover-upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  cursor: pointer;
}

.cover-upload-trigger:hover .el-button {
  background-color: #425D5F;
  border-color: #425D5F;
}

.cover-upload-hint {
  font-size: 12px;
  color: #999;
}

.cover-preview {
  position: relative;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.cover-preview-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}

.cover-preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 8px;
}

.cover-preview:hover .cover-preview-overlay {
  opacity: 1;
}

/* 参与条件 */
.participation-options {
  display: flex;
  gap: 12px;
}

.participation-options .el-button {
  flex: 1;
  border: 1px solid #BACACB;
  background-color: #F8F7F2;
  color: #425D5F;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.participation-options .el-button:hover {
  border-color: #425D5F;
  color: #425D5F;
}

.participation-options .el-button.active {
  border-color: #66b1ff;
  background-color: rgba(102, 177, 255, 0.1);
  color: #66b1ff;
}

.check-icon {
  font-size: 14px;
}

/* 复选框 */
.publish-dialog .el-checkbox__label {
  color: #e5e5e5;
  font-size: 14px;
}

/* 弹窗底部按钮 */
.publish-dialog .dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.publish-dialog .dialog-footer .el-button {
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.publish-dialog .dialog-footer .el-button:not(.submit-btn) {
  background-color: #BACACB;
  border: 1px solid #BACACB;
  color: #425D5F;
}

.publish-dialog .dialog-footer .el-button:not(.submit-btn):hover {
  background-color: #425D5F;
  border-color: #425D5F;
}

.publish-dialog .dialog-footer .submit-btn {
  background-color: #425D5F;
  border: 1px solid #425D5F;
  color: #F8F7F2;
  font-weight: 500;
}

.publish-dialog .dialog-footer .submit-btn:hover {
  background-color: #FAA943;
  border-color: #FAA943;
  box-shadow: 0 2px 4px rgba(250, 169, 67, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .participation-options {
    flex-direction: column;
  }
}

/* 联系弹窗样式 */
.contact-dialog {
  --el-dialog-bg-color: #F8F7F2;
  --el-dialog-header-color: #425D5F;
  --el-dialog-border-color: #BACACB;
}

.contact-dialog .el-dialog__header {
  border-bottom: 1px solid #BACACB;
  padding: 16px 20px;
}

.contact-dialog .el-dialog__title {
  color: #425D5F;
  font-size: 18px;
  font-weight: 600;
}

.contact-dialog .el-dialog__body {
  padding: 30px;
  text-align: center;
  background-color: #F8F7F2;
}

.contact-dialog .el-dialog__footer {
  border-top: 1px solid #BACACB;
  padding: 16px 20px;
  background-color: #F8F7F2;
}

/* 联系内容区域 */
.contact-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.qrcode-wrapper {
  width: 220px;
  height: 220px;
  padding: 12px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f7f2 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(66, 93, 95, 0.15);
  border: 2px solid #BACACB;
  transition: all 0.3s ease;
}

.qrcode-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(66, 93, 95, 0.2);
}

.qrcode-wrapper.qrcode-error {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #BACACB 0%, #F8F7F2 100%);
}

.qrcode-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.contact-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.contact-info .order-title {
  font-size: 18px;
  font-weight: 600;
  color: #425D5F;
  margin: 0;
}

.contact-info .contact-tip {
  color: #425D5F;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

.contact-info .contact-note {
  color: #666;
  font-size: 13px;
  margin: 0;
  padding: 8px 16px;
  background-color: rgba(250, 169, 67, 0.1);
  border-radius: 8px;
  border-left: 3px solid #FAA943;
}

.contact-empty {
  padding: 40px 20px;
}

.contact-empty .el-empty {
  padding: 20px;
}

/* 弹窗底部按钮 */
.contact-dialog .dialog-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.contact-dialog .dialog-footer .el-button {
  padding: 10px 30px;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.contact-dialog .dialog-footer .el-button:not(.is-link) {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
}

.contact-dialog .dialog-footer .el-button:not(.is-link):hover {
  background-color: #FAA943;
  border-color: #FAA943;
  box-shadow: 0 2px 8px rgba(250, 169, 67, 0.3);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .qrcode-wrapper {
    width: 180px;
    height: 180px;
    padding: 10px;
  }
  
  .contact-info .order-title {
    font-size: 16px;
  }
  
  .contact-info .contact-tip {
    font-size: 14px;
  }
  
  .contact-info .contact-note {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
