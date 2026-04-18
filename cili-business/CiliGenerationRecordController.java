package com.ruoyi.web.controller.system;

import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.system.domain.CiliGenerationRecord;
import com.ruoyi.system.service.ICiliGenerationRecordService;

/**
 * AI生成记录Controller
 *
 */
@RestController
@RequestMapping("/system/generationrecord")
public class CiliGenerationRecordController extends BaseController {

    @Autowired
    private ICiliGenerationRecordService ciliGenerationRecordService;

    /**
     * 查询AI生成记录列表
     */
    @PreAuthorize("@ss.hasPermi('cili:generationrecord:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliGenerationRecord ciliGenerationRecord) {
        startPage();
        List<CiliGenerationRecord> list = ciliGenerationRecordService.selectCiliGenerationRecordList(ciliGenerationRecord);
        return getDataTable(list);
    }

    /**
     * 获取AI生成记录详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:generationrecord:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliGenerationRecordService.selectCiliGenerationRecordById(id));
    }

    /**
     * 取消生成任务
     */
    @PreAuthorize("@ss.hasPermi('cili:generationrecord:cancel')")
    @Log(title = "取消生成任务", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/cancel")
    public AjaxResult cancel(@PathVariable Long id) {
        Map<String, Object> result = ciliGenerationRecordService.cancelGeneration(id);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 重试生成任务
     */
    @PreAuthorize("@ss.hasPermi('cili:generationrecord:retry')")
    @Log(title = "重试生成任务", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/retry")
    public AjaxResult retry(@PathVariable Long id) {
        Map<String, Object> result = ciliGenerationRecordService.retryGeneration(id);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 获取生成统计
     */
    @PreAuthorize("@ss.hasPermi('cili:generationrecord:statistics')")
    @GetMapping("/statistics")
    public AjaxResult statistics() {
        return success(ciliGenerationRecordService.getGenerationStatistics());
    }
}
