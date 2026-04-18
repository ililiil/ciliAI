package com.ruoyi.system.service.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.system.mapper.CiliGenerationRecordMapper;
import com.ruoyi.system.domain.CiliGenerationRecord;
import com.ruoyi.system.service.ICiliGenerationRecordService;

/**
 * AI生成记录Service业务层处理
 *
 */
@Service
public class CiliGenerationRecordServiceImpl implements ICiliGenerationRecordService {

    @Autowired
    private CiliGenerationRecordMapper ciliGenerationRecordMapper;

    /**
     * 查询AI生成记录
     *
     * @param id AI生成记录主键
     * @return AI生成记录
     */
    @Override
    public CiliGenerationRecord selectCiliGenerationRecordById(Long id) {
        return ciliGenerationRecordMapper.selectCiliGenerationRecordById(id);
    }

    /**
     * 查询AI生成记录列表
     *
     * @param ciliGenerationRecord AI生成记录
     * @return AI生成记录
     */
    @Override
    public List<CiliGenerationRecord> selectCiliGenerationRecordList(CiliGenerationRecord ciliGenerationRecord) {
        return ciliGenerationRecordMapper.selectCiliGenerationRecordList(ciliGenerationRecord);
    }

    /**
     * 取消生成任务
     *
     * @param id 任务ID
     * @return 结果
     */
    @Override
    @Transactional
    public Map<String, Object> cancelGeneration(Long id) {
        Map<String, Object> result = new HashMap<>();
        CiliGenerationRecord record = ciliGenerationRecordMapper.selectCiliGenerationRecordById(id);
        if (record == null) {
            result.put("success", false);
            result.put("message", "任务不存在");
            return result;
        }
        if (!"processing".equals(record.getStatus())) {
            result.put("success", false);
            result.put("message", "只有进行中的任务才能取消");
            return result;
        }
        record.setStatus("cancelled");
        ciliGenerationRecordMapper.updateCiliGenerationRecord(record);
        result.put("success", true);
        result.put("message", "任务已取消");
        return result;
    }

    /**
     * 重试生成任务
     *
     * @param id 任务ID
     * @return 结果
     */
    @Override
    @Transactional
    public Map<String, Object> retryGeneration(Long id) {
        Map<String, Object> result = new HashMap<>();
        CiliGenerationRecord record = ciliGenerationRecordMapper.selectCiliGenerationRecordById(id);
        if (record == null) {
            result.put("success", false);
            result.put("message", "任务不存在");
            return result;
        }
        if (!"failed".equals(record.getStatus()) && !"cancelled".equals(record.getStatus())) {
            result.put("success", false);
            result.put("message", "只能重试失败或已取消的任务");
            return result;
        }
        // TODO: 调用火山引擎API重新生成
        record.setStatus("processing");
        ciliGenerationRecordMapper.updateCiliGenerationRecord(record);
        result.put("success", true);
        result.put("message", "任务已重新提交");
        return result;
    }

    /**
     * 获取生成统计
     *
     * @return 统计数据
     */
    @Override
    public Map<String, Object> getGenerationStatistics() {
        Map<String, Object> statistics = new HashMap<>();
        // TODO: 从数据库查询统计数据
        statistics.put("totalCount", 0);
        statistics.put("successCount", 0);
        statistics.put("failedCount", 0);
        statistics.put("processingCount", 0);
        return statistics;
    }
}
