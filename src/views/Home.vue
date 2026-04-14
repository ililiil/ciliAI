<template>
  <div class="home-container">
    <el-tabs v-model="activeTab" class="home-tabs">
      <el-tab-pane label="IP版权库" name="works">
        <div class="advertisements">
          <div 
            class="ad-item" 
            v-for="(ad, index) in ads" 
            :key="index"
            @click="handleAdClick(ad)"
          >
            <img :src="ad.src" :alt="ad.alt" class="ad-image">
          </div>
        </div>
        
        <div class="works-grid ip-library-grid">
          <div v-for="work in works" :key="work.id" class="work-card ip-library-card">
            <div class="work-image" @click="openNovelDetail(work)">
              <img 
                :src="getImageUrl(work)" 
                :alt="work.title" 
                class="work-image-img"
                @error="handleImageError($event, work)"
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
              <div class="work-stats simplified-stats">
                <div class="stat-item">
                  <span class="stat-label">版权信息：</span>
                  <span class="stat-value">{{ work.copyright || '番茄小说' }}</span>
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
      
      <el-tab-pane label="社区创作" name="community">
        <div class="community-grid">
          <div v-for="work in communityWorks" :key="work.id" class="community-card">
            <div class="community-image" @click="openNovelDetail(work)">
              <img 
                :src="getImageUrl(work)" 
                :alt="work.title" 
                class="community-image-img"
                @error="handleImageError($event, work)"
              >
              <div class="community-tags">
                <span v-for="tag in work.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="community-overlay">
                <span>查看详情</span>
              </div>
            </div>
            <div class="community-info">
              <h3 class="community-title">{{ work.title }}</h3>
              <div class="community-stats">
                <div class="community-stat-item">
                  <span class="community-stat-label">作者：</span>
                  <span class="community-stat-value">{{ work.studentName || 'CiliAI学员' }}</span>
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
import { ElTabs, ElTabPane, ElMessage } from 'element-plus'
import NovelDetailModal from '../components/NovelDetailModal.vue'

const activeTab = ref('works')
const showNovelModal = ref(false)
const selectedNovel = ref({})

const isLoggedIn = inject('isLoggedIn')
const computingPower = inject('computingPower')
const inviteCode = inject('currentInviteCode')

const ads = ref([])

const works = ref([])
const communityWorks = ref([])

const fetchWorks = async () => {
  try {
    const [worksResponse, featuredResponse, adsResponse] = await Promise.all([
      fetch('/api/works'),
      fetch('/api/works/featured'),
      fetch('/api/advertisements?status=published')
    ])
    
    const worksResult = await worksResponse.json()
    const featuredResult = await featuredResponse.json()
    const adsResult = await adsResponse.json()
    
    if (worksResult.code === 200) {
      console.log('Home.vue - Works API response:', worksResult)
      
      const allWorks = worksResult.data.list.map(work => {
        const category = work.category || 'IP版权库'
        const source = category === 'IP版权库' ? 'ip-library' : 'community'
        
        console.log('Home.vue - Processing work:', work.id, 'category:', category, 'source:', source)
        
        return {
          ...work,
          tags: work.tags ? JSON.parse(work.tags) : [],
          source: source,
          item_type: 'work'
        }
      })
      
      works.value = allWorks.filter(w => w.source === 'ip-library')
      communityWorks.value = allWorks.filter(w => w.source === 'community')
      
      console.log('Home.vue - Final works.value:', works.value)
    }
    
    if (adsResult.status === 'success' && adsResult.data && adsResult.data.list) {
      ads.value = adsResult.data.list.slice(0, 3).map((item) => ({
        src: item.image || `https://picsum.photos/800/400?random=${Math.random()}`,
        alt: item.title || '广告',
        link_url: item.link_url || ''
      }))
      console.log('Home.vue - Advertisements loaded:', ads.value)
    } else if (featuredResult.code === 200 && featuredResult.data && featuredResult.data.list) {
      ads.value = featuredResult.data.list.slice(0, 3).map((item, index) => ({
        src: item.image || `https://picsum.photos/800/400?random=${index + 100}`,
        alt: item.title || `推荐作品${index + 1}`,
        link_url: ''
      }))
      console.log('Home.vue - Featured ads loaded:', ads.value)
    }
  } catch (error) {
    console.error('获取作品列表失败:', error)
    ads.value = []
  }
}

const handleImageError = (e, work) => {
  console.error('图片加载失败 - work:', work, 'error event:', e)
  if (work && work.id) {
    e.target.src = `https://picsum.photos/400/600?random=${work.id}`
  } else {
    e.target.src = 'https://picsum.photos/400/600?random=' + Math.random()
  }
}

const getImageUrl = (work) => {
  console.log('getImageUrl - work:', work)
  console.log('getImageUrl - work.image:', work?.image)
  
  const imageUrl = work?.image
  
  if (!imageUrl) {
    console.warn('作品没有图片字段 - work:', work)
    return `https://picsum.photos/400/600?random=${work.id || Date.now()}`
  }
  
  if (Array.isArray(imageUrl)) {
    const url = imageUrl[0] || `https://picsum.photos/400/600?random=${work.id}`
    console.log('getImageUrl - Array image URL:', url)
    return url
  }
  
  if (typeof imageUrl === 'string') {
    const trimmedUrl = imageUrl.trim()
    
    if (trimmedUrl.length < 10) {
      console.warn('作品图片URL无效（太短）:', trimmedUrl)
      return `https://picsum.photos/400/600?random=${work.id || Date.now()}`
    }
    
    if (trimmedUrl.startsWith('data:image')) {
      console.log('getImageUrl - Base64 image')
      return trimmedUrl
    }
    
    if (trimmedUrl.startsWith('http://') || trimmedUrl.startsWith('https://')) {
      console.log('getImageUrl - HTTP image URL:', trimmedUrl)
      return trimmedUrl
    }
    
    console.warn('作品图片URL格式无效:', trimmedUrl)
    return `https://picsum.photos/400/600?random=${work.id || Date.now()}`
  }
  
  console.warn('作品图片字段类型无效:', typeof imageUrl)
  return `https://picsum.photos/400/600?random=${work.id || Date.now()}`
}

const handleAdClick = (ad) => {
  if (ad.link_url) {
    window.open(ad.link_url, '_blank')
  } else {
    ElMessage.info('该广告暂无跳转链接')
  }
}

onMounted(() => {
  fetchWorks()
  
  setInterval(() => {
    fetchWorks()
  }, 30000)
})

const openNovelDetail = (work) => {
  selectedNovel.value = work
  showNovelModal.value = true
}

const communityComments = {
  25: [
    { id: 1, author: '星空姐姐', avatar: '星', avatarColor: '#667eea', rating: 5, time: '2小时前', content: '视觉效果太惊艳了，空间站的构建非常宏大，氛围也很到位。AI生成的画面质量完全不输专业制作团队，强烈推荐！', likes: 328, replies: 45, isTop: true, isVip: true },
    { id: 2, author: '科幻迷小张', avatar: '科', avatarColor: '#f093fb', rating: 5, time: '5小时前', content: '终于有一部能让我沉浸其中的科幻作品了。剧情紧凑不拖沓，角色塑造立绘精美，会继续追更的！', likes: 245, replies: 32, isTop: false, isVip: false }
  ],
  26: [
    { id: 1, author: '时光收藏家', avatar: '时', avatarColor: '#a18cd1', rating: 5, time: '3小时前', content: '这个穿越设计太有新意了！不是简单的回到过去，而是与不同时空线的自己相遇，创意满分！', likes: 287, replies: 56, isTop: true, isVip: true },
    { id: 2, author: '热血动漫爱好者', avatar: '热', avatarColor: '#fbc2eb', rating: 5, time: '8小时前', content: '每一集都有新的惊喜，根本停不下来！已经三刷了，每次都能发现新的细节。', likes: 234, replies: 41, isTop: false, isVip: false }
  ],
  27: [
    { id: 1, author: '动作片发烧友', avatar: '动', avatarColor: '#ff6b6b', rating: 5, time: '1小时前', content: '战斗场面太燃了！每一个动作戏都设计得行云流水，看得热血沸腾。这制作水准绝对一流！', likes: 412, replies: 67, isTop: true, isVip: true },
    { id: 2, author: '都市白领小李', avatar: '都', avatarColor: '#4ecdc4', rating: 5, time: '4小时前', content: '主角人设太清了！既能又能，剧情全程在线。商战部分特别精彩，非常有代入感！', likes: 356, replies: 52, isTop: false, isVip: false }
  ],
  28: [
    { id: 1, author: '古风控小雅', avatar: '古', avatarColor: '#d299c2', rating: 5, time: '2小时前', content: '古风画面太唯美了，特效做得非常精致，服饰设计古典雅致，看起来是用心之作！', likes: 523, replies: 89, isTop: true, isVip: true },
    { id: 2, author: '悬疑小说家', avatar: '悬', avatarColor: '#fdeaa8', rating: 5, time: '6小时前', content: '世界观构建得非常完整，逻辑线清晰。主角的成长历程让人感同身受，加油！', likes: 445, replies: 72, isTop: false, isVip: true }
  ]
}

const getCommunityComments = (workId) => {
  return communityComments[workId] || []
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.home-tabs {
  width: 100%;
}

.home-tabs :deep(.el-tabs__content) {
  padding: 20px 0;
}

.home-tabs :deep(.el-tabs__item) {
  color: #425D5F !important; /* 设置未选中标签的文字颜色为白色 */
}

.home-tabs :deep(.el-tabs__item.is-active) {
  color: #425D5F !important; /* 保持选中标签的颜色为绿色 */
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
  background-color: #BACACB;
  border: 1px solid rgba(186, 202, 203, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.ad-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 93, 95, 0.3);
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
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(66, 93, 95, 0.15);
}

.work-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(66, 93, 95, 0.25);
}

.work-image {
  position: relative;
  width: 100%;
  height: 280px;
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
  width: 100%;
  height: 100%;
  background-color: rgba(66, 93, 95, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: #F8F7F2;
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
  background-color: rgba(250, 169, 67, 0.9);
  color: #425D5F;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
  border: 1px solid rgba(250, 169, 67, 0.3);
}

.work-info {
  padding: 16px;
  background-color: #F8F7F2;
}

.work-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #425D5F;
  border-bottom: 1px solid #BACACB;
  padding-bottom: 12px;
}

.work-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(186, 202, 203, 0.3);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: #425D5F;
  font-weight: 400;
}

.stat-value {
  color: #425D5F;
  font-weight: 600;
}

/* 社区分享卡片样式 */
.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 24px;
}

.community-card {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(66, 93, 95, 0.15);
  display: flex;
  flex-direction: column;
}

.community-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(66, 93, 95, 0.25);
}

.community-image {
  position: relative;
  width: 100%;
  height: 280px;
  overflow: hidden;
  cursor: pointer;
}

.community-image-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.community-card:hover .community-image-img {
  transform: scale(1.05);
}

.community-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(66, 93, 95, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: #F8F7F2;
  font-weight: 600;
  font-size: 16px;
}

.community-image:hover .community-overlay {
  opacity: 1;
}

.community-tags {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 8px;
}

.community-info {
  padding: 16px;
  background-color: #F8F7F2;
}

.community-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #425D5F;
  border-bottom: 1px solid #BACACB;
  padding-bottom: 12px;
}

.community-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.community-stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(186, 202, 203, 0.3);
}

.community-stat-item:last-child {
  border-bottom: none;
}

.community-stat-label {
  color: #425D5F;
  font-weight: 400;
}

.community-stat-value {
  color: #425D5F;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
    padding: 16px;
  }
  
  .work-image {
    width: 100%;
    height: 240px;
  }
  
  .community-image {
    width: 100%;
    height: 240px;
  }
}

@media (max-width: 480px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
  
  .community-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 12px;
  }
  
  .community-card {
    margin-bottom: 0;
  }
}

.work-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #BACACB;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.meta-label {
  color: #425D5F;
  min-width: 70px;
}

.meta-value {
  color: #425D5F;
  font-weight: 500;
}

.ip-library-grid {
  gap: 20px;
}

.ip-library-card .work-info {
  padding: 12px;
}

.ip-library-card .work-title {
  font-size: 15px;
  margin-bottom: 8px;
  padding-bottom: 8px;
}

.ip-library-card .simplified-stats {
  margin-top: 8px;
}

.ip-library-card .simplified-stats .stat-item {
  padding: 4px 0;
  font-size: 13px;
}

.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 24px;
}

.community-info-section {
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 12px;
  background-color: #F8F7F2;
}

.community-info-section::-webkit-scrollbar {
  width: 6px;
}

.community-info-section::-webkit-scrollbar-track {
  background: #BACACB;
  border-radius: 3px;
}

.community-info-section::-webkit-scrollbar-thumb {
  background: #425D5F;
  border-radius: 3px;
}

.community-header {
  background: linear-gradient(135deg, #BACACB 0%, #F8F7F2 100%);
  border: 1px solid #425D5F;
  border-radius: 8px;
  padding: 12px;
}

.community-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-row {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.meta-row .meta-label {
  color: #425D5F;
  min-width: 70px;
}

.meta-row .meta-value {
  color: #425D5F;
  font-weight: 600;
}

.community-params {
  background-color: #BACACB;
  border-radius: 8px;
  padding: 12px;
}

.params-title {
  color: #425D5F;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.params-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.param-item {
  display: flex;
  font-size: 13px;
  line-height: 1.4;
}

.param-label {
  color: #425D5F;
  min-width: 70px;
}

.param-value {
  color: #425D5F;
  font-weight: 500;
  flex: 1;
  word-break: break-word;
}

.community-comments {
  flex: 1;
  background-color: #1e1e1e;
  border-radius: 8px;
  padding: 12px;
  overflow-y: auto;
}

.community-comments::-webkit-scrollbar {
  width: 4px;
}

.community-comments::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 2px;
}

.community-comments::-webkit-scrollbar-thumb {
  background: #425D5F;
  border-radius: 2px;
}

.comments-title {
  color: #F8F7F2;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 10px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #333;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-item {
  background-color: #252525;
  border-radius: 8px;
  padding: 10px;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.comment-item:hover {
  background-color: #2a2a2a;
  border-color: #444;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #F8F7F2;
  font-weight: 600;
  font-size: 12px;
  box-shadow: 0 2px 6px rgba(66, 93, 95, 0.3);
}

.comment-author-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.comment-author {
  font-size: 13px;
  font-weight: 600;
  color: #F8F7F2;
}

.vip-badge {
  padding: 2px 6px;
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
  color: #425D5F;
  font-size: 10px;
  font-weight: 600;
  border-radius: 4px;
  text-transform: uppercase;
}

.comment-rating {
  display: flex;
  gap: 1px;
}

.comment-rating .star {
  color: #444;
  font-size: 12px;
}

.comment-rating .star.active {
  color: #ffd700;
}

.comment-body {
  padding-left: 42px;
}

.comment-text {
  font-size: 13px;
  color: #ccc;
  line-height: 1.5;
  margin: 0 0 8px 0;
}

.comment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-time {
  font-size: 11px;
  color: #888;
}

.comment-actions {
  display: flex;
  gap: 12px;
}

.action-item {
  font-size: 11px;
  color: #666;
}

.action-item:hover {
  color: #FAA943;
}

@media (max-width: 768px) {
  .community-grid {
    padding: 16px;
  }
  
  .community-info-section {
    padding: 12px;
    gap: 10px;
  }
  
  .community-header {
    padding: 10px;
  }
}
</style>