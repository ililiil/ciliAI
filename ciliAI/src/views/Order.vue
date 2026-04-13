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
            <img :src="order.image" :alt="order.title">
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
    width="400px"
    class="contact-dialog"
  >
    <div class="contact-qrcode" v-if="selectedOrder">
      <div class="qrcode-container">
        <img :src="selectedOrder.qrcode" alt="企业微信二维码" class="qrcode-image">
      </div>
      <p class="contact-tip">请扫描上方二维码添加企业微信</p>
    </div>
    <div v-else class="contact-empty">
      <p>暂无联系方式</p>
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
        <div class="upload-area">
          <el-icon class="upload-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg></el-icon>
          <div class="upload-text">
            <p>点击上传剧本文件</p>
            <p>支持 PDF、DOC、DOCX 格式</p>
          </div>
        </div>
      </el-form-item>

      <!-- 封面上传 -->
      <el-form-item label="封面上传">
        <div class="upload-area cover-upload">
          <el-icon class="upload-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg></el-icon>
          <div class="upload-text">
            <p>点击上传封面文件</p>
            <p>支持 JPG、PNG 格式</p>
          </div>
        </div>
      </el-form-item>

      <!-- 联系方式 -->
      <el-form-item label="联系方式">
        <div class="upload-area">
          <el-icon class="upload-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg></el-icon>
          <div class="upload-text">
            <p>点击上传企业微信二维码</p>
            <p>支持 JPG、PNG 格式</p>
          </div>
        </div>
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
import { ref, computed } from 'vue'

// 标签选项
const tabs = [
  { label: '全部', value: 'all' },
  { label: '待开始', value: 'pending' },
  { label: '招募中', value: 'recruiting' },
  { label: '已结束', value: 'ended' }
]

const activeTab = ref('all')

// 订单数据 - 从 localStorage 读取以与管理后台同步
const orders = ref([])
const initialOrders = [
  {
    id: 1,
    title: '现代都市情感短剧制作',
    image: 'https://img2.baidu.com/it/u=3152765891,1290125229&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=892',
    qrcode: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=weixin://wxid_example1',
    price: '¥5000',
    deadline: '2024-12-31',
    status: 'recruiting',
    tags: ['AI真人', '现代都市'],
    contactCount: 5
  },
  {
    id: 2,
    title: '古装历史短剧制作',
    image: 'https://img2.baidu.com/it/u=3152765891,1290125229&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=892',
    qrcode: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=weixin://wxid_example2',
    price: '¥8000',
    deadline: '2025-01-15',
    status: 'pending',
    tags: ['AI真人', '古装历史'],
    contactCount: 3
  },
  {
    id: 3,
    title: '科幻题材短剧制作',
    image: 'https://img2.baidu.com/it/u=3152765891,1290125229&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=892',
    qrcode: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=weixin://wxid_example3',
    price: '¥6000',
    deadline: '2025-01-10',
    status: 'ended',
    tags: ['AI动画', '科幻题材'],
    contactCount: 8
  }
]

// 初始化订单数据
const initOrders = () => {
  const storedOrders = localStorage.getItem('admin_orders')
  if (storedOrders) {
    orders.value = JSON.parse(storedOrders)
  } else {
    orders.value = initialOrders
    localStorage.setItem('admin_orders', JSON.stringify(initialOrders))
  }
}

// 在组件挂载时初始化
initOrders()

// 根据选中标签筛选订单
const filteredOrders = computed(() => {
  if (activeTab.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === activeTab.value)
})

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待开始',
    'recruiting': '招募中',
    'ended': '已结束'
  }
  return statusMap[status] || status
}

// 切换标签
const handleTabChange = (tab) => {
  activeTab.value = tab
}

// 查看订单详情
const viewOrderDetail = (order) => {
  console.log('查看订单详情:', order)
}

// 发布商单弹窗
const showPublishModal = ref(false)

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
const handleSubmit = () => {
  console.log('提交审核:', publishForm.value)
  // 这里处理提交逻辑
  showPublishModal.value = false
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
}

.contact-dialog .el-dialog__title {
  color: #425D5F;
  font-size: 18px;
  font-weight: 600;
}

.contact-dialog .el-dialog__body {
  padding: 30px;
  text-align: center;
}

.contact-dialog .el-dialog__footer {
  border-top: 1px solid #BACACB;
  padding-top: 20px;
}

/* 二维码样式 */
.contact-qrcode {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qrcode-container {
  width: 200px;
  height: 200px;
  margin-bottom: 20px;
  background-color: #F8F7F2;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.qrcode-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.contact-tip {
  color: #e5e5e5;
  font-size: 14px;
  margin: 0;
}

.contact-empty {
  padding: 40px 0;
  color: #999;
  font-size: 14px;
}
</style>
