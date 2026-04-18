package com.ruoyi.system.service;

import java.util.List;
import java.util.Map;
import com.ruoyi.system.domain.CiliInviteCode;

/**
 * 邀请码Service接口
 *
 */
public interface ICiliInviteCodeService {

    /**
     * 查询邀请码
     *
     * @param id ID
     * @return 邀请码
     */
    public CiliInviteCode selectCiliInviteCodeById(Long id);

    /**
     * 根据邀请码查询
     *
     * @param code 邀请码
     * @return 邀请码
     */
    public CiliInviteCode selectCiliInviteCodeByCode(String code);

    /**
     * 查询邀请码列表
     *
     * @param ciliInviteCode 邀请码
     * @return 邀请码集合
     */
    public List<CiliInviteCode> selectCiliInviteCodeList(CiliInviteCode ciliInviteCode);

    /**
     * 新增邀请码
     *
     * @param ciliInviteCode 邀请码
     * @return 结果
     */
    public int insertCiliInviteCode(CiliInviteCode ciliInviteCode);

    /**
     * 修改邀请码
     *
     * @param ciliInviteCode 邀请码
     * @return 结果
     */
    public int updateCiliInviteCode(CiliInviteCode ciliInviteCode);

    /**
     * 删除邀请码
     *
     * @param id ID
     * @return 结果
     */
    public int deleteCiliInviteCodeById(Long id);

    /**
     * 批量删除邀请码
     *
     * @param ids 需要删除的ID
     * @return 结果
     */
    public int deleteCiliInviteCodeByIds(Long[] ids);

    /**
     * 使用邀请码
     *
     * @param code 邀请码
     * @param userId 用户ID
     * @return 结果
     */
    public Map<String, Object> useInviteCode(String code, Long userId);

    /**
     * 批量生成邀请码
     *
     * @param count 数量
     * @param createdBy 创建者ID
     * @param expiresAt 过期时间
     * @param maxUses 最大使用次数
     * @param batchNo 批次号
     * @return 生成的邀请码列表
     */
    public List<String> batchGenerateInviteCodes(int count, Long createdBy,
                                                  String expiresAt, int maxUses, String batchNo);
}
