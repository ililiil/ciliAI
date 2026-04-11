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
        
        <!-- I Want to Create Button -->
        <div class="create-button-container">
          <el-button type="primary" class="create-button" @click="showTeacherQR">
            我要创作
          </el-button>
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

.create-button-container {
  margin-top: 16px;
  text-align: center;
}

.create-button {
  background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%);
  border: none;
  color: #1d1d1d;
  font-weight: 600;
  padding: 12px 32px;
  font-size: 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
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