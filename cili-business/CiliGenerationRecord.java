package com.ruoyi.system.domain;

import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * AI生成记录对象 cili_generation_record
 *
 */
public class CiliGenerationRecord extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /** ID */
    private Long id;

    /** 用户ID */
    private Long userId;

    /** 火山引擎任务ID */
    private String taskId;

    /** 任务类型 */
    private String taskType;

    /** 正向提示词 */
    private String prompt;

    /** 负向提示词 */
    private String negativePrompt;

    /** 模型版本 */
    private String modelVersion;

    /** 生成参数 */
    private String parameters;

    /** 结果URL */
    private String resultUrl;

    /** 状态 */
    private String status;

    /** 算力消耗 */
    private BigDecimal powerCost;

    /** 错误信息 */
    private String errorMessage;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createdAt;

    /** 完成时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date completedAt;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }

    public String getTaskId() { return taskId; }
    public void setTaskId(String taskId) { this.taskId = taskId; }

    public String getTaskType() { return taskType; }
    public void setTaskType(String taskType) { this.taskType = taskType; }

    public String getPrompt() { return prompt; }
    public void setPrompt(String prompt) { this.prompt = prompt; }

    public String getNegativePrompt() { return negativePrompt; }
    public void setNegativePrompt(String negativePrompt) { this.negativePrompt = negativePrompt; }

    public String getModelVersion() { return modelVersion; }
    public void setModelVersion(String modelVersion) { this.modelVersion = modelVersion; }

    public String getParameters() { return parameters; }
    public void setParameters(String parameters) { this.parameters = parameters; }

    public String getResultUrl() { return resultUrl; }
    public void setResultUrl(String resultUrl) { this.resultUrl = resultUrl; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public BigDecimal getPowerCost() { return powerCost; }
    public void setPowerCost(BigDecimal powerCost) { this.powerCost = powerCost; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getCompletedAt() { return completedAt; }
    public void setCompletedAt(Date completedAt) { this.completedAt = completedAt; }

    // 任务类型常量
    public static final String TYPE_TEXT2IMG = "text2img";
    public static final String TYPE_IMG2IMG = "img2img";
    public static final String TYPE_VIDEO = "video";

    // 状态常量
    public static final String STATUS_PENDING = "pending";
    public static final String STATUS_SUCCESS = "success";
    public static final String STATUS_FAILED = "failed";

    @Override
    public String toString() {
        return "CiliGenerationRecord{" +
                "id=" + id +
                ", taskId='" + taskId + '\'' +
                ", taskType='" + taskType + '\'' +
                ", status='" + status + '\'' +
                '}';
    }
}

    public String getDelFlag()
    {
        return delFlag;
    }

    public void setDelFlag(String delFlag)
    {
        this.delFlag = delFlag;
    }
