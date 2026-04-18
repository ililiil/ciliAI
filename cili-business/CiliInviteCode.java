package com.ruoyi.system.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 邀请码对象 cili_invite_code
 *
 */
public class CiliInviteCode extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /** ID */
    private Long id;

    /** 邀请码 */
    private String code;

    /** 是否已使用（0-未使用 1-已使用） */
    private Integer used;

    /** 使用者用户ID */
    private Long usedBy;

    /** 使用时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date usedAt;

    /** 创建者ID */
    private Long createdBy;

    /** 过期时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date expiresAt;

    /** 最大使用次数 */
    private Integer maxUses;

    /** 已使用次数 */
    private Integer useCount;

    /** 状态（0-正常 1-禁用） */
    private String status;

    /** 批次号 */
    private String batchNo;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public Integer getUsed() {
        return used;
    }

    public void setUsed(Integer used) {
        this.used = used;
    }

    public Long getUsedBy() {
        return usedBy;
    }

    public void setUsedBy(Long usedBy) {
        this.usedBy = usedBy;
    }

    public Date getUsedAt() {
        return usedAt;
    }

    public void setUsedAt(Date usedAt) {
        this.usedAt = usedAt;
    }

    @Override
    public Long getCreatedBy() {
        return createdBy;
    }

    @Override
    public void setCreatedBy(Long createdBy) {
        this.createdBy = createdBy;
    }

    public Date getExpiresAt() {
        return expiresAt;
    }

    public void setExpiresAt(Date expiresAt) {
        this.expiresAt = expiresAt;
    }

    public Integer getMaxUses() {
        return maxUses;
    }

    public void setMaxUses(Integer maxUses) {
        this.maxUses = maxUses;
    }

    public Integer getUseCount() {
        return useCount;
    }

    public void setUseCount(Integer useCount) {
        this.useCount = useCount;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getBatchNo() {
        return batchNo;
    }

    public void setBatchNo(String batchNo) {
        this.batchNo = batchNo;
    }

    /**
     * 判断邀请码是否有效
     */
    public boolean isValid() {
        if ("1".equals(this.status)) {
            return false;
        }
        if (this.expiresAt != null && this.expiresAt.before(new Date())) {
            return false;
        }
        if (this.used != null && this.used >= this.maxUses) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "CiliInviteCode{" +
                "id=" + id +
                ", code='" + code + '\'' +
                ", used=" + used +
                ", usedBy=" + usedBy +
                ", expiresAt=" + expiresAt +
                ", maxUses=" + maxUses +
                ", useCount=" + useCount +
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
