<template>
  <el-dialog
    v-model="visible"
    width="900px"
    :show-close="true"
    :close-on-click-modal="true"
    class="novel-detail-dialog"
    destroy-on-close
  >
    <template #header>
      <div class="dialog-header">
        <h2>{{ novelWithIntro.title }}</h2>
      </div>
    </template>
    
    <div class="novel-detail-content">
      <div class="novel-image-section">
        <div class="image-container">
          <button class="image-nav-btn prev-btn" @click="prevImage" :disabled="currentImageIndex === 0">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path>
            </svg>
          </button>
          <img :src="currentImage" :alt="novelWithIntro.title" class="novel-image">
          <button class="image-nav-btn next-btn" @click="nextImage" :disabled="currentImageIndex === 4">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path>
            </svg>
          </button>
        </div>
        <div class="image-indicators">
          <span 
            v-for="(_, index) in 5" 
            :key="index"
            class="indicator"
            :class="{ active: index === currentImageIndex }"
            @click="currentImageIndex = index"
          ></span>
        </div>
      </div>
      
      <div class="novel-info-section">
        <div class="info-item author-info">
          <div class="author-grid">
            <div class="author-item">
              <span class="author-label">学员名称：</span>
              <span class="author-value">{{ novelWithIntro.studentName || 'CiliAI学员' }}</span>
            </div>
            <div class="author-item">
              <span class="author-label">作品名称：</span>
              <span class="author-value">{{ novelWithIntro.title }}</span>
            </div>
          </div>
        </div>
        
        <div class="info-item">
          <h3 class="info-title">作品简介</h3>
          <p class="info-content">{{ novelWithIntro.introduction }}</p>
        </div>
        
        <div class="info-item">
          <h3 class="info-title">版权信息</h3>
          <p class="info-content">
            本作品由CiliAI制作，版权归CiliAI所有。未经授权，不得转载、复制或用于商业用途。
          </p>
        </div>
        
        <div class="info-item">
          <h3 class="info-title">作品详情</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">算力成本：</span>
              <span class="detail-value">{{ novelWithIntro.cost }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">制作时长：</span>
              <span class="detail-value">{{ novelWithIntro.duration }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">市场价格：</span>
              <span class="detail-value">{{ novelWithIntro.price }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">版权信息：</span>
              <span class="detail-value">{{ novelWithIntro.copyright }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">分账模式：</span>
              <span class="detail-value">100%分账</span>
            </div>
          </div>
        </div>
        
        <div class="info-item">
          <h3 class="info-title">标签</h3>
          <div class="tags-container">
            <span v-for="tag in novelWithIntro.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button type="primary" class="action-button add-button" @click="addToProject" :loading="adding">
            加入项目
          </el-button>
          <el-button type="default" class="action-button create-button" @click="showTeacherQR">
            我要创作
          </el-button>
        </div>
        
        <div class="modal-comments">
          <div class="comments-header">
            <div class="comments-title">
              <span>学员评价</span>
              <span class="comments-count">({{ comments.length }}条)</span>
            </div>
            <div class="rating-summary">
              <div class="stars">
                <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= averageRating }">★</span>
              </div>
              <span class="rating-text">{{ averageRating.toFixed(1) }}</span>
            </div>
          </div>
          
          <div class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-avatar-wrapper">
                <div class="comment-avatar" :style="{ backgroundColor: comment.avatarColor }">
                  {{ comment.avatar }}
                </div>
                <div v-if="comment.isTop" class="top-badge">置顶</div>
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <div class="comment-author-info">
                    <span class="comment-author">{{ comment.author }}</span>
                    <span v-if="comment.isVip" class="vip-badge">VIP</span>
                    <span class="comment-time">{{ comment.time }}</span>
                  </div>
                  <div class="comment-rating">
                    <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= comment.rating }">★</span>
                  </div>
                </div>
                <div class="comment-content">{{ comment.content }}</div>
                <div class="comment-actions">
                  <div class="action-item likes">
                    <span>赞 {{ comment.likes }}</span>
                  </div>
                  <div class="action-item replies">
                    <span>回复 {{ comment.replies }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  
  <el-dialog
    v-model="showQRModal"
    width="400px"
    :show-close="true"
    class="qr-code-dialog"
  >
    <div class="qr-code-content">
      <h3>请联系导师获取创作权限</h3>
      <div class="qr-code-container">
        <img src="https://picsum.photos/300/300" alt="Teacher QR Code" class="qr-code-image">
      </div>
      <p class="qr-code-note">扫描上方二维码联系导师</p>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  novel: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(props.modelValue)
const showQRModal = ref(false)
const currentImageIndex = ref(0)

const novelWithIntro = computed(() => ({
  ...props.novel,
  introduction: props.novel.introduction || '这是一部精彩的AI短剧作品，由CiliAI精心制作。'
}))

const currentImage = computed(() => {
  const imageId = props.novel.id || 1
  return `https://picsum.photos/400/600?random=${imageId * 10 + currentImageIndex.value}`
})

const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

const nextImage = () => {
  if (currentImageIndex.value < 4) {
    currentImageIndex.value++
  }
}

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    currentImageIndex.value = 0
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const showTeacherQR = () => {
  showQRModal.value = true
}

const adding = ref(false)

const allWorkComments = {
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

const comments = computed(() => {
  return allWorkComments[props.novel.id] || []
})

const averageRating = computed(() => {
  if (comments.value.length === 0) return 0
  const total = comments.value.reduce((sum, comment) => sum + comment.rating, 0)
  return total / comments.value.length
})

const addToProject = async () => {
  adding.value = true
  try {
    const inviteCode = localStorage.getItem('inviteCode')
    if (!inviteCode) {
      ElMessage.error('请先登录')
      adding.value = false
      return
    }

    const response = await fetch('/api/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        invite_code: inviteCode,
        title: novelWithIntro.value.title,
        description: `来自IP版权库的作品：${novelWithIntro.value.title}`
      })
    })

    const result = await response.json()
    if (result.status === 'success') {
      ElMessage.success('已成功加入项目！')
      showQRModal.value = false
    } else {
      ElMessage.error(result.message || '加入失败')
    }
  } catch (error) {
    console.error('加入项目失败:', error)
    ElMessage.error('加入失败，请稍后重试')
  } finally {
    adding.value = false
  }
}
</script>

<style scoped>
.novel-detail-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 12px !important;
  --el-dialog-padding-primary: 0 !important;
}

.dialog-header {
  padding: 24px 24px 0;
  text-align: center;
}

.dialog-header h2 {
  color: #425D5F;
  font-size: 20px;
  margin: 0;
}

.novel-detail-content {
  display: flex;
  padding: 24px;
  gap: 32px;
}

.novel-image-section {
  flex-shrink: 0;
  width: 300px;
}

.image-container {
  position: relative;
  width: 100%;
  height: 450px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.novel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(66, 93, 95, 0.9);
  color: #F8F7F2;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.image-nav-btn:hover {
  background-color: rgba(66, 93, 95, 1);
  transform: translateY(-50%) scale(1.1);
}

.image-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.prev-btn {
  left: 12px;
}

.next-btn {
  right: 12px;
}

.image-indicators {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #444;
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background-color: #425D5F;
  width: 12px;
}

.indicator:hover {
  background-color: #BACACB;
}

.novel-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-item {
  background-color: #BACACB;
  border-radius: 8px;
  padding: 16px;
}

.info-title {
  color: #425D5F;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.info-content {
  color: #425D5F;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.detail-label {
  color: #425D5F;
}

.detail-value {
  color: #425D5F;
  font-weight: 500;
}

.author-info {
  background: linear-gradient(135deg, #BACACB 0%, #F8F7F2 100%);
  border: 1px solid #425D5F;
}

.author-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.author-item {
  display: flex;
  align-items: center;
  font-size: 15px;
}

.author-label {
  color: #425D5F;
  min-width: 80px;
}

.author-value {
  color: #425D5F;
  font-weight: 600;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: rgba(163, 230, 53, 0.2);
  color: #425D5F;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 16px;
}

.action-button {
  flex: 1;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.add-button {
  background: linear-gradient(135deg, #425D5F 0%, #425D5F 100%);
  border: none;
  color: #F8F7F2;
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 93, 95, 0.3);
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
}

.create-button {
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
  border: none;
  color: #425D5F;
}

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(250, 169, 67, 0.3);
  background: linear-gradient(135deg, #FDE7A2 0%, #FAA943 100%);
}

.qr-code-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 12px !important;
}

.qr-code-content {
  text-align: center;
  padding: 24px;
}

.qr-code-content h3 {
  color: #425D5F;
  margin: 0 0 24px 0;
}

.qr-code-container {
  margin: 24px 0;
}

.qr-code-image {
  width: 200px;
  height: 200px;
  object-fit: contain;
  border-radius: 8px;
}

.qr-code-note {
  color: #425D5F;
  font-size: 14px;
  margin-top: 16px;
}

.modal-comments {
  padding: 20px;
  background: linear-gradient(180deg, #BACACB 0%, #F8F7F2 100%);
  border-radius: 8px;
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.modal-comments::-webkit-scrollbar {
  width: 6px;
}

.modal-comments::-webkit-scrollbar-track {
  background: #BACACB;
  border-radius: 3px;
}

.modal-comments::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 3px;
}

.modal-comments::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #333;
}

.comments-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #425D5F;
}

.comments-count {
  color: #425D5F;
  font-weight: 400;
  font-size: 13px;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #444;
  font-size: 15px;
  transition: all 0.3s ease;
}

.star.active {
  color: #ffd700;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
}

.rating-text {
  font-size: 15px;
  font-weight: 600;
  color: #ffd700;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.comment-item {
  display: flex;
  gap: 14px;
  padding: 14px;
  background-color: #1e1e1e;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.comment-item:hover {
  background-color: #252525;
  border-color: #444;
}

.comment-avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #F8F7F2;
  font-weight: 600;
  font-size: 15px;
  box-shadow: 0 2px 8px rgba(66, 93, 95, 0.3);
  transition: all 0.3s ease;
}

.comment-avatar:hover {
  transform: scale(1.1);
}

.top-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  font-size: 12px;
  color: #ff6b6b;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.comment-author {
  font-size: 14px;
  font-weight: 600;
  color: #425D5F;
}

.vip-badge {
  padding: 2px 8px;
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
  color: #425D5F;
  font-size: 11px;
  font-weight: 600;
  border-radius: 4px;
  text-transform: uppercase;
}

.comment-time {
  font-size: 12px;
  color: #888;
}

.comment-rating {
  display: flex;
  gap: 2px;
}

.comment-rating .star {
  font-size: 13px;
}

.comment-content {
  font-size: 14px;
  color: #ccc;
  line-height: 1.6;
  margin-bottom: 10px;
}

.comment-actions {
  display: flex;
  gap: 20px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #666;
  transition: all 0.3s ease;
}

.action-item:hover {
  color: #425D5F;
}

@media (max-width: 768px) {
  .novel-detail-content {
    flex-direction: column;
    align-items: center;
  }
  
  .novel-image-section {
    width: 100%;
    max-width: 300px;
  }
  
  .novel-image {
    height: 400px;
  }
  
  .novel-info-section {
    width: 100%;
  }
}
</style>
