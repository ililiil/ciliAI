package com.ruoyi.web.controller.system;

import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.system.domain.CiliChatSession;
import com.ruoyi.system.service.ICiliChatSessionService;

/**
 * 聊天会话Controller
 *
 */
@RestController
@RequestMapping("/system/chatsession")
public class CiliChatSessionController extends BaseController {

    @Autowired
    private ICiliChatSessionService ciliChatSessionService;

    /**
     * 查询聊天会话列表
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliChatSession ciliChatSession) {
        startPage();
        List<CiliChatSession> list = ciliChatSessionService.selectCiliChatSessionList(ciliChatSession);
        return getDataTable(list);
    }

    /**
     * 获取聊天会话详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliChatSessionService.selectCiliChatSessionById(id));
    }

    /**
     * 新增聊天会话
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:add')")
    @Log(title = "聊天会话", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliChatSession ciliChatSession) {
        return toAjax(ciliChatSessionService.insertCiliChatSession(ciliChatSession));
    }

    /**
     * 修改聊天会话
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:edit')")
    @Log(title = "聊天会话", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliChatSession ciliChatSession) {
        return toAjax(ciliChatSessionService.updateCiliChatSession(ciliChatSession));
    }

    /**
     * 归档聊天会话
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:archive')")
    @Log(title = "归档会话", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/archive")
    public AjaxResult archive(@PathVariable Long id) {
        Map<String, Object> result = ciliChatSessionService.archiveSession(id);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 删除聊天会话
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:remove')")
    @Log(title = "聊天会话", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliChatSessionService.deleteCiliChatSessionByIds(ids));
    }

    /**
     * 获取会话消息列表
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:messages')")
    @GetMapping("/{sessionId}/messages")
    public TableDataInfo messages(@PathVariable Long sessionId) {
        startPage();
        List<Map<String, Object>> messages = ciliChatSessionService.getSessionMessages(sessionId);
        return getDataTable(messages);
    }

    /**
     * 获取聊天统计
     */
    @PreAuthorize("@ss.hasPermi('cili:chatsession:statistics')")
    @GetMapping("/statistics")
    public AjaxResult statistics() {
        return success(ciliChatSessionService.getChatStatistics());
    }
}
