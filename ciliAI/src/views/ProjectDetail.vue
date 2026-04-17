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
          :class="['tab-item', { active: activeModule === 'edit' }]"
          @click="activeModule = 'edit'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 19l7-7 3 3-7 7-3-3z"/>
            <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
            <path d="M2 2l7.586 7.586"/>
            <circle cx="11" cy="11" r="2"/>
          </svg>
          <span>AI重绘</span>
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
                    :action="''"
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
                  <div v-if="editingImageIndex === index" class="edit-overlay-fullscreen">
                    <div class="edit-canvas-wrapper-fullscreen">
                      <canvas
                        :ref="el => { if (el) editCanvasInstance = el }"
                        class="edit-mask-canvas-fullscreen"
                        @mousedown="startEditDrawing"
                        @mousemove="editDrawing"
                        @mouseup="stopEditDrawing"
                        @mouseleave="stopEditDrawing"
                        @touchstart.prevent="startEditDrawingTouch"
                        @touchmove.prevent="editDrawingTouch"
                        @touchend="stopEditDrawing"
                      ></canvas>
                      <img :src="image.url" class="edit-base-image-fullscreen" />
                    </div>
                    
                    <!-- 浮动工具栏 -->
                    <div class="edit-controls-floating">
                      <div class="edit-toolbar-floating">
                        <button
                          :class="{ active: editingTool === 'brush' }"
                          @click="editingTool = 'brush'"
                        >
                          画笔
                        </button>
                        <button
                          :class="{ active: editingTool === 'eraser' }"
                          @click="editingTool = 'eraser'"
                        >
                          橡皮擦
                        </button>
                        <button @click="clearEditMask">
                          清空
                        </button>
                        <!-- 画笔大小调整 -->
                        <div class="brush-size-control">
                          <span class="brush-size-label">画笔大小:</span>
                          <input
                            type="range"
                            min="20"
                            max="200"
                            v-model.number="brushSettings.size"
                            class="brush-size-slider"
                          />
                          <span class="brush-size-value">{{ brushSettings.size }}px</span>
                        </div>
                      </div>
                      <div class="edit-prompt-input-floating">
                        <input
                          v-model="editPrompt"
                          type="text"
                          placeholder="请输入提示词，描述要生成的内容..."
                          class="prompt-input"
                          @keyup.enter="applyEdit(image, index)"
                        />
                      </div>
                      <div class="edit-action-bar-floating">
                        <button @click="cancelEdit" class="cancel-btn">
                          取消
                        </button>
                        <button @click="applyEdit(image, index)" :disabled="isApplyingEdit" class="confirm-btn">
                          {{ isApplyingEdit ? '处理中...' : '确认重绘' }}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div v-else class="result-content">
                    <img :src="image.url" :alt="image.prompt" @click="previewImage(image.url)" style="cursor: pointer;" />
                    <div class="result-actions">
                      <button class="action-btn" @click="startEdit(image, index)" title="局部重绘">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                          <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                          <path d="M2 2l7.586 7.586"/>
                          <circle cx="11" cy="11" r="2"/>
                        </svg>
                      </button>
                      <button class="action-btn" @click="downloadImage(image.url)" title="下载">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                          <polyline points="7 10 12 15 17 10"/>
                          <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                      </button>
                      <button class="action-btn" @click="previewImage(image.url)" title="预览">
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

        <!-- 重绘历史模块 -->
        <div v-else-if="activeModule === 'edit'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>重绘历史</h3>
              <button class="new-chat-btn" @click="loadEditHistory">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                刷新
              </button>
            </div>
            <div class="image-history-list">
              <div 
                v-if="editHistory.length === 0"
                class="empty-history"
              >
                <p>暂无重绘记录</p>
                <p class="empty-hint">点击图片上的编辑按钮开始重绘</p>
              </div>
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
            <div class="edit-history-intro">
              <h3 class="section-title">重绘历史</h3>
              <div class="intro-content">
                <p>查看您所有的重绘记录</p>
                <ul>
                  <li>✅ 展示重绘时的输入提示词</li>
                  <li>✅ 点击记录可查看大图</li>
                  <li>✅ 所有记录永久保存</li>
                </ul>
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
                    :action="''"
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
                    :action="''"
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
                    <div class="editor-toolbar">
                      <div class="tool-group">
                        <button
                          :class="['tool-btn', { active: editingTool === 'brush' }]"
                          @click="editingTool = 'brush'"
                          title="画笔工具"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                            <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                            <path d="M2 2l7.586 7.586"/>
                            <circle cx="11" cy="11" r="2"/>
                          </svg>
                          <span>画笔</span>
                        </button>
                        <button
                          :class="['tool-btn', { active: editingTool === 'eraser' }]"
                          @click="editingTool = 'eraser'"
                          title="橡皮擦"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 20H7L3 16c-.8-.8-.8-2 0-2.8L14.2 2a2 2 0 0 1 2.8 0L21 6a2 2 0 0 1 0 2.8L9 20"/>
                            <path d="M6.5 13.5L12.5 7.5"/>
                          </svg>
                          <span>橡皮擦</span>
                        </button>
                      </div>

                      <div class="tool-group brush-settings" v-if="editingTool === 'brush'">
                        <div class="setting-item">
                          <label>大小</label>
                          <el-slider
                            v-model="brushSettings.size"
                            :min="5"
                            :max="100"
                            :step="5"
                            show-stops
                            :marks="brushSizeMarks"
                            @change="updateBrushPreview"
                          />
                          <span class="value-label">{{ brushSettings.size }}px</span>
                        </div>
                        <div class="setting-item">
                          <label>硬度</label>
                          <el-slider
                            v-model="brushSettings.hardness"
                            :min="0"
                            :max="100"
                            :step="10"
                            :marks="brushHardnessMarks"
                          />
                          <span class="value-label">{{ brushSettings.hardness }}%</span>
                        </div>
                        <div class="setting-item">
                          <label>透明度</label>
                          <el-slider
                            v-model="brushSettings.opacity"
                            :min="10"
                            :max="100"
                            :step="10"
                            :marks="brushOpacityMarks"
                          />
                          <span class="value-label">{{ brushSettings.opacity }}%</span>
                        </div>
                        <div class="brush-preview">
                          <div
                            class="preview-dot"
                            :style="{
                              width: (brushSettings.size / 10) + 'px',
                              height: (brushSettings.size / 10) + 'px',
                              opacity: brushSettings.opacity / 100,
                              background: getBrushGradient()
                            }"
                          ></div>
                        </div>
                      </div>

                      <div class="tool-group">
                        <button
                          class="tool-btn"
                          @click="undoEdit"
                          :disabled="editHistoryStack.length === 0"
                          title="撤销"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 7v6h6"/>
                            <path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/>
                          </svg>
                          <span>撤销</span>
                        </button>
                        <button
                          class="tool-btn"
                          @click="redoEdit"
                          :disabled="editRedoStack.length === 0"
                          title="重做"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 7v6h-6"/>
                            <path d="M3 17a9 9 0 0 1 9-9 9 9 0 0 1 6 2.3l3 2.7"/>
                          </svg>
                          <span>重做</span>
                        </button>
                        <button
                          class="tool-btn clear-btn"
                          @click="clearMask"
                          title="清空"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 6h18"/>
                            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                          </svg>
                          <span>清空</span>
                        </button>
                      </div>
                    </div>

                    <div class="canvas-wrapper">
                      <div class="canvas-container" @wheel="handleCanvasZoom">
                        <div class="canvas-scroll-area" :style="{ transform: `scale(${canvasZoom})` }">
                          <canvas
                            ref="editCanvas"
                            @mousedown="startDrawing"
                            @mousemove="draw"
                            @mouseup="stopDrawing"
                            @mouseleave="stopDrawing"
                            @touchstart="startDrawingTouch"
                            @touchmove="drawTouch"
                            @touchend="stopDrawing"
                            :style="{ cursor: getCanvasCursor() }"
                          ></canvas>
                          <img ref="editImageRef" :src="editParams.image" class="editor-image" />
                        </div>
                      </div>
                      <div class="canvas-zoom-controls">
                        <button @click="zoomIn" title="放大">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <path d="M21 21l-4.35-4.35"/>
                            <path d="M11 8v6"/>
                            <path d="M8 11h6"/>
                          </svg>
                        </button>
                        <span class="zoom-level">{{ Math.round(canvasZoom * 100) }}%</span>
                        <button @click="zoomOut" title="缩小">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <path d="M21 21l-4.35-4.35"/>
                            <path d="M8 11h6"/>
                          </svg>
                        </button>
                        <button @click="resetZoom" title="重置">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 21l-6-6"/>
                            <path d="M3 12a9 9 0 1 0 9-9"/>
                          </svg>
                        </button>
                      </div>
                    </div>

                    <div class="mask-preview">
                      <h4>涂抹预览</h4>
                      <canvas ref="maskPreviewCanvas" class="preview-canvas"></canvas>
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

    <el-dialog
      v-model="showImagePreview"
      width="80%"
      class="image-preview-dialog"
    >
      <img :src="previewImageUrl" class="preview-image" />
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { generateImage as volcGenerateImage, editImage as volcEditImage, extendImage as volcExtendImage } from '../utils/volcengine.js'

const route = useRoute()
const router = useRouter()
const updateComputingPower = inject('updateComputingPower')

const currentInviteCode = ref(localStorage.getItem('inviteCode') || '')

const accessKeyId = import.meta.env.VITE_VOLC_AK_1 || import.meta.env.VITE_VOLC_AK || ''
const secretAccessKey = import.meta.env.VITE_VOLC_SK_1 || import.meta.env.VITE_VOLC_SK || ''

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
    const response = await fetch('/api/power/deduct', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        invite_code: inviteCode,
        project_id: project.value.id,
        message: inputMessage.value.trim()
      })
    })
    
    const result = await response.json()
    
    if (result.status !== 'success') {
      return { 
        success: false, 
        message: result.message || '算力不足',
        remainingPower: result.power_current || 0
      }
    }
    
    const remainingPower = result.remaining_power
    if (updateComputingPower) {
      updateComputingPower(remainingPower)
    }
    
    return { 
      success: true, 
      remainingPower: remainingPower,
      powerCost: result.power_cost
    }
  } catch (error) {
    console.error('算力扣减失败:', error)
    return { success: false, message: '算力扣减失败，请重试', remainingPower: 0 }
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
const editCanvas = ref(null)
const canvasContext = ref(null)
const editCanvasInstance = ref(null)

// 简化的画笔设置
const brushSettings = reactive({
  size: 80  // 增大默认画笔大小，从30改为80，更适合涂抹大区域
})

// 蒙版编辑状态
const editingImageIndex = ref(null)
const editingImageUrl = ref('')
const editPrompt = ref('')
const isApplyingEdit = ref(false)
let lastX = 0
let lastY = 0
const editMaskData = ref('')

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

const getImageUrl = (imageUrl) => {
  if (!imageUrl) {
    return ''
  }
  
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl
  }
  
  if (imageUrl.startsWith('data:image')) {
    return imageUrl
  }
  
  if (imageUrl.startsWith('/')) {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
    return `${apiBaseUrl}${imageUrl}`
  }
  
  return imageUrl
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
  
  await loadHistoryData()
}

const loadHistoryData = async () => {
  await loadChatSessions()
  await loadImageHistory()
}

const loadChatSessions = async () => {
  const inviteCode = localStorage.getItem('inviteCode') || ''
  if (!inviteCode) {
    chatList.value = []
    return
  }
  
  try {
    const response = await fetch(`/api/chat/sessions?invite_code=${encodeURIComponent(inviteCode)}&project_id=${project.value.id}`)
    const result = await response.json()
    
    if (result.status === 'success') {
      chatList.value = result.sessions.map(session => ({
        id: session.id.toString(),
        title: session.title,
        conversationId: session.conversation_id || '',
        selectedPeople: session.selected_people || 'script',
        updateTime: new Date(session.update_time).toLocaleString('zh-CN'),
        messages: []
      }))
      
      if (chatList.value.length > 0) {
        await selectChat(chatList.value[0].id)
      } else {
        await createNewChat()
      }
    }
  } catch (error) {
    console.error('加载聊天会话失败:', error)
    chatList.value = []
  }
}

const loadImageHistory = async () => {
  const inviteCode = localStorage.getItem('inviteCode') || ''
  if (!inviteCode) {
    imageHistory.value = []
    return
  }
  
  try {
    const response = await fetch(`/api/records?invite_code=${encodeURIComponent(inviteCode)}&project_id=${project.value.id}&type=generate`)
    const result = await response.json()
    
    if (result.status === 'success') {
      imageHistory.value = result.records.map(record => ({
        id: record.id.toString(),
        prompt: record.prompt || '',
        imageUrl: getImageUrl(record.image_url) || '',
        createTime: new Date(record.create_time).toLocaleString('zh-CN'),
        params: JSON.parse(record.params || '{}')
      }))
    }
  } catch (error) {
    console.error('加载图片历史失败:', error)
    imageHistory.value = []
  }
}

const loadEditHistory = async () => {
  const inviteCode = localStorage.getItem('inviteCode') || ''
  if (!inviteCode) {
    editHistory.value = []
    return
  }
  
  try {
    const response = await fetch(`/api/records?invite_code=${encodeURIComponent(inviteCode)}&project_id=${project.value.id}&type=inpaint`)
    const result = await response.json()
    
    if (result.status === 'success') {
      editHistory.value = result.records.map(record => ({
        id: record.id.toString(),
        prompt: record.prompt || '无提示词',
        imageUrl: getImageUrl(record.image_url) || '',
        createTime: new Date(record.create_time).toLocaleString('zh-CN'),
        params: JSON.parse(record.params || '{}')
      }))
    }
  } catch (error) {
    console.error('加载重绘历史失败:', error)
    editHistory.value = []
  }
}

const goBack = () => {
  router.push('/works')
}

const saveProject = async () => {
  isSaving.value = true
  try {
    const inviteCode = localStorage.getItem('inviteCode') || ''
    
    if (!inviteCode) {
      ElMessage.warning('请先登录')
      isSaving.value = false
      return
    }
    
    const response = await fetch(`/api/projects/${project.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        invite_code: inviteCode,
        title: project.value.title,
        description: project.value.description,
        cover_image: project.value.coverImage
      })
    })
    
    const result = await response.json()
    
    if (result.status === 'success') {
      ElMessage.success('项目保存成功')
    } else {
      ElMessage.error(result.message || '保存失败，请重试')
    }
  } catch (error) {
    console.error('保存项目失败:', error)
    ElMessage.error('保存失败，请检查网络连接')
  } finally {
    isSaving.value = false
  }
}

const createNewChat = async () => {
  const inviteCode = localStorage.getItem('inviteCode') || ''
  
  const newChat = {
    id: Date.now().toString(),
    title: '新对话',
    updateTime: new Date().toLocaleString('zh-CN'),
    messages: [],
    conversationId: '',
    selectedPeople: selectedPeople.value
  }
  
  try {
    if (inviteCode && project.value.id) {
      const response = await fetch('/api/chat/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          invite_code: inviteCode,
          project_id: project.value.id,
          title: '新对话',
          selected_people: selectedPeople.value
        })
      })
      
      const result = await response.json()
      if (result.status === 'success') {
        newChat.id = result.session_id.toString()
        console.log('✅ 会话已保存到后端，session_id:', result.session_id)
      }
    }
  } catch (error) {
    console.error('保存会话失败:', error)
  }
  
  chatList.value.unshift(newChat)
  currentChatId.value = newChat.id
  inputMessage.value = ''
  localStorage.removeItem('currentConversationId')
  console.log('✅ 新对话已创建，conversationId 已清空')
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
    
    try {
      const inviteCode = localStorage.getItem('inviteCode') || ''
      await fetch(`/api/chat/sessions/${chatId}?invite_code=${encodeURIComponent(inviteCode)}`, {
        method: 'DELETE'
      })
      console.log('✅ 会话已从后端删除')
    } catch (error) {
      console.error('删除后端会话失败:', error)
    }
    
    const index = chatList.value.findIndex(c => c.id === chatId)
    if (index > -1) {
      chatList.value.splice(index, 1)
      if (currentChatId.value === chatId) {
        if (chatList.value.length > 0) {
          await selectChat(chatList.value[0].id)
        } else {
          await createNewChat()
        }
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
    console.log('========== 发送消息开始 ==========')
    console.log('当前会话ID:', chat.conversationId || '(新会话)')
    
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
          localStorage.setItem('currentConversationId', receivedConversationId)
          console.log('✅ 会话ID已更新并保存:', receivedConversationId)
        }
        
        scrollToBottom()
      }
    )
    
    if (conversationId && chat) {
      chat.conversationId = conversationId
      localStorage.setItem('currentConversationId', conversationId)
      console.log('✅ 最终会话ID已保存:', conversationId)
      
      try {
        const inviteCode = localStorage.getItem('inviteCode') || ''
        await fetch(`/api/chat/sessions/${chat.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            invite_code: inviteCode,
            title: message.slice(0, 20) + (message.length > 20 ? '...' : ''),
            conversation_id: conversationId
          })
        })
        console.log('✅ 会话信息已更新到后端')
      } catch (error) {
        console.error('更新会话信息失败:', error)
      }
    }
    
    const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
    if (msgIndex > -1) {
      chat.messages[msgIndex].status = 'success'
    }
    
    console.log('✅ 消息发送成功！')
    console.log('==================================')
  } catch (error) {
    if (error.name === 'AbortError' || error.message.includes('请求超时') || error.message.includes('abort')) {
      console.warn('⚠️ 请求被中止（非错误，可能是重复请求或超时）:', error.message)
      isSending.value = false
      return
    }
    
    console.error('❌ 发送消息失败:', error)
    console.error('错误信息:', error.message)
    
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
    } else if (error.message.includes('超时') || error.message.includes('timeout')) {
      const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
      if (msgIndex > -1) {
        const currentContent = chat.messages[msgIndex].content
        if (currentContent && currentContent.length > 0) {
          chat.messages[msgIndex].content = currentContent + '\n\n[⚠️ 请求超时，AI可能还在思考中...]'
          chat.messages[msgIndex].status = 'success'
        } else {
          chat.messages[msgIndex].content = '[⚠️ 请求超时] ' + error.message
          chat.messages[msgIndex].status = 'error'
        }
      }
      ElMessage.warning('请求超时：' + error.message)
    } else {
      const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
      if (msgIndex > -1) {
        const currentContent = chat.messages[msgIndex].content
        if (currentContent && currentContent.length > 0) {
          chat.messages[msgIndex].content = currentContent + '\n\n[⚠️ 连接中断，如需继续请重试]'
          chat.messages[msgIndex].status = 'success'
        } else {
          chat.messages[msgIndex].content = '抱歉，API 连接失败: ' + error.message
          chat.messages[msgIndex].status = 'error'
        }
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
  const timeout = setTimeout(() => {
    console.warn('⏰ 请求超时触发（180秒），中止请求')
    controller.abort()
  }, 180000)

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
    files: [],
    pre_deducted: true
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
    
  } catch (error) {
    clearTimeout(timeout)
    
    if (error.name === 'AbortError') {
      console.warn('⚠️ Dify API 请求被中止（非错误，可能是重复请求或超时）')
      throw error
    }
    
    console.error('❌ Dify API 网络错误:', error)
    console.error('错误类型:', error.name)
    console.error('错误消息:', error.message)
    console.error('错误堆栈:', error.stack)
    
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
        console.error('❌ 读取流数据时出错:', error)
        if (result.length > 0) {
          console.log('⚠️ 部分响应已接收，返回已获取的内容')
          return { answer: result, conversationId: newConversationId }
        }
        throw error
      }

      const { done, value } = readResult
      if (done) {
        isCompleted = true
        break
      }

      try {
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
                console.log('✅ 收到新会话ID:', newConversationId)
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
      } catch (decodeError) {
        console.error('❌ 解码数据块时出错:', decodeError)
        continue
      }
    }
  } catch (error) {
    cleanup()
    console.error('❌ 流式处理出错:', error)
    
    if (error.name === 'AbortError' || error.message.includes('abort')) {
      if (result.length > 0) {
        console.log('⚠️ 请求被中止但已有部分响应，返回已获取的内容')
        return { answer: result, conversationId: newConversationId }
      }
      throw new Error('请求被中止，请检查网络连接后重试。')
    }
    throw error
  }

  cleanup()
  console.log('✅ 流式响应处理完成')
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
    
    await loadImageHistory()
    
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

// 蒙版编辑功能

let isDrawing = false

const startEdit = (image, index) => {
  console.log('开始编辑图片:', image, index)
  editingImageIndex.value = index
  editingImageUrl.value = image.url
  
  // 进入编辑模式时自动增大画笔大小，方便涂抹大区域
  brushSettings.size = 80
  
  nextTick(() => {
    setTimeout(() => {
      initEditCanvas(image.url)
    }, 100)
  })
}

const initEditCanvas = (imageUrl) => {
  if (!editCanvasInstance.value) return

  const canvas = editCanvasInstance.value
  const img = new Image()
  img.crossOrigin = 'anonymous'

  img.onload = () => {
    canvas.width = img.width
    canvas.height = img.height
    canvasContext.value = canvas.getContext('2d')

    // 清空蒙版
    clearEditMask()
  }

  img.src = imageUrl
}

const startEditDrawing = (e) => {
  isDrawing = true
  const canvas = editCanvasInstance.value
  if (!canvas) return

  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  lastX = (e.clientX - rect.left) * scaleX
  lastY = (e.clientY - rect.top) * scaleY

  editDrawing(e)
}

const editDrawing = (e) => {
  if (!isDrawing || !canvasContext.value || !editCanvasInstance.value) return

  const canvas = editCanvasInstance.value
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  const x = (e.clientX - rect.left) * scaleX
  const y = (e.clientY - rect.top) * scaleY

  const ctx = canvasContext.value

  ctx.lineWidth = brushSettings.size
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'

  if (editingTool.value === 'brush') {
    ctx.globalCompositeOperation = 'source-over'
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
  } else {
    ctx.globalCompositeOperation = 'destination-out'
    ctx.fillStyle = 'black'
  }

  // 绘制线条
  ctx.beginPath()
  ctx.moveTo(lastX, lastY)
  ctx.lineTo(x, y)
  ctx.stroke()

  // 绘制圆点
  ctx.beginPath()
  ctx.arc(x, y, brushSettings.size / 2, 0, Math.PI * 2)
  ctx.fill()

  lastX = x
  lastY = y
}

const stopEditDrawing = () => {
  isDrawing = false
  updateEditMask()
}

const startEditDrawingTouch = (e) => {
  const touch = e.touches[0]
  const mouseEvent = new MouseEvent('mousedown', {
    clientX: touch.clientX,
    clientY: touch.clientY
  })
  startEditDrawing(mouseEvent)
}

const editDrawingTouch = (e) => {
  const touch = e.touches[0]
  const mouseEvent = new MouseEvent('mousemove', {
    clientX: touch.clientX,
    clientY: touch.clientY
  })
  editDrawing(mouseEvent)
}

const clearEditMask = () => {
  if (!canvasContext.value || !editCanvasInstance.value) return

  const canvas = editCanvasInstance.value
  const ctx = canvasContext.value

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  updateEditMask()
}

const updateEditMask = () => {
  if (!editCanvasInstance.value) return

  editMaskData.value = editCanvasInstance.value.toDataURL('image/png')
}

const applyEdit = async (image, index) => {
  if (!editMaskData.value) {
    ElMessage.warning('请先绘制要修改的区域')
    return
  }

  if (!editPrompt.value.trim()) {
    ElMessage.warning('请输入提示词')
    return
  }

  isApplyingEdit.value = true

  try {
    console.log('开始局部重绘...')
    console.log('图片URL:', editingImageUrl.value)
    console.log('Mask长度:', editMaskData.value.length)
    console.log('提示词:', editPrompt.value.trim())

    // 将图片URL转换为base64
    const imageBase64 = await urlToBase64(editingImageUrl.value)
    console.log('图片Base64长度:', imageBase64.length)

    const params = {
      image: imageBase64,
      mask: editMaskData.value,
      prompt: editPrompt.value.trim()
    }

    console.log('调用局部重绘API...')
    const submitResponse = await volcEditImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    console.log('API响应:', submitResponse)

    if (submitResponse.code === 10000 && submitResponse.data.images.length > 0) {
      // 用返回的图片替换原图
      generatedImages.value[index] = {
        url: submitResponse.data.images[0].url,
        prompt: image.prompt
      }

      ElMessage.success('局部重绘成功')
      cancelEdit()
    } else {
      throw new Error(submitResponse.message || '处理失败')
    }
  } catch (error) {
    console.error('局部重绘失败:', error)
    ElMessage.error(`局部重绘失败: ${error.message}`)
  } finally {
    isApplyingEdit.value = false
  }
}

const cancelEdit = () => {
  editingImageIndex.value = null
  editingImageUrl.value = ''
  editPrompt.value = ''
  editMaskData.value = ''
  if (editCanvasInstance.value) {
    clearEditMask()
  }
}

// 辅助函数：将URL转换为base64
const urlToBase64 = (url) => {
  return new Promise((resolve, reject) => {
    // 如果已经是base64格式，直接返回
    if (url.startsWith('data:')) {
      resolve(url)
      return
    }

    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      try {
        const canvas = document.createElement('canvas')
        canvas.width = img.width
        canvas.height = img.height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0)
        const dataURL = canvas.toDataURL('image/png')
        console.log('Base64转换成功，长度:', dataURL.length)
        resolve(dataURL)
      } catch (error) {
        console.error('Base64转换失败:', error)
        reject(error)
      }
    }
    img.onerror = (error) => {
      console.error('图片加载失败:', error)
      reject(error)
    }
    img.src = url
  })
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

const loadImageForEdit = (image) => {
  console.log('加载图片到编辑区:', image)

  // 切换到编辑模块
  activeModule.value = 'edit'

  // 设置编辑参数
  editParams.image = image.url
  editParams.prompt = image.prompt || ''
  editParams.mask = ''

  // 清空文件列表
  editFileList.value = []
  maskFileList.value = []

  // 清空编辑历史图片
  editedImages.value = []

  // 初始化画布
  nextTick(() => {
    setTimeout(() => {
      initCanvas()
      ElMessage.success('已加载到编辑区，请在涂抹区域绘制要修改的部分')
    }, 300)
  })
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
  loadEditHistory()
  
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
  text-align: left;
}

.project-time {
  font-size: 12px;
  color: #425D5F;
  margin-top: 4px;
  text-align: left;
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
  color: #425D5F;
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
  color: #425D5F;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 11px;
  color: #425D5F;
  margin-top: 4px;
}

.empty-history {
  text-align: center;
  padding: 40px 16px;
  color: #425D5F;
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
  background-color: #fff;
  border: 1px solid #BACACB;
  border-radius: 12px;
  padding: 20px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 500;
  color: #425D5F;
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
  color: #666;
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
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
  box-shadow: none;
}

.params-form :deep(.el-input__inner),
.params-form :deep(.el-textarea__inner) {
  color: #425D5F;
}

.params-form :deep(.el-input__inner::placeholder),
.params-form :deep(.el-textarea__inner::placeholder) {
  color: #999;
}

.params-form :deep(.el-upload-list__item) {
  background-color: #F8F7F2;
  border: 1px solid #BACACB;
}

.params-form :deep(.el-upload-list__item-name) {
  color: #425D5F;
}

.params-form :deep(.el-upload__tip) {
  color: #999;
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
  border: 1px solid #BACACB;
  border-radius: 8px;
  overflow: hidden;
  background-color: #F8F7F2;
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
  border: 1px dashed #BACACB;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  color: #425D5F;
  margin-top: 8px;
  background-color: #F8F7F2;
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
  color: #425D5F;
}

.empty-result .empty-icon {
  margin-bottom: 16px;
  color: #425D5F;
}

.empty-result .hint {
  font-size: 13px;
  margin-top: 8px;
  color: #425D5F;
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

/* 蒙版编辑功能 */
.edit-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.edit-canvas-wrapper {
  position: relative;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-mask-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 100%;
  max-height: 100%;
  cursor: crosshair;
  z-index: 2;
}

.edit-base-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  pointer-events: none;
}

.edit-controls {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid #e8e8e8;
}

.edit-toolbar {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #e8e8e8;
}

.edit-toolbar button {
  padding: 8px 20px;
  font-size: 14px;
  color: #333;
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.edit-toolbar button:hover:not(:disabled) {
  background: #e6e6e6;
  border-color: #1890ff;
  color: #1890ff;
}

.edit-toolbar button:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.edit-toolbar button.active {
  background: #1890ff;
  border-color: #1890ff;
  color: white;
}

.edit-prompt-input {
  padding: 12px 16px;
  border-bottom: 1px solid #e8e8e8;
}

.prompt-input {
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  outline: none;
  transition: all 0.2s;
}

.prompt-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.prompt-input::placeholder {
  color: #bfbfbf;
}

.edit-action-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 12px 16px;
}

.edit-action-bar button {
  padding: 8px 20px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.edit-action-bar .cancel-btn {
  background: #f5f5f5;
  color: #425D5F;
  border: 1px solid #d9d9d9;
}

.edit-action-bar .cancel-btn:hover {
  background: #e6e6e6;
}

.edit-action-bar .confirm-btn {
  background: #1890ff;
  color: white;
}

.edit-action-bar .confirm-btn:hover:not(:disabled) {
  background: #40a9ff;
  transform: translateY(-1px);
}

.edit-action-bar .confirm-btn:disabled {
  background: #999;
}

/* 全屏编辑模式 */
.edit-overlay-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
}

.edit-canvas-wrapper-fullscreen {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 60px 20px 160px 20px;  /* 为工具栏留出空间 */
}

.edit-mask-canvas-fullscreen {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: calc(100% - 40px);
  max-height: calc(100vh - 220px);  /* 减去工具栏高度 */
  cursor: crosshair;
  z-index: 2;
}

.edit-base-image-fullscreen {
  max-width: calc(100% - 40px);
  max-height: calc(100vh - 220px);  /* 减去工具栏高度 */
  object-fit: contain;
  pointer-events: none;
}

/* 浮动工具栏 */
.edit-controls-floating {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 -2px 20px rgba(0, 0, 0, 0.1);
  z-index: 10000;
}

.edit-toolbar-floating {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #e8e8e8;
}

.edit-toolbar-floating button {
  padding: 10px 28px;
  font-size: 15px;
  color: #333;
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.edit-toolbar-floating button:hover:not(:disabled) {
  background: #e6e6e6;
  border-color: #1890ff;
  color: #1890ff;
}

.edit-toolbar-floating button:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.edit-toolbar-floating button.active {
  background: #1890ff;
  border-color: #1890ff;
  color: white;
}

/* 画笔大小控制 */
.brush-size-control {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 20px;
  padding-left: 20px;
  border-left: 1px solid #e8e8e8;
}

.brush-size-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.brush-size-slider {
  width: 150px;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: linear-gradient(to right, #1890ff, #40a9ff);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.brush-size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #fff;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}

.brush-size-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 3px 8px rgba(24, 144, 255, 0.4);
}

.brush-size-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #fff;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.brush-size-value {
  font-size: 14px;
  color: #1890ff;
  font-weight: 600;
  min-width: 50px;
  text-align: center;
}

.edit-prompt-input-floating {
  padding: 16px 20px;
  border-bottom: 1px solid #e8e8e8;
}

.edit-prompt-input-floating .prompt-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  outline: none;
  transition: all 0.2s;
}

.edit-prompt-input-floating .prompt-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.edit-prompt-input-floating .prompt-input::placeholder {
  color: #bfbfbf;
}

.edit-action-bar-floating {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
}

.edit-action-bar-floating button {
  padding: 10px 28px;
  font-size: 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.edit-action-bar-floating .cancel-btn {
  background: #f5f5f5;
  color: #425D5F;
  border: 1px solid #d9d9d9;
}

.edit-action-bar-floating .cancel-btn:hover {
  background: #e6e6e6;
}

.edit-action-bar-floating .confirm-btn {
  background: #1890ff;
  color: white;
}

.edit-action-bar-floating .confirm-btn:hover:not(:disabled) {
  background: #40a9ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.edit-action-bar-floating .confirm-btn:disabled {
  background: #999;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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

/* 编辑工具栏样式 */
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

/* 重绘历史模块样式 */
.edit-history-intro {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.edit-history-intro .section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.edit-history-intro .intro-content {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.edit-history-intro .intro-content p {
  font-size: 16px;
  color: #666;
  margin-bottom: 16px;
}

.edit-history-intro .intro-content ul {
  list-style: none;
  padding: 0;
}

.edit-history-intro .intro-content li {
  font-size: 14px;
  color: #555;
  padding: 8px 0;
  padding-left: 24px;
  position: relative;
}

.edit-history-intro .intro-content li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #1890ff;
  font-weight: bold;
  font-size: 18px;
}

.empty-history {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-history p {
  font-size: 14px;
  margin-bottom: 8px;
}

.empty-history .empty-hint {
  font-size: 12px;
  color: #bbb;
}
</style>
