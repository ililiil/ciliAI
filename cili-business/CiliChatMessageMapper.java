package com.ruoyi.system.mapper;

import java.util.List;
import java.util.Map;
import com.ruoyi.system.domain.CiliChatMessage;

/**
 * 聊天消息Mapper接口
 *
 */
public interface CiliChatMessageMapper {

    /**
     * 查询聊天消息
     *
     * @param id 聊天消息主键
     * @return 聊天消息
     */
    public CiliChatMessage selectCiliChatMessageById(Long id);

    /**
     * 查询聊天消息列表
     *
     * @param ciliChatMessage 聊天消息
     * @return 聊天消息集合
     */
    public List<CiliChatMessage> selectCiliChatMessageList(CiliChatMessage ciliChatMessage);

    /**
     * 新增聊天消息
     *
     * @param ciliChatMessage 聊天消息
     * @return 结果
     */
    public int insertCiliChatMessage(CiliChatMessage ciliChatMessage);

    /**
     * 修改聊天消息
     *
     * @param ciliChatMessage 聊天消息
     * @return 结果
     */
    public int updateCiliChatMessage(CiliChatMessage ciliChatMessage);

    /**
     * 批量删除聊天消息
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliChatMessageByIds(Long[] ids);

    /**
     * 删除聊天消息信息
     *
     * @param id 聊天消息主键
     * @return 结果
     */
    public int deleteCiliChatMessageById(Long id);

    /**
     * 查询会话消息列表
     *
     * @param sessionId 会话ID
     * @return 消息列表
     */
    public List<Map<String, Object>> selectMessagesBySessionId(Long sessionId);
}
