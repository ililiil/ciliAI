package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliComputePower;
import org.apache.ibatis.annotations.Param;

/**
 * 用户算力Mapper接口
 *
 */
public interface CiliComputePowerMapper {

    /**
     * 查询用户算力
     *
     * @param id ID
     * @return 用户算力
     */
    public CiliComputePower selectCiliComputePowerById(Long id);

    /**
     * 根据用户ID查询
     *
     * @param userId 用户ID
     * @return 用户算力
     */
    public CiliComputePower selectCiliComputePowerByUserId(Long userId);

    /**
     * 查询用户算力列表
     *
     * @param ciliComputePower 用户算力
     * @return 用户算力集合
     */
    public List<CiliComputePower> selectCiliComputePowerList(CiliComputePower ciliComputePower);

    /**
     * 新增用户算力
     *
     * @param ciliComputePower 用户算力
     * @return 结果
     */
    public int insertCiliComputePower(CiliComputePower ciliComputePower);

    /**
     * 修改用户算力
     *
     * @param ciliComputePower 用户算力
     * @return 结果
     */
    public int updateCiliComputePower(CiliComputePower ciliComputePower);

    /**
     * 充值算力
     *
     * @param userId 用户ID
     * @param amount 充值金额
     * @return 结果
     */
    public int rechargePower(@Param("userId") Long userId, @Param("amount") java.math.BigDecimal amount);

    /**
     * 消费算力
     *
     * @param userId 用户ID
     * @param amount 消费金额
     * @return 结果
     */
    public int consumePower(@Param("userId") Long userId, @Param("amount") java.math.BigDecimal amount);

    /**
     * 删除用户算力
     *
     * @param id ID
     * @return 结果
     */
    public int deleteCiliComputePowerById(Long id);

    /**
     * 批量删除用户算力
     *
     * @param ids 需要删除的ID
     * @return 结果
     */
    public int deleteCiliComputePowerByIds(Long[] ids);
}
