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
      <!-- Left Section: Novel Main Image -->
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
      
      <!-- Right Section: Detailed Information -->
      <div class="novel-info-section">
        <!-- 学员和作品信息 -->
        <div class="info-item author-info">
          <div class="author-grid">
            <div class="author-item">
              <span class="author-label">学员名称：</span>
              <span class="author-value">{{ novelWithIntro.studentName || '方塘学员' }}</span>
            </div>
            <div class="author-item">
              <span class="author-label">作品名称：</span>
              <span class="author-value">{{ novelWithIntro.title }}</span>
            </div>
          </div>
        </div>
        
        <!-- Novel Introduction -->
        <div class="info-item">
          <h3 class="info-title">作品简介</h3>
          <p class="info-content">{{ novelWithIntro.introduction }}</p>
        </div>
        
        <!-- Copyright Information -->
        <div class="info-item">
          <h3 class="info-title">版权信息</h3>
          <p class="info-content">
            本作品由方塘AI制作，版权归方塘所有。未经授权，不得转载、复制或用于商业用途。
          </p>
        </div>
        
        <!-- Additional Description -->
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
              <span class="detail-label">市场售价：</span>
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
        
        <!-- Tags -->
        <div class="info-item">
          <h3 class="info-title">标签</h3>
          <div class="tags-container">
            <span v-for="tag in novelWithIntro.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons">
          <el-button type="primary" class="action-button add-button" @click="addToProject" :loading="adding">
            <span class="button-icon">📚</span>
            加入项目
          </el-button>
          <el-button type="default" class="action-button create-button" @click="showTeacherQR">
            <span class="button-icon">✨</span>
            我要创作
          </el-button>
        </div>
        
        <!-- Comments Section -->
        <div class="modal-comments">
          <div class="comments-header">
            <div class="comments-title">
              <span class="title-icon">💬</span>
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
                <div v-if="comment.isTop" class="top-badge">🔥</div>
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
                    <span class="action-icon">👍</span>
                    <span>{{ comment.likes }}</span>
                  </div>
                  <div class="action-item replies">
                    <span class="action-icon">💬</span>
                    <span>{{ comment.replies }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  
  <!-- Teacher QR Code Modal -->
  <el-dialog
    v-model="showQRModal"
    width="400px"
    :show-close="true"
    class="qr-code-dialog"
  >
    <div class="qr-code-content">
      <h3>请联系老师获取创作权限</h3>
      <div class="qr-code-container">
        <!-- Temporarily hardcoded QR code image -->
        <img src="https://picsum.photos/300/300" alt="Teacher QR Code" class="qr-code-image">
      </div>
      <p class="qr-code-note">扫描上方二维码联系老师</p>
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
  introduction: props.novel.introduction || '这是一部精彩的AI短剧作品，由方塘AI精心制作。'
}))

// Compute current image based on index
const currentImage = computed(() => {
  // Generate random image URL based on index and novel id
  const imageId = props.novel.id || 1
  return `https://picsum.photos/400/600?random=${imageId * 10 + currentImageIndex.value}`
})

// Navigation methods
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

// Reset image index when modal opens or novel changes
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

// Comments data for each work
const allWorkComments = {
  25: [
    { id: 1, author: '星空漫步者', avatar: '星', avatarColor: '#667eea', rating: 5, time: '2小时前', content: '视觉效果太震撼了！宇宙场景的构建非常宏大，配乐也很到位。AI生成的画面质量完全不输专业制作团队，强力推荐！', likes: 328, replies: 45, isTop: true, isVip: true },
    { id: 2, author: '科幻迷小王', avatar: '王', avatarColor: '#f093fb', rating: 5, time: '5小时前', content: '终于有一部能让我沉浸其中的科幻作品了。剧情紧凑不拖沓，角色塑造立体饱满，会继续追更的！', likes: 245, replies: 32, isTop: false, isVip: false },
    { id: 3, author: '内容创作者阿明', avatar: '明', avatarColor: '#4facfe', rating: 4, time: '1天前', content: '作为同行真的很有启发。特别是光影效果的运用，给了我很多灵感。期待更多精彩内容！', likes: 189, replies: 28, isTop: false, isVip: true },
    { id: 4, author: '追剧达人Linda', avatar: 'L', avatarColor: '#43e97b', rating: 5, time: '1天前', content: '一口气追完了全部更新，太好看了！每个情节都设计得很巧妙，完全猜不到下一步发展', likes: 156, replies: 21, isTop: false, isVip: false },
    { id: 5, author: '周末影评人', avatar: '周', avatarColor: '#fa709a', rating: 4, time: '2天前', content: '周末一口气看完，沉浸感很强。唯一希望的是更新能再快一些，根本不够看啊！', likes: 98, replies: 15, isTop: false, isVip: false }
  ],
  26: [
    { id: 1, author: '时光收藏家', avatar: '时', avatarColor: '#a18cd1', rating: 5, time: '3小时前', content: '这个穿越设定太有新意了！不是简单的回到过去，而是与不同时间线的自己对话，构思非常巧妙。', likes: 287, replies: 56, isTop: true, isVip: true },
    { id: 2, author: '烧脑剧爱好者', avatar: '烧', avatarColor: '#fbc2eb', rating: 5, time: '8小时前', content: '每一集都有新的悬念，根本停不下来！已经三刷了，每次都能发现新的细节，太上头了。', likes: 234, replies: 41, isTop: false, isVip: false },
    { id: 3, author: '剧情分析师老李', avatar: '李', avatarColor: '#a1ecff', rating: 5, time: '1天前', content: '不得不夸一下编剧的逻辑思维，时间线处理得滴水不漏。第五集那个反转直接看哭了，推荐给所有朋友！', likes: 198, replies: 37, isTop: false, isVip: true }
  ],
  27: [
    { id: 1, author: '动作片发烧友', avatar: '动', avatarColor: '#ff6b6b', rating: 5, time: '1小时前', content: '打斗场面太燃了！每一场动作戏都设计得行云流水，看得热血沸腾。这制作水准绝对一流！', likes: 412, replies: 67, isTop: true, isVip: true },
    { id: 2, author: '都市白领小陈', avatar: '陈', avatarColor: '#4ecdc4', rating: 5, time: '4小时前', content: '主角人设太帅了！又酷又能打，智商全程在线。市井气息还原得很真实，很有代入感。', likes: 356, replies: 52, isTop: false, isVip: false },
    { id: 3, author: '剧评人Tommy', avatar: 'T', avatarColor: '#45b7d1', rating: 4, time: '12小时前', content: '节奏把控得很好，一集40分钟完全没有尿点。期待后续剧情发展！', likes: 278, replies: 43, isTop: false, isVip: true }
  ],
  28: [
    { id: 1, author: '仙侠迷小雪', avatar: '雪', avatarColor: '#d299c2', rating: 5, time: '2小时前', content: '仙气飘飘的画面太美了！特效做得非常精致，法术对决的场面恢宏大气，看得出来是用心之作。', likes: 523, replies: 89, isTop: true, isVip: true },
    { id: 2, author: '玄幻小说控', avatar: '玄', avatarColor: '#fdeaa8', rating: 5, time: '6小时前', content: '世界观构建得很完整，修炼体系逻辑清晰。主角的成长历程让人感同身受，加油！', likes: 445, replies: 72, isTop: false, isVip: true },
    { id: 3, author: '古风爱好者阿月', avatar: '月', avatarColor: '#ffd1dc', rating: 5, time: '1天前', content: '每一帧都可以当壁纸！服装道具都很有质感，完美诠释了我心中的仙侠世界。', likes: 389, replies: 61, isTop: false, isVip: false }
  ],
  29: [
    { id: 1, author: '喜剧达人欢欢', avatar: '欢', avatarColor: '#ffecd2', rating: 5, time: '30分钟前', content: '笑到肚子疼！室友都被我传染了，集体追剧。人物关系处理得很巧妙，梗特别多！', likes: 678, replies: 102, isTop: true, isVip: false },
    { id: 2, author: '压力山大上班族', avatar: '压', avatarColor: '#fcb69f', rating: 5, time: '3小时前', content: '下班回家看这个简直太治愈了！轻松愉快的氛围，完美解压神剧，每天就等着更新。', likes: 592, replies: 87, isTop: false, isVip: true },
    { id: 3, author: '闺蜜追剧团', avatar: '闺', avatarColor: '#ff9a9e', rating: 5, time: '1天前', content: '我们寝室四个人一起追的，每集结束都要讨论半天。台词太经典了，都快背下来了！', likes: 478, replies: 76, isTop: false, isVip: false }
  ],
  30: [
    { id: 1, author: '探险家老张', avatar: '张', avatarColor: '#8b5a2b', rating: 5, time: '1小时前', content: '紧张刺激到不行！每次下墓都提心吊胆，音效配合得很好，身临其境的感觉太棒了！', likes: 489, replies: 78, isTop: true, isVip: true },
    { id: 2, author: '悬疑剧忠实粉', avatar: '悬', avatarColor: '#667eea', rating: 5, time: '5小时前', content: '每个谜题都设计得恰到好处，不会太简单也不会太刁钻。线索铺垫得很细致，值得反复推敲。', likes: 423, replies: 69, isTop: false, isVip: true }
  ],
  31: [
    { id: 1, author: '宫斗剧资深粉', avatar: '宫', avatarColor: '#c471ed', rating: 5, time: '2小时前', content: '宫斗戏码精彩绝伦！每个嫔妃都有自己的小心思，权谋算计让人拍案叫绝，大女主太飒了！', likes: 567, replies: 91, isTop: true, isVip: true },
    { id: 2, author: '历史剧爱好者', avatar: '历', avatarColor: '#f5af19', rating: 5, time: '7小时前', content: '服化道非常考究，还原度极高。甄嬛传的既视感，但又有自己独特的风格，很喜欢！', likes: 498, replies: 83, isTop: false, isVip: true }
  ],
  32: [
    { id: 1, author: '赛博朋克迷', avatar: '赛', avatarColor: '#00d2ff', rating: 5, time: '1小时前', content: '未来世界的构建太牛了！霓虹灯光、摩天大楼、飞行汽车，完美诠释了什么叫赛博朋克！', likes: 612, replies: 97, isTop: true, isVip: true },
    { id: 2, author: '科技博主极客', avatar: '极', avatarColor: '#667eea', rating: 5, time: '4小时前', content: '作为科技从业者看得很激动！里面很多未来科技的设想很有前瞻性，剧情也很引人深思。', likes: 534, replies: 85, isTop: false, isVip: true }
  ],
  33: [
    { id: 1, author: '武侠小说重度患者', avatar: '武', avatarColor: '#eecda3', rating: 5, time: '2小时前', content: '江湖味道太浓了！刀光剑影、快意恩仇，这才是我心目中的武侠世界，打斗设计超燃！', likes: 534, replies: 86, isTop: true, isVip: true },
    { id: 2, author: '功夫电影爱好者', avatar: '功', avatarColor: '#ef629f', rating: 5, time: '6小时前', content: '武术指导太专业了！每个动作都干净利落，行云流水。轻功设计也很飘逸，看得过瘾！', likes: 467, replies: 74, isTop: false, isVip: true }
  ],
  34: [
    { id: 1, author: '青春回忆录', avatar: '青', avatarColor: '#ffecd2', rating: 5, time: '1小时前', content: '太真实了！仿佛看到了当年的自己，那些友情、懵懂的感情、青涩的时光，都太美好了！', likes: 723, replies: 112, isTop: true, isVip: false },
    { id: 2, author: '大学毕业生小李', avatar: '李', avatarColor: '#fcb69f', rating: 5, time: '4小时前', content: '看完特别怀念大学时光！每个角色都能找到共鸣，青春就是这样美好而纯粹呀。', likes: 645, replies: 98, isTop: false, isVip: true }
  ],
  35: [
    { id: 1, author: '名侦探柯柯', avatar: '侦', avatarColor: '#4b6cb7', rating: 5, time: '3小时前', content: '推理过程太烧脑了！每一集都在猜凶手，但每次都猜错，编剧的水平太高了！', likes: 456, replies: 73, isTop: true, isVip: true },
    { id: 2, author: '悬疑小说作家', avatar: '悬', avatarColor: '#667eea', rating: 5, time: '8小时前', content: '从创作者角度说，这个剧本结构非常严谨。伏笔埋得很深，回头看才发现全是线索。', likes: 398, replies: 64, isTop: false, isVip: true }
  ],
  36: [
    { id: 1, author: '商业精英Emily', avatar: 'E', avatarColor: '#c0c0c0', rating: 5, time: '2小时前', content: '商战戏码太刺激了！职场博弈、资本运作，看得热血沸腾。主角的逆袭之路太燃了！', likes: 534, replies: 82, isTop: true, isVip: true },
    { id: 2, author: 'MBA在读学员', avatar: 'M', avatarColor: '#ffd700', rating: 5, time: '6小时前', content: '把商业逻辑讲得很透彻！每一个决策背后的思考都很有深度，值得反复品味。', likes: 467, replies: 71, isTop: false, isVip: true }
  ]
}

// Get comments for current work
const comments = computed(() => {
  return allWorkComments[props.novel.id] || []
})

// Calculate average rating
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
  --el-dialog-bg-color: #1d1d1d !important;
  --el-dialog-border-radius: 12px !important;
  --el-dialog-padding-primary: 0 !important;
}

.dialog-header {
  padding: 24px 24px 0;
  text-align: center;
}

.dialog-header h2 {
  color: #ffffff;
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
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.image-nav-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
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
  background-color: #a3e635;
  width: 12px;
}

.indicator:hover {
  background-color: #666;
}

.novel-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-item {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 16px;
}

.info-title {
  color: #a3e635;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.info-content {
  color: #e0e0e0;
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
  color: #999;
}

.detail-value {
  color: #a3e635;
  font-weight: 500;
}

.author-info {
  background: linear-gradient(135deg, #2a3a2a 0%, #1a2a1a 100%);
  border: 1px solid #3a4a3a;
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
  color: #8a9a8a;
  min-width: 80px;
}

.author-value {
  color: #a3e635;
  font-weight: 600;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: rgba(163, 230, 53, 0.2);
  color: #a3e635;
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

.button-icon {
  font-size: 16px;
}

.add-button {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  border: none;
  color: #ffffff;
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
}

.create-button {
  background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%);
  border: none;
  color: #1d1d1d;
}

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(163, 230, 53, 0.3);
  background: linear-gradient(135deg, #84cc16 0%, #a3e635 100%);
}

/* QR Code Modal */
.qr-code-dialog {
  --el-dialog-bg-color: #1d1d1d !important;
  --el-dialog-border-radius: 12px !important;
}

.qr-code-content {
  text-align: center;
  padding: 24px;
}

.qr-code-content h3 {
  color: #ffffff;
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
  color: #999;
  font-size: 14px;
  margin-top: 16px;
}

/* Modal Comments Section */
.modal-comments {
  padding: 20px;
  background: linear-gradient(180deg, #2a2a2a 0%, #232323 100%);
  border-radius: 8px;
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.modal-comments::-webkit-scrollbar {
  width: 6px;
}

.modal-comments::-webkit-scrollbar-track {
  background: #2a2a2a;
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
  color: #fff;
}

.title-icon {
  font-size: 18px;
}

.comments-count {
  color: #666;
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
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.comment-avatar:hover {
  transform: scale(1.1);
}

.top-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  font-size: 14px;
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
  color: #fff;
}

.vip-badge {
  padding: 2px 8px;
  background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 100%);
  color: #fff;
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
  color: #a3e635;
}

.action-icon {
  font-size: 15px;
}

/* Responsive Design */
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