<template>
  <div class="project-manager">
    <div class="pm-header">
      <h2 class="pm-title">我的项目</h2>
      <el-button type="primary" @click="showCreateDialog = true" :icon="Plus">
        新建项目
      </el-button>
    </div>

    <div class="pm-stats" v-if="isLoggedIn">
      <div class="stat-card">
        <div class="stat-icon power-icon">⚡</div>
        <div class="stat-info">
          <div class="stat-value">{{ userInfo.compute_power || 0 }}</div>
          <div class="stat-label">当前算力</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon project-icon">📁</div>
        <div class="stat-info">
          <div class="stat-value">{{ userInfo.project_count || 0 }}</div>
          <div class="stat-label">项目总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon image-icon">🖼️</div>
        <div class="stat-info">
          <div class="stat-value">{{ userInfo.image_count || 0 }}</div>
          <div class="stat-label">生成图片</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon used-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ userInfo.total_power_used || 0 }}</div>
          <div class="stat-label">累计消耗</div>
        </div>
      </div>
    </div>

    <div class="pm-projects" v-loading="loading">
      <div v-if="!isLoggedIn" class="pm-login-tip">
        <p>请先登录以查看您的项目</p>
      </div>
      <div v-else-if="projects.length === 0" class="pm-empty">
        <p>暂无项目，点击上方按钮创建您的第一个项目</p>
      </div>
      <div v-else class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card" @click="openProject(project)">
          <div class="project-cover">
            <img v-if="project.cover_image" :src="project.cover_image" alt="cover">
            <div v-else class="project-cover-placeholder">
              <span>📁</span>
            </div>
          </div>
          <div class="project-info">
            <h3 class="project-title">{{ project.title }}</h3>
            <p class="project-desc">{{ project.description || '暂无描述' }}</p>
            <div class="project-meta">
              <span class="meta-item">
                <el-icon><Picture /></el-icon>
                {{ project.image_count || 0 }} 张图片
              </span>
              <span class="meta-item">
                <el-icon><ChatDotRound /></el-icon>
                {{ project.chat_count || 0 }} 条对话
              </span>
            </div>
            <div class="project-footer">
              <span class="project-time">{{ formatDate(project.create_time) }}</span>
              <div class="project-actions">
                <el-button size="small" text @click.stop="editProject(project)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" text type="danger" @click.stop="deleteProject(project)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog v-model="showCreateDialog" :title="editingProject ? '编辑项目' : '新建项目'" width="600px">
      <el-form :model="projectForm" label-width="80px">
        <el-form-item label="项目封面">
          <div class="cover-upload-wrapper">
            <el-upload
              class="cover-uploader"
              action="#"
              :auto-upload="false"
              :on-change="handleCoverUpload"
              :file-list="coverFileList"
              :show-file-list="false"
              accept="image/*"
              list-type="picture"
            >
              <template #default>
                <div class="cover-upload-trigger" v-if="!projectForm.cover_image">
                  <el-button type="primary" size="large">
                    <el-icon><Plus /></el-icon>
                    上传封面
                  </el-button>
                  <div class="cover-upload-hint">支持 JPG、PNG 格式，建议尺寸 500x892</div>
                </div>
                <div class="cover-preview" v-else>
                  <img :src="projectForm.cover_image" alt="封面预览" class="cover-preview-image">
                  <div class="cover-preview-overlay">
                    <el-button type="danger" size="small" @click.stop="removeCover">移除</el-button>
                  </div>
                </div>
              </template>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="项目名称" required>
          <el-input v-model="projectForm.title" placeholder="请输入项目名称" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="项目描述">
          <el-input v-model="projectForm.description" type="textarea" :rows="3" placeholder="请输入项目描述（可选）" maxlength="200" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProject" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showProjectDialog" :title="currentProject?.title" width="90%" top="5vh" class="project-detail-dialog">
      <div class="project-detail" v-if="currentProject">
        <el-tabs v-model="detailTab">
          <el-tab-pane label="生成记录" name="records">
            <div class="records-list" v-loading="recordsLoading">
              <div v-if="generationRecords.length === 0" class="empty-tip">
                暂无生成记录
              </div>
              <div v-else class="records-grid">
                <div v-for="record in generationRecords" :key="record.id" class="record-card">
                  <div class="record-image" v-if="record.image_url">
                    <img :src="record.image_url.startsWith('data:') ? record.image_url : `data:image/png;base64,${record.image_url}`" alt="generated">
                  </div>
                  <div class="record-info">
                    <div class="record-type">
                      <el-tag size="small" :type="getRecordTypeTag(record.type)">{{ getRecordTypeLabel(record.type) }}</el-tag>
                    </div>
                    <div class="record-prompt" v-if="record.prompt">{{ record.prompt }}</div>
                    <div class="record-meta">
                      <span>消耗: {{ record.power_cost }} 算力</span>
                      <span>{{ formatDate(record.create_time) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="对话历史" name="chat">
            <div class="chat-list" v-loading="chatLoading">
              <div v-if="chatMessages.length === 0" class="empty-tip">
                暂无对话记录
              </div>
              <div v-else class="chat-messages">
                <div v-for="msg in chatMessages" :key="msg.id" :class="['chat-message', msg.role]">
                  <div class="message-avatar">{{ msg.role === 'user' ? '我' : 'AI' }}</div>
                  <div class="message-content">
                    <div class="message-text">{{ msg.content }}</div>
                    <div class="message-time">{{ formatDate(msg.create_time) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="算力明细" name="power">
            <div class="power-logs" v-loading="powerLogsLoading">
              <div v-if="powerLogs.length === 0" class="empty-tip">
                暂无算力记录
              </div>
              <el-table v-else :data="powerLogs" stripe>
                <el-table-column prop="operation_type" label="操作类型" width="120">
                  <template #default="{ row }">
                    {{ getOperationLabel(row.operation_type) }}
                  </template>
                </el-table-column>
                <el-table-column prop="power_change" label="算力变化" width="120">
                  <template #default="{ row }">
                    <span :class="row.power_change > 0 ? 'power-add' : 'power-minus'">
                      {{ row.power_change > 0 ? '+' : '' }}{{ row.power_change }}
                    </span>
                  </template>
                </el-table-column>
                <el-table-column prop="description" label="描述" />
                <el-table-column prop="created_at" label="时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.created_at) }}
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Picture, ChatDotRound } from '@element-plus/icons-vue'

const props = defineProps({
  inviteCode: {
    type: String,
    default: ''
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['updatePower'])

const loading = ref(false)
const saving = ref(false)
const recordsLoading = ref(false)
const chatLoading = ref(false)
const powerLogsLoading = ref(false)

const projects = ref([])
const userInfo = ref({})
const generationRecords = ref([])
const chatMessages = ref([])
const powerLogs = ref([])

const showCreateDialog = ref(false)
const showProjectDialog = ref(false)
const editingProject = ref(null)
const currentProject = ref(null)
const detailTab = ref('records')

const projectForm = ref({
  title: '',
  description: '',
  cover_image: '',
  cover_file: null
})

const coverFileList = ref([])

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getRecordTypeLabel = (type) => {
  const labels = {
    generate: '文生图',
    extend: '扩图',
    super_resolution: '超清',
    inpaint: '编辑'
  }
  return labels[type] || type
}

const getRecordTypeTag = (type) => {
  const tags = {
    generate: 'success',
    extend: 'warning',
    super_resolution: 'primary',
    inpaint: 'info'
  }
  return tags[type] || ''
}

const getOperationLabel = (type) => {
  const labels = {
    generate: '文生图',
    extend: '扩图',
    super_resolution: '超清',
    inpaint: '编辑',
    chat: '对话',
    init: '初始化',
    refund: '退还',
    recharge: '充值'
  }
  return labels[type] || type
}

const fetchUserInfo = async () => {
  if (!props.inviteCode) return
  
  try {
    const response = await fetch(`/api/user/info?invite_code=${encodeURIComponent(props.inviteCode)}`)
    const result = await response.json()
    if (result.status === 'success') {
      userInfo.value = result.data
      emit('updatePower', result.data.compute_power)
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
}

const fetchProjects = async () => {
  if (!props.inviteCode) {
    projects.value = []
    return
  }
  
  loading.value = true
  try {
    const response = await fetch(`/api/projects?invite_code=${encodeURIComponent(props.inviteCode)}`)
    const result = await response.json()
    if (result.status === 'success') {
      projects.value = result.projects
    }
  } catch (error) {
    console.error('Failed to fetch projects:', error)
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

const saveProject = async () => {
  if (!projectForm.value.title.trim()) {
    ElMessage.warning('请输入项目名称')
    return
  }
  
  saving.value = true
  try {
    const url = editingProject.value 
      ? `/api/projects/${editingProject.value.id}`
      : '/api/projects'
    const method = editingProject.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...projectForm.value,
        invite_code: props.inviteCode
      })
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      ElMessage.success(editingProject.value ? '项目已更新' : '项目创建成功')
      showCreateDialog.value = false
      fetchProjects()
      fetchUserInfo()
      resetForm()
    } else {
      ElMessage.error(result.message || '操作失败')
    }
  } catch (error) {
    console.error('Failed to save project:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const editProject = (project) => {
  editingProject.value = project
  projectForm.value = {
    title: project.title,
    description: project.description || '',
    cover_image: project.cover_image || '',
    cover_file: null
  }
  coverFileList.value = project.cover_image ? [{ name: 'cover.jpg', url: project.cover_image }] : []
  showCreateDialog.value = true
}

const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm('确定要删除此项目吗？删除后无法恢复。', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/projects/${project.id}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      ElMessage.success('项目已删除')
      fetchProjects()
      fetchUserInfo()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete project:', error)
      ElMessage.error('删除失败')
    }
  }
}

const openProject = async (project) => {
  currentProject.value = project
  detailTab.value = 'records'
  showProjectDialog.value = true
  
  await Promise.all([
    fetchGenerationRecords(project.id),
    fetchChatMessages(project.id),
    fetchPowerLogs()
  ])
}

const fetchGenerationRecords = async (projectId) => {
  recordsLoading.value = true
  try {
    const response = await fetch(`/api/records?invite_code=${encodeURIComponent(props.inviteCode)}&project_id=${projectId}`)
    const result = await response.json()
    if (result.status === 'success') {
      generationRecords.value = result.records
    }
  } catch (error) {
    console.error('Failed to fetch records:', error)
  } finally {
    recordsLoading.value = false
  }
}

const fetchChatMessages = async (projectId) => {
  chatLoading.value = true
  try {
    const response = await fetch(`/api/chat/messages?invite_code=${encodeURIComponent(props.inviteCode)}&project_id=${projectId}`)
    const result = await response.json()
    if (result.status === 'success') {
      chatMessages.value = result.messages
    }
  } catch (error) {
    console.error('Failed to fetch chat messages:', error)
  } finally {
    chatLoading.value = false
  }
}

const fetchPowerLogs = async () => {
  powerLogsLoading.value = true
  try {
    const response = await fetch(`/api/user/power-logs?invite_code=${encodeURIComponent(props.inviteCode)}&page_size=50`)
    const result = await response.json()
    if (result.status === 'success') {
      powerLogs.value = result.data.list
    }
  } catch (error) {
    console.error('Failed to fetch power logs:', error)
  } finally {
    powerLogsLoading.value = false
  }
}

const resetForm = () => {
  editingProject.value = null
  projectForm.value = {
    title: '',
    description: '',
    cover_image: '',
    cover_file: null
  }
  coverFileList.value = []
}

const handleCoverUpload = (file) => {
  console.log('封面文件:', file)
  coverFileList.value = [file]
  
  const reader = new FileReader()
  reader.onload = (e) => {
    projectForm.value.cover_image = e.target.result
    projectForm.value.cover_file = file.raw
    console.log('封面已读取:', projectForm.value.cover_image)
  }
  reader.readAsDataURL(file.raw)
}

const removeCover = () => {
  projectForm.value.cover_image = ''
  projectForm.value.cover_file = null
  coverFileList.value = []
}

watch(() => props.inviteCode, (newVal) => {
  if (newVal && props.isLoggedIn) {
    fetchUserInfo()
    fetchProjects()
  }
}, { immediate: true })

watch(showCreateDialog, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})

defineExpose({
  fetchUserInfo,
  fetchProjects
})
</script>

<style scoped>
.project-manager {
  padding: 20px;
}

.pm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.pm-title {
  font-size: 24px;
  font-weight: 600;
  color: #425D5F;
  margin: 0;
}

.pm-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: linear-gradient(135deg, #BACACB 0%, #F8F7F2 100%);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #333;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.power-icon {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.project-icon {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
}

.image-icon {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
}

.used-icon {
  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #425D5F;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #425D5F;
  margin-top: 4px;
}

.pm-projects {
  min-height: 200px;
}

.pm-login-tip,
.pm-empty {
  text-align: center;
  padding: 60px 20px;
  color: #888;
  font-size: 16px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.project-card {
  background: #232323;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #333;
}

.project-card:hover {
  transform: translateY(-4px);
  border-color: #425D5F;
  box-shadow: 0 8px 24px rgba(163, 230, 53, 0.15);
}

.project-cover {
  height: 160px;
  background: #F8F7F2;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-cover-placeholder {
  font-size: 48px;
  opacity: 0.5;
}

.project-info {
  padding: 16px;
}

.project-title {
  font-size: 16px;
  font-weight: 600;
  color: #425D5F;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.project-desc {
  font-size: 14px;
  color: #888;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
}

.project-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #888;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #333;
}

.project-time {
  font-size: 12px;
  color: #666;
}

.project-actions {
  display: flex;
  gap: 4px;
}

.project-detail-dialog :deep(.el-dialog__body) {
  max-height: 70vh;
  overflow-y: auto;
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #888;
}

.records-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.record-card {
  background: #F8F7F2;
  border-radius: 8px;
  overflow: hidden;
}

.record-image {
  height: 200px;
  background: #232323;
  display: flex;
  align-items: center;
  justify-content: center;
}

.record-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.record-info {
  padding: 12px;
}

.record-type {
  margin-bottom: 8px;
}

.record-prompt {
  font-size: 13px;
  color: #ccc;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.record-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 500px;
  overflow-y: auto;
  padding: 16px;
}

.chat-message {
  display: flex;
  gap: 12px;
}

.chat-message.assistant {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #425D5F;
  color: #F8F7F2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.chat-message.assistant .message-avatar {
  background: #425D5F;
  color: #F8F7F2;
}

.message-content {
  max-width: 70%;
}

.message-text {
  background: #BACACB;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  color: #425D5F;
  line-height: 1.5;
}

.chat-message.assistant .message-text {
  background: #BACACB;
}

.message-time {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
  text-align: right;
}

.power-add {
  color: #34d399;
  font-weight: 600;
}

.power-minus {
  color: #f87171;
  font-weight: 600;
}

@media (max-width: 768px) {
  .pm-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
}

.cover-upload-wrapper {
  width: 100%;
}

.cover-uploader {
  width: 100%;
}

.cover-upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  cursor: pointer;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  transition: all 0.3s;
}

.cover-upload-trigger:hover {
  border-color: #425D5F;
  background-color: rgba(66, 93, 95, 0.05);
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
  aspect-ratio: 500 / 892;
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
</style>
