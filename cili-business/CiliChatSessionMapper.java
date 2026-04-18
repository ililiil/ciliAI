package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliChatSession;

/**
 * 聊天会话Mapper接口
 *
 */
public interface CiliChatSessionMapper {

    /**
     * 查询聊天会话
     *
     * @param id 聊天会话主键
     * @return 聊天会话
     */
    public CiliChatSession selectCiliChatSessionById(Long id);

    /**
     * 查询聊天会话列表
     *
     * @param ciliChatSession 聊天会话
     * @return 聊天会话集合
     */
    public List<CiliChatSession> selectCiliChatSessionList(CiliChatSession ciliChatSession);

    /**
     * 新增聊天会话
     *
     * @param ciliChatSession 聊天会话
     * @return 结果
     */
    public int insertCiliChatSession(CiliChatSession ciliChatSession);

    /**
     * 修改聊天会话
     *
     * @param ciliChatSession 聊天会话
     * @return 结果
     */
    public int updateCiliChatSession(CiliChatSession ciliChatSession);

    /**
     * 批量删除聊天会话
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliChatSessionByIds(Long[] ids);

    /**
     * 删除聊天会话信息
     *
     * @param id 聊天会话主键
     * @return 结果
     */
    public int deleteCiliChatSessionById(Long id);
}
