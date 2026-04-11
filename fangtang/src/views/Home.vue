<template>
  <div class="home-container">
    <el-tabs v-model="activeTab" class="home-tabs">
      <el-tab-pane label="IP版权库" name="works">
        <!-- 广告位区域 -->
        <div class="advertisements">
          <div class="ad-item" v-for="(ad, index) in ads" :key="index">
            <img :src="ad.src" :alt="ad.alt" class="ad-image">
          </div>
        </div>
        
        <div class="works-grid">
          <div v-for="work in works" :key="work.id" class="work-card">
            <div class="work-image" @click="openNovelDetail(work)">
              <img 
                :src="work.image" 
                :alt="work.title" 
                class="work-image-img"
                @error="handleImageError"
              >
              <div class="work-tags">
                <span v-for="tag in work.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="view-detail-overlay">
                <span>查看详情</span>
              </div>
            </div>
            <div class="work-info">
                <h3 class="work-title">{{ work.title }}</h3>
                <div class="work-stats">
                  <div class="stat-item">
                    <span class="stat-label">算力成本：</span>
                    <span class="stat-value">{{ work.cost }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">制作时长：</span>
                    <span class="stat-value">{{ work.duration }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">市场售价：</span>
                    <span class="stat-value">{{ work.price }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">版权信息：</span>
                    <span class="stat-value">番茄小说</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">分账模式：</span>
                    <span class="stat-value">100%分账</span>
                  </div>
                </div>
              </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="社区分享" name="community">
        <div class="works-grid">
          <div v-for="work in communityWorks" :key="work.id" class="work-card">
            <div class="work-image" @click="openNovelDetail(work)">
              <img 
                :src="work.image" 
                :alt="work.title" 
                class="work-image-img"
                @error="handleImageError"
              >
              <div class="work-tags">
                <span v-for="tag in work.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="view-detail-overlay">
                <span>查看详情</span>
              </div>
            </div>
            <div class="work-info">
                <div class="work-meta">
                  <div class="meta-item">
                    <span class="meta-label">学员名称：</span>
                    <span class="meta-value">{{ work.studentName }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">作品名称：</span>
                    <span class="meta-value">{{ work.title }}</span>
                  </div>
                </div>
                <div class="work-stats">
                  <div class="stat-item">
                    <span class="stat-label">算力成本：</span>
                    <span class="stat-value">{{ work.cost }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">制作时长：</span>
                    <span class="stat-value">{{ work.duration }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">市场售价：</span>
                    <span class="stat-value">{{ work.price }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">版权信息：</span>
                    <span class="stat-value">番茄小说</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">分账模式：</span>
                    <span class="stat-value">100%分账</span>
                  </div>
                </div>
              </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- Novel Detail Modal -->
    <NovelDetailModal v-model="showNovelModal" :novel="selectedNovel" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { ElTabs, ElTabPane } from 'element-plus'
import NovelDetailModal from '../components/NovelDetailModal.vue'

const activeTab = ref('works')
const showNovelModal = ref(false)
const selectedNovel = ref({})

const isLoggedIn = inject('isLoggedIn')
const computingPower = inject('computingPower')
const inviteCode = inject('currentInviteCode')

const ads = ref([
  { src: 'https://pubsto.fullpeace.cn/freefishpc/file/726afab63d004543b7c1069d27d89bb4.png', alt: '广告位1' },
  { src: 'https://pubsto.fullpeace.cn/freefishpc/file/d86bf1a04eaa45bf8e5faa71f5d33308.png', alt: '广告位2' },
  { src: 'https://pubsto.fullpeace.cn/freefishpc/file/34264806d3ef5eb00ad8877e0140d1e1.png', alt: '广告位3' }
])

const works = ref([])
const communityWorks = ref([])

const fetchWorks = async () => {
  try {
    const response = await fetch('http://localhost:5002/api/works')
    const result = await response.json()
    if (result.code === 200) {
      const allWorks = result.data.list.map(work => ({
        ...work,
        tags: work.tags ? JSON.parse(work.tags) : []
      }))
      
      works.value = allWorks.filter(w => !w.student_name || w.student_name === '方塘官方')
      communityWorks.value = allWorks.filter(w => w.student_name && w.student_name !== '方塘官方')
    }
  } catch (error) {
    console.error('获取作品列表失败:', error)
  }
}

const handleImageError = (e) => {
  e.target.src = 'https://picsum.photos/400/600?random=' + Math.random()
}

onMounted(() => {
  fetchWorks()
})

const openNovelDetail = (work) => {
  selectedNovel.value = work
  showNovelModal.value = true
}
</script>

<style scoped>
.home-container {
  padding: 0;
}

.home-tabs {
  width: 100%;
}

.home-tabs :deep(.el-tabs__content) {
  padding: 20px 0;
}

.home-tabs :deep(.el-tabs__item) {
  color: #ffffff !important; /* 设置未选中标签的文字颜色为白色 */
}

.home-tabs :deep(.el-tabs__item.is-active) {
  color: #a3e635 !important; /* 保持选中标签的颜色为绿色 */
}

.home-tabs :deep(.el-tabs__nav-wrap)::after {
  height: 0 !important; /* 移除底部边框线 */
}

.advertisements {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 20px;
  margin-bottom: 20px;
}

.ad-item {
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #2c2c2c;
}

.ad-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 24px;
}

.work-card {
  background-color: #232323;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.work-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.work-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
}

.work-image-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.work-card:hover .work-image-img {
  transform: scale(1.05);
}

.view-detail-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
}

.work-image:hover .view-detail-overlay {
  opacity: 1;
}

.work-tags {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 8px;
}

.tag {
  background-color: rgba(163, 230, 53, 0.8);
  color: #1a1a1a;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.work-info {
  padding: 16px;
}

.work-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.work-stats {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.stat-label {
  color: #999;
}

.stat-value {
  color: #a3e635;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
    padding: 16px;
  }
  
  .work-image {
    height: 160px;
  }
}

@media (max-width: 480px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
}

.work-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #333;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.meta-label {
  color: #999;
  min-width: 70px;
}

.meta-value {
  color: #fff;
  font-weight: 500;
}
</style>