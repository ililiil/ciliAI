package com.ruoyi.system.service;

import java.util.List;
import java.util.Map;
import com.ruoyi.system.domain.CiliGenerationRecord;

/**
 * AI生成记录Service接口
 *
 */
public interface ICiliGenerationRecordService {

    /**
     * 查询AI生成记录
     *
     * @param id AI生成记录主键
     * @return AI生成记录
     */
    public CiliGenerationRecord selectCiliGenerationRecordById(Long id);

    /**
     * 查询AI生成记录列表
     *
     * @param ciliGenerationRecord AI生成记录
     * @return AI生成记录集合
     */
    public List<CiliGenerationRecord> selectCiliGenerationRecordList(CiliGenerationRecord ciliGenerationRecord);

    /**
     * 取消生成任务
     *
     * @param id 任务ID
     * @return 结果
     */
    public Map<String, Object> cancelGeneration(Long id);

    /**
     * 重试生成任务
     *
     * @param id 任务ID
     * @return 结果
     */
    public Map<String, Object> retryGeneration(Long id);

    /**
     * 获取生成统计
     *
     * @return 统计数据
     */
    public Map<String, Object> getGenerationStatistics();
}
