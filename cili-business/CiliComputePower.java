package com.ruoyi.system.domain;

import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 用户算力对象 cili_compute_power
 *
 */
public class CiliComputePower extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /** ID */
    private Long id;

    /** 用户ID */
    private Long userId;

    /** 当前余额 */
    private BigDecimal balance;

    /** 累计充值 */
    private BigDecimal totalRecharged;

    /** 累计使用 */
    private BigDecimal totalUsed;

    /** 更新时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date updatedAt;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createdAt;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public BigDecimal getBalance() {
        return balance;
    }

    public void setBalance(BigDecimal balance) {
        this.balance = balance;
    }

    public BigDecimal getTotalRecharged() {
        return totalRecharged;
    }

    public void setTotalRecharged(BigDecimal totalRecharged) {
        this.totalRecharged = totalRecharged;
    }

    public BigDecimal getTotalUsed() {
        return totalUsed;
    }

    public void setTotalUsed(BigDecimal totalUsed) {
        this.totalUsed = totalUsed;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    /**
     * 检查余额是否足够
     */
    public boolean hasEnoughBalance(BigDecimal amount) {
        return this.balance != null && this.balance.compareTo(amount) >= 0;
    }

    @Override
    public String toString() {
        return "CiliComputePower{" +
                "id=" + id +
                ", userId=" + userId +
                ", balance=" + balance +
                ", totalRecharged=" + totalRecharged +
                ", totalUsed=" + totalUsed +
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
