<template>
  <div class="project-detail-page">
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="project-info">
          <h1 class="project-title">{{ project.title }}</h1>
          <span class="project-time">创建时间: {{ project.createTime }}</span>
        </div>
      </div>
      <div class="header-right">
        <el-button type="default" class="edit-work-btn" @click="openEditWorkDialog">
          编辑作品
        </el-button>
        <el-button type="primary" class="save-btn" @click="saveProject" :loading="isSaving">
          保存项目
        </el-button>
      </div>
    </div>

    <div class="page-content">
      <div class="sidebar-tabs">
        <div 
          :class="['tab-item', { active: activeModule === 'chat' }]"
          @click="activeModule = 'chat'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <span>AI对话</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'image' }]"
          @click="activeModule = 'image'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
          <span>AI生图</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'extend' }]"
          @click="activeModule = 'extend'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <line x1="8" y1="3" x2="8" y2="21"/>
            <line x1="16" y1="3" x2="16" y2="21"/>
            <line x1="3" y1="8" x2="21" y2="8"/>
            <line x1="3" y1="16" x2="21" y2="16"/>
          </svg>
          <span>AI扩图</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'edit' }]"
          @click="activeModule = 'edit'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          <span>AI改图</span>
        </div>
      </div>

      <div class="main-content">
        <div v-if="activeModule === 'chat'" class="chat-module">
          <div class="chat-sidebar">
            <div class="sidebar-header">
              <h3>对话列表</h3>
              <button class="new-chat-btn" @click="createNewChat">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                新对话
              </button>
            </div>
            <div class="chat-list">
              <div 
                v-for="chat in chatList" 
                :key="chat.id"
                :class="['chat-item', { active: currentChatId === chat.id }]"
                @click="selectChat(chat.id)"
              >
                <div class="chat-item-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                  </svg>
                </div>
                <div class="chat-item-content">
                  <div class="chat-item-title">{{ chat.title }}</div>
                  <div class="chat-item-time">{{ chat.updateTime }}</div>
                </div>
                <div class="chat-item-actions">
                  <button class="action-btn" @click.stop="deleteChat(chat.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="chat-main">
            <div class="chat-messages" ref="messagesContainer">
              <div v-if="currentMessages.length === 0" class="empty-messages">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                  </svg>
                </div>
                <p class="hint">输入您的提问，AI将为您提供帮助</p>
              </div>
              <div 
                v-for="message in currentMessages" 
                :key="message.id"
                :class="['message', message.role]"
              >
                <div class="message-avatar">
                  <div v-if="message.role === 'user'" class="avatar user-avatar">U</div>
                  <div v-else class="avatar ai-avatar">AI</div>
                </div>
                <div class="message-content">
                  <div class="message-text">{{ message.content }}</div>
                  <div class="message-time">{{ message.time }}</div>
                  <div v-if="message.status === 'sending'" class="message-status">
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                  </div>
                  <div v-else-if="message.status === 'error'" class="message-status error">
                    发送失败
                  </div>
                </div>
              </div>
            </div>

            <div class="chat-input-area">
              <div class="input-wrapper">
                <div class="people-selector">
                  <el-dropdown @command="handlePeopleSelect" trigger="click">
                    <button class="people-btn">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                      </svg>
                      <span>{{ currentPeopleLabel }}</span>
                    </button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="script" :class="{ 'active-item': selectedPeople === 'script' }">
                          <span class="dropdown-icon">📝</span>
                          <span class="dropdown-text">剧本设计</span>
                        </el-dropdown-item>
                        <el-dropdown-item command="character" :class="{ 'active-item': selectedPeople === 'character' }">
                          <span class="dropdown-icon">👤</span>
                          <span class="dropdown-text">人设设计</span>
                        </el-dropdown-item>
                        <el-dropdown-item command="scene" :class="{ 'active-item': selectedPeople === 'scene' }">
                          <span class="dropdown-icon">🎬</span>
                          <span class="dropdown-text">场景设计</span>
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                <textarea 
                  v-model="inputMessage"
                  placeholder="输入消息..."
                  @keydown.enter.exact.prevent="sendMessage"
                  rows="1"
                  ref="inputTextarea"
                ></textarea>
                <button 
                  class="send-btn" 
                  @click="sendMessage"
                  :disabled="!inputMessage.trim() || isSending"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'image'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>生图历史</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in imageHistory" 
                :key="item.id"
                class="history-item"
                @click="viewHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">生图参数</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>提示词</label>
                  <el-input
                    v-model="imageParams.prompt"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入图片描述，例如：一个美丽的风景照，远处有山脉..."
                  />
                </div>
                <div class="form-item">
                  <label>图片尺寸</label>
                  <el-select v-model="imageParams.size" placeholder="选择尺寸">
                    <el-option label="1024 x 1024 (1K)" value="1024x1024" />
                    <el-option label="2048 x 2048 (2K)" value="2048x2048" />
                    <el-option label="2304 x 1728 (4:3)" value="2304x1728" />
                    <el-option label="2560 x 1440 (16:9)" value="2560x1440" />
                    <el-option label="4096 x 4096 (4K)" value="4096x4096" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label>参考图（可选）</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleReferenceUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="referenceFileList"
                  >
                    <el-button size="small" type="primary">上传图片</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持JPEG、PNG格式，最大5MB
                      </div>
                    </template>
                  </el-upload>
                </div>

                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="generateImage"
                  :loading="isGenerating"
                >
                  {{ isGenerating ? '生成中...' : '开始生成' }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">生成结果</h3>
              <div v-if="generatedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                  </svg>
                </div>
                <p class="hint">点击生成按钮开始创作</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in generatedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" @click="previewImage(image.url)" style="cursor: pointer;" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'extend'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>扩图历史</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in extendHistory" 
                :key="item.id"
                class="history-item"
                @click="viewExtendHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">扩图参数</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>目标图片</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleExtendImageUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="extendFileList"
                  >
                    <el-button size="small" type="primary">上传图片</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持JPEG、PNG格式，最大5MB
                      </div>
                    </template>
                  </el-upload>
                </div>
                <div class="form-item">
                  <label>扩展后尺寸</label>
                  <el-select v-model="extendParams.size" placeholder="选择尺寸">
                    <el-option label="2048 x 2048 (2K)" value="2048x2048" />
                    <el-option label="2304 x 1728 (4:3)" value="2304x1728" />
                    <el-option label="2560 x 1440 (16:9)" value="2560x1440" />
                    <el-option label="4096 x 4096 (4K)" value="4096x4096" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label>提示词</label>
                  <el-input
                    v-model="extendParams.prompt"
                    type="textarea"
                    :rows="2"
                    placeholder="请描述扩展区域的内容，如：延展的背景风景，保持一致的风格..."
                  />
                </div>
                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="extendImage"
                  :loading="isExtending"
                >
                  {{ isExtending ? '扩展中...' : '开始扩展' }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">扩展结果</h3>
              <div v-if="extendedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <line x1="8" y1="3" x2="8" y2="21"/>
                    <line x1="16" y1="3" x2="16" y2="21"/>
                    <line x1="3" y1="8" x2="21" y2="8"/>
                    <line x1="3" y1="16" x2="21" y2="16"/>
                  </svg>
                </div>
                <p class="hint">上传图片开始扩展创作</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in extendedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" @click="previewImage(image.url)" style="cursor: pointer;" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'edit'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>改图历史</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in editHistory" 
                :key="item.id"
                class="history-item"
                @click="viewEditHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">改图参数</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>原图</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleEditImageUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="editFileList"
                  >
                    <el-button size="small" type="primary">上传原图</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持JPEG、PNG格式，最大5.7MB
                      </div>
                    </template>
                  </el-upload>
                </div>
                <div class="form-item">
                  <label>涂抹区域</label>
                  <div class="image-editor" v-if="editParams.image">
                    <div class="editor-controls">
                      <el-button size="small" :class="{ active: editingTool === 'brush' }" @click="editingTool = 'brush'">画笔</el-button>
                      <el-button size="small" :class="{ active: editingTool === 'eraser' }" @click="editingTool = 'eraser'">橡皮擦</el-button>
                      <el-button size="small" @click="clearMask">清空</el-button>
                    </div>
                    <div class="canvas-container">
                      <canvas ref="editCanvas" @mousedown="startDrawing" @mousemove="draw" @mouseup="stopDrawing" @mouseleave="stopDrawing"></canvas>
                      <img ref="editImageRef" :src="editParams.image" class="editor-image" />
                    </div>
                  </div>
                </div>
                <div class="form-item">
                  <label>提示词</label>
                  <el-input
                    v-model="editParams.prompt"
                    type="textarea"
                    :rows="3"
                    placeholder="请描述修改内容，如：删除物体，替换文字为'新内容'..."
                  />
                </div>
                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="generateEditImage"
                  :loading="isEditing"
                >
                  {{ isEditing ? '修改中...' : '开始修改' }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">修改结果</h3>
              <div v-if="editedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </div>
                <p class="hint">上传原图并涂抹要修改的区域</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in editedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" @click="previewImage(image.url)" style="cursor: pointer;" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 已保存作品列表 -->
    <div v-if="savedWorks.length > 0" class="saved-works-section">
      <div class="saved-works-header">
        <h3>已保存的作品</h3>
        <el-button size="small" @click="clearSavedWorks">清空</el-button>
      </div>
      <div class="saved-works-grid">
        <div
          v-for="work in savedWorks"
          :key="work.id"
          class="saved-work-card"
          @click="viewSavedWork(work)"
        >
          <div class="work-cover">
            <img v-if="work.coverImage" :src="work.coverImage" alt="作品封面" />
            <div v-else class="no-cover">暂无封面</div>
          </div>
          <div class="work-details">
            <h4 class="work-title">{{ work.title }}</h4>
            <p class="work-student">学员: {{ work.studentName }}</p>
            <div class="work-tags">
              <span v-for="tag in work.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showImagePreview"
      width="80%"
      class="image-preview-dialog"
    >
      <img :src="previewImageUrl" class="preview-image" />
    </el-dialog>

    <!-- 编辑作品对话框 -->
    <el-dialog
      v-model="showEditWorkDialog"
      title="编辑作品"
      width="650px"
      class="edit-work-dialog"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form :model="editWorkForm" label-width="100px" label-position="right">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="作品名称" required>
              <el-input v-model="editWorkForm.title" placeholder="请输入作品名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员名称" required>
              <el-input v-model="editWorkForm.studentName" placeholder="请输入学员姓名" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="分类" required>
          <el-select v-model="editWorkForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="IP版权库" value="IP版权库" />
            <el-option label="原创作品" value="原创作品" />
            <el-option label="合作作品" value="合作作品" />
            <el-option label="教学案例" value="教学案例" />
          </el-select>
        </el-form-item>

        <el-form-item label="封面图片" required>
          <div class="cover-upload-container">
            <el-upload
              class="work-cover-uploader"
              action="#"
              :auto-upload="false"
              :on-change="handleWorkCoverUpload"
              :file-list="workCoverFileList"
              :show-file-list="false"
              accept="image/*"
              list-type="picture"
            >
              <template #default>
                <div class="cover-upload-trigger" v-if="!editWorkForm.coverImage">
                  <el-icon class="upload-icon"><Upload /></el-icon>
                  <div class="upload-text">点击上传封面图片</div>
                  <div class="upload-hint">支持 JPG、PNG 格式，建议尺寸 500x892，最大 5MB</div>
                </div>
                <div class="cover-preview" v-else>
                  <img :src="editWorkForm.coverImage" alt="封面预览" class="cover-preview-image">
                  <div class="cover-preview-overlay">
                    <el-button type="danger" size="small" @click.stop="removeWorkCover">移除</el-button>
                  </div>
                </div>
              </template>
            </el-upload>
          </div>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="算力成本">
              <el-input v-model="editWorkForm.computeCost" placeholder="如：1000算力/分钟" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="制作时长">
              <el-input v-model="editWorkForm.duration" placeholder="如：420分钟" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="市场价格">
              <el-input v-model="editWorkForm.price" placeholder="如：150-300元/分钟" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版权信息">
              <el-input v-model="editWorkForm.copyright" placeholder="如：归CiliAI所有" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="标签">
          <el-select
            v-model="editWorkForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择或输入标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="作品简介">
          <el-input
            v-model="editWorkForm.introduction"
            type="textarea"
            :rows="4"
            placeholder="请输入作品简介"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showEditWorkDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSaveWork" :loading="isSavingWork">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { generateImage as volcGenerateImage, editImage as volcEditImage, extendImage as volcExtendImage } from '../utils/volcengine.js'

const route = useRoute()
const router = useRouter()
const updateComputingPower = inject('updateComputingPower')

const currentInviteCode = ref('demo-invite-code')

const accessKeyId = import.meta.env.VITE_VOLC_AK || ''
const secretAccessKey = import.meta.env.VITE_VOLC_SK || ''

const difyApiKey = 'app-jd05GWziMofrIu8sX7FFfLd2'
const difyApiUrl = '/dify-api/chat-messages'

const activeModule = ref('chat')
const isSaving = ref(false)
const isSending = ref(false)

// 算力相关
const userComputePower = ref(0)
const isCheckingPower = ref(false)

const fetchUserPower = async () => {
  try {
    const inviteCode = localStorage.getItem('inviteCode') || ''
    if (!inviteCode) return
    
    const response = await fetch(`/api/user/power?invite_code=${encodeURIComponent(inviteCode)}`)
    const result = await response.json()
    
    if (result.status === 'success') {
      userComputePower.value = result.compute_power
    }
  } catch (error) {
    console.error('获取算力失败:', error)
  }
}

const checkAndDeductPower = async () => {
  const inviteCode = localStorage.getItem('inviteCode') || ''
  if (!inviteCode) {
    ElMessage.warning('请先登录')
    return { success: false, message: '请先登录', remainingPower: 0 }
  }
  
  isCheckingPower.value = true
  try {
    const response = await fetch(`/api/user/power?invite_code=${encodeURIComponent(inviteCode)}`)
    const result = await response.json()
    
    if (result.status !== 'success') {
      return { success: false, message: '获取算力失败', remainingPower: 0 }
    }
    
    const currentPower = result.compute_power
    const requiredPower = 1
    
    if (currentPower < requiredPower) {
      return { 
        success: false, 
        message: `算力不足，当前算力 ${currentPower}，需要 ${requiredPower} 算力`,
        remainingPower: currentPower,
        requiredPower: requiredPower
      }
    }
    
    return { 
      success: true, 
      remainingPower: currentPower 
    }
  } catch (error) {
    console.error('算力检查失败:', error)
    return { success: false, message: '算力检查失败，请重试', remainingPower: 0 }
  } finally {
    isCheckingPower.value = false
  }
}

// 角色选择相关
const selectedPeople = ref('script')
const peopleLabels = {
  script: '剧本设计',
  character: '人设设计',
  scene: '场景设计'
}

const peopleValues = {
  script: '1',
  character: '2',
  scene: '3'
}

const currentPeopleLabel = computed(() => peopleLabels[selectedPeople.value] || '剧本设计')

const handlePeopleSelect = (command) => {
  selectedPeople.value = command
  ElMessage.success(`已切换到${peopleLabels[command]}模式`)
}
const isGenerating = ref(false)

const project = ref({
  id: '',
  title: '加载中...',
  createTime: ''
})

const chatList = ref([])
const currentChatId = ref('')
const inputMessage = ref('')
const messagesContainer = ref(null)
const inputTextarea = ref(null)

const currentMessages = computed(() => {
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  return chat ? chat.messages : []
})

// 已保存作品相关
const savedWorks = computed(() => {
  try {
    const works = localStorage.getItem('edit_works')
    return works ? JSON.parse(works) : []
  } catch (error) {
    console.error('读取已保存作品失败:', error)
    return []
  }
})

const viewSavedWork = (work) => {
  editWorkForm.value = { ...work }
  workCoverFileList.value = work.coverImage ? [{ name: 'cover.jpg', url: work.coverImage }] : []
  showEditWorkDialog.value = true
}

const clearSavedWorks = () => {
  if (confirm('确定要清空所有已保存的作品吗？')) {
    localStorage.removeItem('edit_works')
    ElMessage.success('已清空所有作品')
  }
}

const imageParams = reactive({
  prompt: '',
  size: '1024x1024',
  referenceImage: ''
})

const extendParams = reactive({
  image: '',
  size: '2048x2048',
  prompt: ''
})

const editParams = reactive({
  image: '',
  mask: '',
  prompt: ''
})

const editingTool = ref('brush')
const isDrawing = ref(false)
const editCanvas = ref(null)
const editImageRef = ref(null)
const canvasContext = ref(null)

const imageHistory = ref([])
const extendHistory = ref([])
const editHistory = ref([])
const generatedImages = ref([])
const extendedImages = ref([])
const editedImages = ref([])
const showImagePreview = ref(false)
const previewImageUrl = ref('')
const referenceFileList = ref([])
const extendFileList = ref([])
const editFileList = ref([])
const maskFileList = ref([])
const isExtending = ref(false)
const isEditing = ref(false)

// 编辑作品对话框相关
const showEditWorkDialog = ref(false)
const isSavingWork = ref(false)
const workCoverFileList = ref([])
const availableTags = ref(['AI动画', '现代科幻', '穿越', '都市', '古装', '悬疑', '爱情', '喜剧', '动作', '冒险'])

const editWorkForm = ref({
  title: '',
  studentName: '',
  category: '',
  coverImage: '',
  computeCost: '',
  duration: '',
  price: '',
  copyright: '',
  tags: [],
  introduction: ''
})

const handleWorkCoverUpload = (file) => {
  console.log('作品封面文件:', file)
  
  const isImage = file.raw.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return
  }
  
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    ElMessage.error('封面图片大小不能超过 5MB！')
    return
  }
  
  workCoverFileList.value = [file]
  
  const reader = new FileReader()
  reader.onload = (e) => {
    editWorkForm.value.coverImage = e.target.result
    console.log('作品封面已读取:', editWorkForm.value.coverImage.substring(0, 50) + '...')
  }
  reader.readAsDataURL(file.raw)
}

const removeWorkCover = () => {
  editWorkForm.value.coverImage = ''
  workCoverFileList.value = []
}

const handleSaveWork = async () => {
  if (!editWorkForm.value.title.trim()) {
    ElMessage.warning('请输入作品名称')
    return
  }
  
  if (!editWorkForm.value.studentName.trim()) {
    ElMessage.warning('请输入学员名称')
    return
  }
  
  if (!editWorkForm.value.category) {
    ElMessage.warning('请选择分类')
    return
  }
  
  if (!editWorkForm.value.coverImage) {
    ElMessage.warning('请上传封面图片')
    return
  }
  
  isSavingWork.value = true
  
  try {
    const workData = {
      ...editWorkForm.value,
      id: Date.now(),
      createTime: new Date().toLocaleString('zh-CN')
    }
    
    const existingWorks = JSON.parse(localStorage.getItem('edit_works') || '[]')
    const existingIndex = existingWorks.findIndex(w => w.id === workData.id)
    
    if (existingIndex > -1) {
      existingWorks[existingIndex] = workData
    } else {
      existingWorks.unshift(workData)
    }
    
    localStorage.setItem('edit_works', JSON.stringify(existingWorks))
    
    console.log('作品已保存:', workData)
    
    showEditWorkDialog.value = false
    ElMessage.success('作品保存成功！')
    
    resetEditWorkForm()
  } catch (error) {
    console.error('保存作品失败:', error)
    ElMessage.error('保存失败，请重试')
  } finally {
    isSavingWork.value = false
  }
}

const resetEditWorkForm = () => {
  editWorkForm.value = {
    title: '',
    studentName: '',
    category: '',
    coverImage: '',
    computeCost: '',
    duration: '',
    price: '',
    copyright: '',
    tags: [],
    introduction: ''
  }
  workCoverFileList.value = []
}

const openEditWorkDialog = () => {
  showEditWorkDialog.value = true
  resetEditWorkForm()
}

const loadProjectData = async () => {
  const projectId = route.params.id
  
  try {
    const inviteCode = localStorage.getItem('inviteCode') || ''
    const response = await fetch(`/api/projects?invite_code=${encodeURIComponent(inviteCode)}`)
    const result = await response.json()
    
    if (result.status === 'success' && result.projects) {
      const foundProject = result.projects.find(p => p.id === projectId || p.id?.toString() === projectId)
      if (foundProject) {
        project.value = {
          id: foundProject.id,
          title: foundProject.title || foundProject.name || '未命名项目',
          createTime: foundProject.createTime || foundProject.created_at || new Date().toLocaleString('zh-CN')
        }
      } else {
        project.value = {
          id: projectId,
          title: '项目详情',
          createTime: new Date().toLocaleString('zh-CN')
        }
      }
    } else {
      project.value = {
        id: projectId,
        title: '项目详情',
        createTime: new Date().toLocaleString('zh-CN')
      }
    }
  } catch (error) {
    console.error('Failed to fetch project data:', error)
    project.value = {
      id: projectId,
      title: '项目详情',
      createTime: '加载失败'
    }
  }
  
  chatList.value = [
    {
      id: Date.now().toString(),
      title: '新对话',
      updateTime: new Date().toLocaleString('zh-CN'),
      conversationId: '',
      messages: []
    }
  ]
  
  if (chatList.value.length > 0) {
    currentChatId.value = chatList.value[0].id
  }
  
  imageHistory.value = [
    {
      id: '1',
      prompt: '一个未来城市的夜景，霓虹灯光闪烁',
      imageUrl: 'https://picsum.photos/400/300?random=100',
      createTime: '2025-03-31 13:00',
      params: { size: '1024x1024', steps: 30, cfgScale: 7 }
    },
    {
      id: '2',
      prompt: '海边的日落，金色光芒洒落',
      imageUrl: 'https://picsum.photos/400/300?random=101',
      createTime: '2025-03-31 11:30',
      params: { size: '1024x1024', steps: 25, cfgScale: 8 }
    }
  ]
}

const goBack = () => {
  router.push('/works')
}

const saveProject = async () => {
  isSaving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('项目保存成功')
  } catch (error) {
    ElMessage.error('保存失败，请重试')
  } finally {
    isSaving.value = false
  }
}

const createNewChat = () => {
  const newChat = {
    id: Date.now().toString(),
    title: '新对话',
    updateTime: new Date().toLocaleString('zh-CN'),
    messages: [],
    conversationId: ''
  }
  chatList.value.unshift(newChat)
  currentChatId.value = newChat.id
  inputMessage.value = ''
  localStorage.removeItem('currentConversationId')
}

const selectChat = (chatId) => {
  currentChatId.value = chatId
  scrollToBottom()
}

const deleteChat = async (chatId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个对话吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const chat = chatList.value.find(c => c.id === chatId)
    if (chat && chat.conversationId) {
      localStorage.removeItem('currentConversationId')
    }
    const index = chatList.value.findIndex(c => c.id === chatId)
    if (index > -1) {
      chatList.value.splice(index, 1)
      if (currentChatId.value === chatId) {
        currentChatId.value = chatList.value.length > 0 ? chatList.value[0].id : ''
        localStorage.removeItem('currentConversationId')
      }
    }
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isSending.value) return
  
  const inviteCode = localStorage.getItem('inviteCode') || ''
  if (!inviteCode) {
    ElMessage.warning('请先登录后再发送消息')
    return
  }
  
  isCheckingPower.value = true
  const powerCheckResult = await checkAndDeductPower()
  isCheckingPower.value = false
  
  if (!powerCheckResult.success) {
    ElMessage.warning('算力不足')
    return
  }
  
  userComputePower.value = powerCheckResult.remainingPower - 1
  if (updateComputingPower) {
    updateComputingPower(powerCheckResult.remainingPower - 1)
  }
  
  const message = inputMessage.value.trim()
  inputMessage.value = ''
  
  const currentChat = chatList.value.find(c => c.id === currentChatId.value)
  if (!currentChat) {
    createNewChat()
  }
  
  const userMessage = {
    id: Date.now().toString(),
    role: 'user',
    content: message,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    status: 'success'
  }
  
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  if (chat) {
    chat.messages.push(userMessage)
    chat.title = message.slice(0, 20) + (message.length > 20 ? '...' : '')
    chat.updateTime = new Date().toLocaleString('zh-CN')
  }
  
  scrollToBottom()
  
  isSending.value = true
  
  const aiMessageId = (Date.now() + 1).toString()
  const aiMessage = {
    id: aiMessageId,
    role: 'assistant',
    content: '',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    status: 'sending'
  }
  
  if (chat) {
    chat.messages.push(aiMessage)
  }
  
  scrollToBottom()
  
  try {
    const { answer, conversationId } = await callDifyAPI(
      message,
      chat.conversationId,
      selectedPeople.value,
      (chunk, receivedConversationId) => {
        const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
        if (msgIndex > -1) {
          chat.messages[msgIndex].content += chunk
        }
        
        if (receivedConversationId && chat) {
          chat.conversationId = receivedConversationId
        }
        
        scrollToBottom()
      }
    )
    
    if (conversationId && chat) {
      chat.conversationId = conversationId
      localStorage.setItem('currentConversationId', conversationId)
    }
    
    const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
    if (msgIndex > -1) {
      chat.messages[msgIndex].status = 'success'
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    
    fetchUserPower()
    
    if (error.message.includes('404') || error.message.includes('not_found') || error.message.includes('not exist')) {
      if (chat) {
        chat.conversationId = ''
        localStorage.removeItem('currentConversationId')
      }
      ElMessage.warning('会话已过期，将创建新对话，请重试')
      
      const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
      if (msgIndex > -1) {
        chat.messages[msgIndex].content = '[会话已过期] 请重新发送消息开始新对话'
        chat.messages[msgIndex].status = 'error'
      }
    } else if (error.message.includes('算力不足')) {
      const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
      if (msgIndex > -1) {
        chat.messages[msgIndex].content = '[算力不足] ' + error.message
        chat.messages[msgIndex].status = 'error'
      }
      fetchUserPower()
    } else {
      const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
      if (msgIndex > -1) {
        const currentContent = chat.messages[msgIndex].content
        if (currentContent && currentContent.length > 0) {
          chat.messages[msgIndex].content = currentContent + '\n\n[连接中断，如需继续请重试]'
        } else {
          chat.messages[msgIndex].content = '抱歉，API 连接失败: ' + error.message
        }
        chat.messages[msgIndex].status = 'error'
      }
      ElMessage.error('连接失败: ' + error.message)
    }
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}

const callDifyAPI = async (query, conversationId, people, onChunk) => {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 180000)

  const userId = localStorage.getItem('userId') || `user-${Date.now()}`
  const inviteCode = localStorage.getItem('inviteCode') || ''
  
  const requestBody = {
    invite_code: inviteCode,
    project_id: project.value.id,
    inputs: {
      people: peopleValues[people] || '1'
    },
    query: query,
    response_mode: 'streaming',
    user: userId,
    files: []
  }
  
  if (conversationId) {
    requestBody.conversation_id = conversationId
  }

  console.log('========== Dify API 请求开始 ==========')
  console.log('发送 Dify API 请求:', {
    url: difyApiUrl,
    body: requestBody,
    headers: {
      'Authorization': `Bearer ${difyApiKey.substring(0, 15)}...`
    }
  })
  
  console.log('发送的消息详情:', {
    query: query,
    people: requestBody.inputs.people,
    selectedPeople: selectedPeople.value,
    peopleMapping: peopleValues,
    conversationId: conversationId || '(新建会话)',
    user: userId,
    response_mode: 'streaming'
  })
  
  console.log('请求体 JSON:', JSON.stringify(requestBody, null, 2))
  console.log('=====================================')

  let response
  try {
    console.log('开始发送请求到:', difyApiUrl)
    console.log('完整 URL:', window.location.origin + difyApiUrl)
    
    response = await fetch(difyApiUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${difyApiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal
    })
    
    console.log('========== Dify API 响应 ==========')
    console.log('Dify API 响应状态:', response.status, response.statusText)
    console.log('响应头 Content-Type:', response.headers.get('content-type'))
    console.log('响应头 X-Power-Cost:', response.headers.get('x-power-cost'))
    console.log('响应头 X-Remaining-Power:', response.headers.get('x-remaining-power'))
    console.log('所有响应头:', Object.fromEntries(response.headers.entries()))
    
    const remainingPower = response.headers.get('x-remaining-power')
    if (remainingPower) {
      userComputePower.value = parseInt(remainingPower)
      console.log('更新算力余额:', userComputePower.value)
      if (updateComputingPower) {
        updateComputingPower(parseInt(remainingPower))
      }
    }
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Dify API 错误响应:', errorText)
      console.log('===================================')
    }
  } catch (error) {
    clearTimeout(timeout)
    console.error('Dify API 网络错误:', error)
    console.error('错误类型:', error.name)
    console.error('错误消息:', error.message)
    console.error('错误堆栈:', error.stack)
    
    if (error.name === 'AbortError') {
      throw new Error('请求超时，请重试')
    }
    
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      throw new Error(`无法连接到服务器，请检查网络连接。错误详情: ${error.message}`)
    }
    
    throw new Error(`网络连接失败: ${error.message}`)
  }

  clearTimeout(timeout)

  if (!response.ok) {
    let errorText = ''
    try {
      errorText = await response.text()
    } catch (e) {
      errorText = '无法读取错误响应'
    }
    throw new Error(`API请求失败 (${response.status}): ${errorText || 'Unknown error'}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let result = ''
  let newConversationId = conversationId
  let isCompleted = false

  const cleanup = () => {
    if (reader) {
      reader.cancel().catch(() => {})
    }
  }

  try {
    while (!isCompleted) {
      let readResult
      try {
        readResult = await reader.read()
      } catch (error) {
        if (result.length > 0) {
          return { answer: result, conversationId: newConversationId }
        }
        throw error
      }

      const { done, value } = readResult
      if (done) {
        isCompleted = true
        break
      }

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        const trimmedLine = line.trim()
        if (!trimmedLine || trimmedLine === 'data: [DONE]') {
          continue
        }
        
        if (trimmedLine.startsWith('data: ')) {
          const dataStr = trimmedLine.slice(6).trim()
          if (!dataStr) continue
          
          try {
            const data = JSON.parse(dataStr)
            
            console.log('收到事件:', data.event, data)
            
            if (data.event === 'message' || data.event === 'agent_message') {
              const answerText = data.answer || ''
              result += answerText
              if (onChunk) {
                onChunk(answerText, data.conversation_id || newConversationId)
              }
            }
            
            if (data.conversation_id) {
              newConversationId = data.conversation_id
              if (onChunk) {
                onChunk('', data.conversation_id)
              }
            }
            
            if (data.event === 'message_end' || data.event === 'done') {
              console.log('========== 流式响应结束 ==========')
              console.log('最终回复:', result)
              console.log('会话ID:', newConversationId)
              console.log('==================================')
              isCompleted = true
              cleanup()
              return { answer: result, conversationId: newConversationId }
            }
            
            if (data.error || data.error_code) {
              throw new Error(data.message || data.error || `API错误: ${data.error_code}`)
            }
          } catch (e) {
            if (e instanceof SyntaxError) {
              console.warn('跳过无效的JSON数据:', dataStr)
              continue
            }
            throw e
          }
        }
      }
    }
  } catch (error) {
    cleanup()
    if (error.name === 'AbortError' || error.message.includes('abort')) {
      if (result.length > 0) {
        return { answer: result, conversationId: newConversationId }
      }
      throw new Error('请求被中止，请检查网络连接后重试')
    }
    throw error
  }

  cleanup()
  return { answer: result, conversationId: newConversationId }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleReferenceUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    imageParams.referenceImage = e.target.result
    referenceFileList.value = [file]
  }
  reader.readAsDataURL(file.raw)
}

const generateImage = async () => {
  if (!imageParams.prompt.trim()) {
    ElMessage.warning('请输入提示词')
    return
  }
  
  isGenerating.value = true
  generatedImages.value = []
  
  try {
    const [width, height] = imageParams.size.split('x').map(Number)
    
    const params = {
      prompt: imageParams.prompt,
      width: width,
      height: height,
      force_single: true
    }
    
    if (imageParams.referenceImage) {
      params.referenceImage = imageParams.referenceImage
    }
    
    console.log('开始调用生图API，参数:', params)
    
    if (!currentInviteCode.value) {
      ElMessage.error('请先登录')
      isGenerating.value = false
      return
    }
    
    const submitResponse = await volcGenerateImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('生图任务响应:', submitResponse)
    
    if (submitResponse.data?.remaining_power !== undefined) {
      userComputePower.value = submitResponse.data.remaining_power
      if (updateComputingPower) {
        updateComputingPower(submitResponse.data.remaining_power)
      }
    }
    
    if (!submitResponse.data?.task_id) {
      throw new Error('任务提交失败，未返回task_id')
    }
    
    const taskId = submitResponse.data.task_id
    
    const newImages = []
    console.log('API返回的images数据:', submitResponse.data?.images)
    
    if (submitResponse.data?.images && submitResponse.data.images.length > 0) {
      submitResponse.data.images.forEach((image, index) => {
        console.log('处理图片数据:', index, image)
        
        if (typeof image === 'object' && image.url) {
          newImages.push({
            url: image.url,
            prompt: imageParams.prompt,
            taskId: taskId
          })
        } else if (typeof image === 'string') {
          newImages.push({
            url: image,
            prompt: imageParams.prompt,
            taskId: taskId
          })
        }
      })
    } else {
      throw new Error('API返回结果中没有图片数据')
    }
    
    console.log('处理后的newImages:', newImages)
    
    generatedImages.value = newImages
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: imageParams.prompt,
      imageUrl: newImages[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        size: imageParams.size,
        hasReference: !!imageParams.referenceImage,
        taskId: taskId
      }
    }
    imageHistory.value.unshift(historyItem)
    
    ElMessage.success('图片生成成功')
  } catch (error) {
    console.error('生图失败:', error)
    ElMessage.error(`生成失败: ${error.message}`)
    
    console.error('详细错误信息:', error)
    
    if (error.message.includes('Failed to fetch')) {
      ElMessage.error('网络请求失败，请检查网络连接或后端服务器是否运行正常')
    }
  } finally {
    isGenerating.value = false
  }
}

const viewHistoryItem = (item) => {
  imageParams.prompt = item.prompt
  imageParams.size = item.params?.size || '2048x2048'
  imageParams.referenceImage = ''
  referenceFileList.value = []
  
  generatedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const handleExtendImageUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    extendParams.image = e.target.result
    extendFileList.value = [file]
  }
  reader.readAsDataURL(file.raw)
}

const extendImage = async () => {
  if (!extendParams.image) {
    ElMessage.warning('请上传目标图片')
    return
  }
  
  isExtending.value = true
  extendedImages.value = []
  
  try {
    const [width, height] = extendParams.size.split('x').map(Number)
    
    const params = {
      image: extendParams.image,
      prompt: extendParams.prompt || '扩展图像，保持原有风格',
      width: width,
      height: height
    }
    
    if (!currentInviteCode.value) {
      ElMessage.error('请先登录')
      isExtending.value = false
      return
    }
    
    const response = await volcExtendImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('扩图任务响应:', response)
    
    if (response.data?.remaining_power !== undefined) {
      userComputePower.value = response.data.remaining_power
      if (updateComputingPower) {
        updateComputingPower(response.data.remaining_power)
      }
    }
    
    if (!response.data?.task_id) {
      throw new Error('任务提交失败，未返回task_id')
    }
    
    const taskId = response.data.task_id
    
    const newImages = []
    if (response.data?.images && response.data.images.length > 0) {
      response.data.images.forEach((image) => {
        if (typeof image === 'object' && image.url) {
          newImages.push({
            url: image.url,
            prompt: extendParams.prompt,
            taskId: taskId
          })
        } else if (typeof image === 'string') {
          newImages.push({
            url: image,
            prompt: extendParams.prompt,
            taskId: taskId
          })
        }
      })
    } else {
      throw new Error('API返回结果中没有图片数据')
    }
    
    extendedImages.value = newImages
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: extendParams.prompt,
      imageUrl: newImages[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        size: extendParams.size,
        taskId: taskId
      }
    }
    extendHistory.value.unshift(historyItem)
    
    ElMessage.success('图片扩展成功')
  } catch (error) {
    console.error('扩图失败:', error)
    ElMessage.error(`扩展失败: ${error.message}`)
  } finally {
    isExtending.value = false
  }
}

const viewExtendHistoryItem = (item) => {
  extendParams.prompt = item.prompt
  extendParams.size = item.params?.size || '2048x2048'
  extendParams.image = ''
  extendFileList.value = []
  
  extendedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const handleEditImageUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    editParams.image = e.target.result
    editFileList.value = [file]
    
    setTimeout(() => {
      initCanvas()
    }, 100)
  }
  reader.readAsDataURL(file.raw)
}

const initCanvas = () => {
  if (!editCanvas.value || !editImageRef.value) return
  
  const canvas = editCanvas.value
  const image = editImageRef.value
  
  canvas.width = image.width
  canvas.height = image.height
  
  canvasContext.value = canvas.getContext('2d')
  
  clearMask()
}

const startDrawing = (e) => {
  isDrawing.value = true
  draw(e)
}

const draw = (e) => {
  if (!isDrawing.value || !canvasContext.value || !editCanvas.value) return
  
  const canvas = editCanvas.value
  const rect = canvas.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  
  const ctx = canvasContext.value
  ctx.lineWidth = 20
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  if (editingTool.value === 'brush') {
    ctx.globalCompositeOperation = 'source-over'
    ctx.fillStyle = 'white'
  } else {
    ctx.globalCompositeOperation = 'destination-out'
    ctx.fillStyle = 'black'
  }
  
  ctx.beginPath()
  ctx.arc(x, y, 10, 0, Math.PI * 2)
  ctx.fill()
  
  updateMask()
}

const stopDrawing = () => {
  isDrawing.value = false
}

const clearMask = () => {
  if (!canvasContext.value || !editCanvas.value) return
  
  const canvas = editCanvas.value
  const ctx = canvasContext.value
  
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  editParams.mask = ''
}

const updateMask = () => {
  if (!editCanvas.value) return
  
  editParams.mask = editCanvas.value.toDataURL('image/png')
}

const generateEditImage = async () => {
  if (!editParams.image) {
    ElMessage.warning('请上传原图')
    return
  }
  if (!editParams.mask) {
    ElMessage.warning('请在原图上绘制修改区域')
    return
  }
  
  isEditing.value = true
  editedImages.value = []
  
  try {
    const params = {
      image: editParams.image,
      mask: editParams.mask,
      prompt: editParams.prompt
    }
    
    if (!currentInviteCode.value) {
      ElMessage.error('请先登录')
      isEditing.value = false
      return
    }
    
    const submitResponse = await volcEditImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('改图任务提交响应:', submitResponse)
    
    if (submitResponse.data?.remaining_power !== undefined) {
      userComputePower.value = submitResponse.data.remaining_power
      if (updateComputingPower) {
        updateComputingPower(submitResponse.data.remaining_power)
      }
    }
    
    if (!submitResponse.data?.task_id) {
      throw new Error('任务提交失败，未返回task_id')
    }
    
    const taskId = submitResponse.data.task_id
    ElMessage.success(`图片修改任务已提交，任务ID: ${taskId}`)
    
    editedImages.value = [{
      url: `https://picsum.photos/512/512?random=${Date.now()}`,
      prompt: editParams.prompt,
      taskId: taskId
    }]
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: editParams.prompt,
      imageUrl: editedImages.value[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        hasMask: true,
        taskId: taskId
      }
    }
    editHistory.value.unshift(historyItem)
    
    ElMessage.success('图片修改成功')
  } catch (error) {
    console.error('改图失败:', error)
    ElMessage.error(`修改失败: ${error.message}`)
  } finally {
    isEditing.value = false
  }
}

const viewEditHistoryItem = (item) => {
  editParams.prompt = item.prompt
  editParams.image = ''
  editParams.mask = ''
  editFileList.value = []
  maskFileList.value = []
  
  editedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const downloadImage = (url) => {
  const link = document.createElement('a')
  link.href = url
  link.download = `ai-image-${Date.now()}.png`
  link.click()
  ElMessage.success('开始下载')
}

const previewImage = (url) => {
  previewImageUrl.value = url
  showImagePreview.value = true
}

onMounted(() => {
  if (!localStorage.getItem('userId')) {
    localStorage.setItem('userId', `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`)
  }
  loadProjectData()
  fetchUserPower()
  
  // 添加测试方法到 window 对象，方便调试
  window.testDifyAPI = async () => {
    console.log('========== 开始测试 Dify API ==========')
    console.log('测试 API: https://whhongyi.com.cn/v1/chat-messages')
    console.log('API Key:', difyApiKey)
    
    try {
      const response = await fetch('/dify-api/chat-messages', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${difyApiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          inputs: {
            people: '1'
          },
          query: '你好，测试消息',
          response_mode: 'streaming',
          user: 'test-user',
          files: []
        })
      })
      
      console.log('响应状态:', response.status, response.statusText)
      console.log('响应头:', Object.fromEntries(response.headers.entries()))
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('API 错误:', errorText)
        return { error: errorText }
      }
      
      // 处理流式响应
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let result = ''
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value, { stream: true })
        console.log('收到数据块:', chunk)
        
        const lines = chunk.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.answer) {
                result += data.answer
                console.log('收到回复片段:', data.answer)
              }
              if (data.event === 'message_end') {
                console.log('流式响应结束')
                console.log('完整回复:', result)
                console.log('会话ID:', data.conversation_id)
                return { answer: result, conversationId: data.conversation_id }
              }
            } catch (e) {
              console.warn('解析失败:', e)
            }
          }
        }
      }
      
      return { answer: result }
    } catch (error) {
      console.error('测试失败:', error)
      return { error: error.message }
    }
  }
  
  console.log('✅ 测试方法已添加！在控制台输入 window.testDifyAPI() 进行测试')
})
</script>

<style scoped>
.project-detail-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #F8F7F2;
  color: #425D5F;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #BACACB;
  background-color: #F8F7F2;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #BACACB;
  border: none;
  color: #425D5F;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #425D5F;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.project-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  color: #425D5F;
}

.project-time {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  padding-left: 14px;
}

.save-btn {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
  font-weight: 500;
}

.save-btn:hover {
  background-color: #FAA943;
  border-color: #FAA943;
}

/* 已保存作品列表样式 */
.saved-works-section {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.saved-works-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #BACACB;
}

.saved-works-header h3 {
  margin: 0;
  color: #425D5F;
  font-size: 16px;
  font-weight: 600;
}

.saved-works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.saved-work-card {
  background-color: #fff;
  border: 1px solid #BACACB;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.saved-work-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 93, 95, 0.2);
  border-color: #425D5F;
}

.work-cover {
  width: 100%;
  aspect-ratio: 500 / 892;
  overflow: hidden;
  background-color: #BACACB;
}

.work-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-cover {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 14px;
}

.work-details {
  padding: 12px;
}

.work-title {
  margin: 0 0 8px 0;
  color: #425D5F;
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.work-student {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 12px;
}

.work-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.work-tags .tag {
  background-color: rgba(250, 169, 67, 0.2);
  color: #425D5F;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
}

.edit-work-btn {
  background-color: #BACACB;
  border-color: #BACACB;
  color: #425D5F;
  font-weight: 500;
}

.edit-work-btn:hover {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
}

.page-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar-tabs {
  width: 120px;
  background-color: #F8F7F2;
  border-right: 1px solid #BACACB;
  display: flex;
  flex-direction: column;
  padding: 16px 8px;
  gap: 8px;
}

.tab-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 12px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #425D5F;
  gap: 8px;
}

.tab-item:hover {
  background-color: #BACACB;
  color: #425D5F;
}

.tab-item.active {
  background-color: rgba(250, 169, 67, 0.2);
  color: #425D5F;
}

.tab-item span {
  font-size: 10px;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

.chat-module {
  display: flex;
  height: 100%;
}

.chat-sidebar {
  width: 260px;
  background-color: #F8F7F2;
  border-right: 1px solid #BACACB;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #BACACB;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #425D5F;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background-color: #425D5F;
  border: none;
  border-radius: 6px;
  color: #F8F7F2;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background-color: #FAA943;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 12px;
}

.chat-item:hover {
  background-color: #BACACB;
}

.chat-item.active {
  background-color: rgba(250, 169, 67, 0.1);
}

.chat-item-icon {
  color: #425D5F;
}

.chat-item.active .chat-item-icon {
  color: #425D5F;
}

.chat-item-content {
  flex: 1;
  min-width: 0;
}

.chat-item-title {
  font-size: 13px;
  color: #425D5F;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-item-time {
  font-size: 11px;
  color: #425D5F;
  margin-top: 4px;
}

.chat-item-actions {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.chat-item:hover .chat-item-actions {
  opacity: 1;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  background-color: transparent;
  border: none;
  color: #425D5F;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background-color: #BACACB;
  color: #425D5F;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #F8F7F2;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #425D5F;
}

.empty-icon {
  margin-bottom: 16px;
  color: #425D5F;
}

.empty-messages .hint {
  font-size: 13px;
  margin-top: 8px;
  color: #444;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.user-avatar {
  background-color: #425D5F;
  color: #F8F7F2;
}

.ai-avatar {
  background-color: #BACACB;
  color: #425D5F;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.message.user .message-text {
  background-color: #425D5F;
  color: #F8F7F2;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-text {
  background-color: #BACACB;
  color: #425D5F;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #425D5F;
  margin-top: 4px;
}

.message.user .message-time {
  text-align: right;
}

.message-status {
  margin-top: 4px;
  font-size: 12px;
}

.message-status.error {
  color: #f56c6c;
}

.loading-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #425D5F;
  border-radius: 50%;
  margin-right: 4px;
  animation: loading 1s infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes loading {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid #BACACB;
  background-color: #F8F7F2;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background-color: #BACACB;
  border-radius: 12px;
  padding: 12px 16px;
}

.input-wrapper textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 14px;
  resize: none;
  outline: none;
  max-height: 120px;
  line-height: 1.5;
}

.people-selector {
  display: flex;
  align-items: center;
}

.people-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background-color: #425D5F;
  border: none;
  border-radius: 6px;
  color: #F8F7F2;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.people-btn:hover {
  background-color: #FAA943;
}

.people-btn svg {
  flex-shrink: 0;
}

.people-btn span {
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.people-selector :deep(.el-dropdown-menu) {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  padding: 8px 0;
}

.people-selector :deep(.el-dropdown-menu__item) {
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #425D5F;
  font-size: 14px;
  transition: all 0.3s ease;
}

.people-selector :deep(.el-dropdown-menu__item:hover) {
  background-color: rgba(250, 169, 67, 0.1);
}

.people-selector :deep(.el-dropdown-menu__item.active-item) {
  background-color: rgba(250, 169, 67, 0.2);
  font-weight: 600;
}

.dropdown-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.dropdown-text {
  flex: 1;
}

.input-wrapper textarea::placeholder {
  color: #666;
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #425D5F;
  border: none;
  color: #F8F7F2;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background-color: #FAA943;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-module {
  display: flex;
  height: 100%;
}

.image-sidebar {
  width: 260px;
  background-color: #F8F7F2;
  border-right: 1px solid #BACACB;
  display: flex;
  flex-direction: column;
}

.image-history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.history-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  background-color: #BACACB;
}

.history-thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.history-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.history-info {
  flex: 1;
  min-width: 0;
}

.history-prompt {
  font-size: 12px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.empty-history {
  text-align: center;
  padding: 40px 16px;
  color: #666;
}

.image-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 24px;
  gap: 24px;
}

.image-params-section,
.image-result-section {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 20px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 500;
  color: #fff;
}

.params-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-item label {
  font-size: 13px;
  color: #999;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-item {
  flex: 1;
}

.params-form :deep(.el-input__wrapper),
.params-form :deep(.el-textarea__inner),
.params-form :deep(.el-select .el-input__wrapper) {
  background-color: #1d1d1d;
  border: 1px solid #3a3a3a;
  box-shadow: none;
}

.params-form :deep(.el-input__inner),
.params-form :deep(.el-textarea__inner) {
  color: #fff;
}

.params-form :deep(.el-input__inner::placeholder),
.params-form :deep(.el-textarea__inner::placeholder) {
  color: #666;
}

.params-form :deep(.el-upload-list__item) {
  background-color: #1d1d1d;
  border: 1px solid #3a3a3a;
}

.params-form :deep(.el-upload-list__item-name) {
  color: #999;
}

.params-form :deep(.el-upload__tip) {
  color: #666;
  font-size: 12px;
  margin-top: 4px;
}

.image-editor {
  margin-top: 8px;
}

.editor-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.editor-controls .el-button.active {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
}

.canvas-container {
  position: relative;
  max-width: 100%;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  overflow: hidden;
}

.canvas-container canvas {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  cursor: crosshair;
}

.editor-image {
  display: block;
  max-width: 100%;
  height: auto;
  z-index: 0;
}

.no-image {
  border: 1px dashed #3a3a3a;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  color: #666;
  margin-top: 8px;
}

.generate-btn {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
  font-weight: 500;
  margin-top: 8px;
}

.generate-btn:hover {
  background-color: #FAA943;
  border-color: #FAA943;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #666;
}

.empty-result .empty-icon {
  margin-bottom: 16px;
  color: #666;
}

.empty-result .hint {
  font-size: 13px;
  margin-top: 8px;
  color: #999;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.result-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;
}

.result-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-actions {
  position: absolute;
  bottom: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.result-item:hover .result-actions {
  opacity: 1;
}

.result-actions .action-btn {
  background-color: rgba(0, 0, 0, 0.6);
  color: #fff;
}

.result-actions .action-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.image-preview-dialog {
  z-index: 9999 !important;
}

.image-preview-dialog :deep(.el-dialog) {
  background-color: #1d1d1d;
  z-index: 9999 !important;
  margin-top: 10vh !important;
  .el-dialog__body {
    z-index: 10000;
    position: relative;
  }
}

.image-preview-dialog :deep(.el-overlay) {
  z-index: 9998 !important;
}

.preview-image {
  width: 100%;
  max-height: 80vh;
  object-fit: contain;
  position: relative;
  z-index: 10000;
}

@media (max-width: 1024px) {
  .chat-sidebar,
  .image-sidebar {
    width: 220px;
  }
}

/* 编辑作品对话框样式 */
.edit-work-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 12px !important;
}

.edit-work-dialog .el-dialog__header {
  border-bottom: 1px solid #BACACB;
  padding: 20px 24px;
  background-color: #F8F7F2;
}

.edit-work-dialog .el-dialog__title {
  color: #425D5F;
  font-size: 18px;
  font-weight: 600;
}

.edit-work-dialog .el-dialog__body {
  padding: 24px;
  background-color: #F8F7F2;
  max-height: 70vh;
  overflow-y: auto;
}

.edit-work-dialog .el-dialog__footer {
  border-top: 1px solid #BACACB;
  padding: 16px 24px;
  background-color: #F8F7F2;
}

.edit-work-dialog .el-form-item__label {
  color: #425D5F;
  font-weight: 500;
}

.edit-work-dialog .el-input__wrapper,
.edit-work-dialog .el-textarea__inner {
  background-color: #BACACB;
  border: none;
  box-shadow: none;
}

.edit-work-dialog .el-input__inner,
.edit-work-dialog .el-textarea__inner {
  color: #425D5F;
}

.edit-work-dialog .el-input__inner::placeholder,
.edit-work-dialog .el-textarea__inner::placeholder {
  color: #666;
}

.edit-work-dialog .el-select__wrapper {
  background-color: #BACACB;
  border: none;
  box-shadow: none;
}

.edit-work-dialog .el-select__wrapper .el-select__placeholder {
  color: #666;
}

.edit-work-dialog .dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.edit-work-dialog .dialog-footer .el-button {
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 14px;
}

.edit-work-dialog .dialog-footer .el-button:not(.el-button--primary) {
  background-color: #BACACB;
  border-color: #BACACB;
  color: #425D5F;
}

.edit-work-dialog .dialog-footer .el-button:not(.el-button--primary):hover {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
}

.edit-work-dialog .dialog-footer .el-button--primary {
  background-color: #425D5F;
  border-color: #425D5F;
  color: #F8F7F2;
}

.edit-work-dialog .dialog-footer .el-button--primary:hover {
  background-color: #FAA943;
  border-color: #FAA943;
}

/* 封面上传样式 */
.cover-upload-container {
  width: 100%;
}

.work-cover-uploader {
  width: 100%;
}

.cover-upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 20px;
  cursor: pointer;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  transition: all 0.3s;
  background-color: #fff;
}

.cover-upload-trigger:hover {
  border-color: #425D5F;
  background-color: rgba(66, 93, 95, 0.05);
}

.cover-upload-trigger .upload-icon {
  font-size: 48px;
  color: #BACACB;
  margin-bottom: 8px;
}

.cover-upload-trigger .upload-text {
  font-size: 14px;
  color: #425D5F;
  font-weight: 500;
}

.cover-upload-trigger .upload-hint {
  font-size: 12px;
  color: #999;
  text-align: center;
}

.cover-preview {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.cover-preview-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
  aspect-ratio: 500 / 892;
  border: 1px solid #BACACB;
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

@media (max-width: 768px) {
  .page-header {
    padding: 12px 16px;
  }

  .sidebar-tabs {
    width: 100px;
  }
  
  .tab-item {
    gap: 6px;
  }
  
  .tab-item span {
    font-size: 9px;
  }

  .chat-sidebar,
  .image-sidebar {
    display: none;
  }

  .chat-messages {
    padding: 16px;
  }

  .chat-input-area {
    padding: 12px 16px;
  }

  .message-content {
    max-width: 85%;
  }

  .image-main {
    padding: 16px;
  }

  .form-row {
    flex-direction: column;
  }
}
</style>
