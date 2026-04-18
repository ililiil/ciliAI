package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliInviteCode;
import org.apache.ibatis.annotations.Param;

/**
 * 邀请码Mapper接口
 *
 */
public interface CiliInviteCodeMapper {

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
     * @param id 用户ID
     * @param userId 使用者ID
     * @return 结果
     */
    public int useInviteCode(@Param("id") Long id, @Param("userId") Long userId);
}
