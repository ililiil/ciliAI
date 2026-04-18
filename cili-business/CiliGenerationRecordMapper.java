package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliGenerationRecord;

/**
 * AI生成记录Mapper接口
 *
 */
public interface CiliGenerationRecordMapper {

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
     * 新增AI生成记录
     *
     * @param ciliGenerationRecord AI生成记录
     * @return 结果
     */
    public int insertCiliGenerationRecord(CiliGenerationRecord ciliGenerationRecord);

    /**
     * 修改AI生成记录
     *
     * @param ciliGenerationRecord AI生成记录
     * @return 结果
     */
    public int updateCiliGenerationRecord(CiliGenerationRecord ciliGenerationRecord);

    /**
     * 批量删除AI生成记录
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliGenerationRecordByIds(Long[] ids);

    /**
     * 删除AI生成记录信息
     *
     * @param id AI生成记录主键
     * @return 结果
     */
    public int deleteCiliGenerationRecordById(Long id);
}
