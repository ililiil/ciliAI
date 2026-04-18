package com.ruoyi.web.controller.system;

import java.util.List;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.system.domain.CiliWorks;
import com.ruoyi.system.service.ICiliWorksService;

/**
 * 作品管理Controller
 *
 */
@RestController
@RequestMapping("/system/works")
public class CiliWorksController extends BaseController {

    @Autowired
    private ICiliWorksService ciliWorksService;

    /**
     * 查询作品列表
     */
    @PreAuthorize("@ss.hasPermi('cili:works:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliWorks ciliWorks) {
        startPage();
        List<CiliWorks> list = ciliWorksService.selectCiliWorksList(ciliWorks);
        return getDataTable(list);
    }

    /**
     * 导出作品列表
     */
    @PreAuthorize("@ss.hasPermi('cili:works:export')")
    @Log(title = "作品", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliWorks ciliWorks) {
        List<CiliWorks> list = ciliWorksService.selectCiliWorksList(ciliWorks);
        ExcelUtil<CiliWorks> util = new ExcelUtil<CiliWorks>(CiliWorks.class);
        util.exportExcel(response, list, "作品数据");
    }

    /**
     * 获取作品详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:works:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliWorksService.selectCiliWorksById(id));
    }

    /**
     * 新增作品
     */
    @PreAuthorize("@ss.hasPermi('cili:works:add')")
    @Log(title = "作品", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliWorks ciliWorks) {
        return toAjax(ciliWorksService.insertCiliWorks(ciliWorks));
    }

    /**
     * 修改作品
     */
    @PreAuthorize("@ss.hasPermi('cili:works:edit')")
    @Log(title = "作品", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliWorks ciliWorks) {
        return toAjax(ciliWorksService.updateCiliWorks(ciliWorks));
    }

    /**
     * 删除作品
     */
    @PreAuthorize("@ss.hasPermi('cili:works:remove')")
    @Log(title = "作品", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliWorksService.deleteCiliWorksByIds(ids));
    }

    /**
     * 审核作品
     */
    @PreAuthorize("@ss.hasPermi('cili:works:audit')")
    @Log(title = "作品审核", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/audit")
    public AjaxResult audit(@PathVariable Long id, @RequestParam String status, @RequestParam(required = false) String reason) {
        return toAjax(ciliWorksService.auditWorks(id, status, reason));
    }

    /**
     * 设置作品置顶
     */
    @PreAuthorize("@ss.hasPermi('cili:works:top')")
    @Log(title = "作品置顶", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/top")
    public AjaxResult top(@PathVariable Long id, @RequestParam Boolean isTop) {
        return toAjax(ciliWorksService.setWorksTop(id, isTop));
    }
}
