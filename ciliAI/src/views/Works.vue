<template>
  <div class="works-page">
    <!-- 顶部 Tab 和创建按钮 -->
    <div class="page-header">
      <div class="tabs">
        <div
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
          <span class="tab-count">({{ tab.count }})</span>
        </div>
      </div>
      <el-button type="primary" class="create-btn" @click="createProject">
        <el-icon><Plus /></el-icon>
        创建项目
      </el-button>
    </div>

    <!-- 项目列表 -->
    <div class="projects-grid">
      <div
        v-for="project in filteredProjects"
        :key="project.id"
        class="project-card"
        @click="viewProject(project.id)"
      >
        <!-- 缩略图 -->
        <div class="project-thumbnail">
          <img :src="project.thumbnail" :alt="project.title" />
          <!-- 更多操作按钮 -->
          <div class="more-btn" @click.stop="showMoreMenu($event, project)">
            <el-icon><MoreFilled /></el-icon>
          </div>
          <!-- 集数标签 -->
          <div class="episode-tag">共{{ project.episodes }}集</div>
        </div>

        <!-- 项目信息 -->
        <div class="project-info">
          <h3 class="project-title">{{ project.title }}</h3>
          <div class="project-meta">
            <span class="meta-time">{{ project.createTime }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredProjects.length === 0" class="empty-state">
      <el-empty description="暂无项目">
        <template #image>
          <div class="empty-icon">
            <el-icon :size="60"><FolderOpened /></el-icon>
          </div>
        </template>
        <el-button type="primary" @click="createProject">
          创建第一个项目
        </el-button>
      </el-empty>
    </div>

    <!-- 创建项目模态框 -->
    <CreateProjectModal v-model="showCreateModal" @create="handleProjectCreate" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus,
  MoreFilled,
  User,
  FolderOpened
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CreateProjectModal from '../components/CreateProjectModal.vue'

const router = useRouter()

const isLoggedIn = inject('isLoggedIn')
const inviteCode = inject('currentInviteCode')

const showCreateModal = ref(false)

const activeTab = ref('my')
const tabs = computed(() => [
  { key: 'my', label: '我的项目', count: myProjects.value.length }
])

const myProjects = ref([])

const fetchProjects = async () => {
  if (!inviteCode.value) {
    myProjects.value = []
    return
  }
  
  try {
    const response = await fetch(`/api/projects?invite_code=${encodeURIComponent(inviteCode.value)}`)
    const result = await response.json()
    if (result.status === 'success') {
      myProjects.value = result.projects.map(p => ({
        id: p.id,
        title: p.title,
        thumbnail: p.cover_image || `https://picsum.photos/400/225?random=${p.id}`,
        episodes: p.image_count || 0,
        createTime: p.create_time,
        collaborators: 1
      }))
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

onMounted(() => {
  if (inviteCode.value) {
    fetchProjects()
  }
})

const filteredProjects = computed(() => {
  return myProjects.value
})

const createProject = () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }
  showCreateModal.value = true
}

const handleProjectCreate = async (formData) => {
  if (!inviteCode.value) {
    ElMessage.error('请先登录')
    return
  }
  
  try {
    const response = await fetch('/api/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        invite_code: inviteCode.value,
        title: formData.projectName,
        description: ''
      })
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      ElMessage.success('项目创建成功')
      fetchProjects()
    } else {
      ElMessage.error(result.message || '创建失败')
    }
  } catch (error) {
    console.error('创建项目失败:', error)
    ElMessage.error('创建失败，请稍后重试')
  }
}

const viewProject = (id) => {
  router.push(`/project/${id}`)
}

const showMoreMenu = (event, project) => {
  event.stopPropagation()
  console.log('显示更多菜单', project)
}
</script>

<style scoped>
.works-page {
  padding: 20px 24px;
  background-color: #F8F7F2;
  min-height: 100%;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

/* Tab 样式 */
.tabs {
  display: flex;
  gap: 24px;
}

.tab {
  font-size: 14px;
  color: #888;
  cursor: pointer;
  padding-bottom: 8px;
  position: relative;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #ccc;
}

.tab.active {
  color: #425D5F;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #425D5F;
}

.tab-count {
  color: #425D5F;
  margin-left: 4px;
}

.tab.active .tab-count {
  color: #425D5F;
}

/* 创建按钮 */
.create-btn {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
  font-weight: 500;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 6px;
}

.create-btn:hover {
  background-color: #FAA943;
  border-color: #FAA943;
}

.create-btn .el-icon {
  margin-right: 4px;
  font-size: 14px;
}

/* 项目网格 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.project-card {
  background-color: #BACACB;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* 缩略图 */
.project-thumbnail {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
}

.project-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.project-card:hover .project-thumbnail img {
  transform: scale(1.05);
}

/* 更多按钮 */
.more-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  background-color: rgba(66, 93, 95, 0.8);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #F8F7F2;
  font-size: 14px;
}

.more-btn:hover {
  background-color: rgba(66, 93, 95, 0.9);
}

/* 集数标签 */
.episode-tag {
  position: absolute;
  bottom: 8px;
  right: 8px;
  padding: 2px 8px;
  background-color: rgba(66, 93, 95, 0.8);
  border-radius: 4px;
  font-size: 12px;
  color: #F8F7F2;
}

/* 项目信息 */
.project-info {
  padding: 12px;
}

.project-title {
  font-size: 14px;
  font-weight: 500;
  color: #425D5F;
  margin: 0 0 8px 0;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-time {
  font-size: 12px;
  color: #666;
}

.meta-collaborators {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #666;
}

.meta-collaborators .el-icon {
  font-size: 12px;
}

/* 空状态 */
.empty-state {
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon {
  color: #444;
  margin-bottom: 16px;
}

.empty-state :deep(.el-empty__description) {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

/* 响应式 */
@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .create-btn {
    align-self: flex-end;
  }
}

@media (max-width: 480px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
