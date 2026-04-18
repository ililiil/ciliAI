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
import com.ruoyi.system.domain.CiliAdvertisement;
import com.ruoyi.system.service.ICiliAdvertisementService;

/**
 * 广告管理Controller
 *
 */
@RestController
@RequestMapping("/system/advertisement")
public class CiliAdvertisementController extends BaseController {

    @Autowired
    private ICiliAdvertisementService ciliAdvertisementService;

    /**
     * 查询广告列表
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliAdvertisement ciliAdvertisement) {
        startPage();
        List<CiliAdvertisement> list = ciliAdvertisementService.selectCiliAdvertisementList(ciliAdvertisement);
        return getDataTable(list);
    }

    /**
     * 导出广告列表
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:export')")
    @Log(title = "广告", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliAdvertisement ciliAdvertisement) {
        List<CiliAdvertisement> list = ciliAdvertisementService.selectCiliAdvertisementList(ciliAdvertisement);
        ExcelUtil<CiliAdvertisement> util = new ExcelUtil<CiliAdvertisement>(CiliAdvertisement.class);
        util.exportExcel(response, list, "广告数据");
    }

    /**
     * 获取广告详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliAdvertisementService.selectCiliAdvertisementById(id));
    }

    /**
     * 新增广告
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:add')")
    @Log(title = "广告", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliAdvertisement ciliAdvertisement) {
        return toAjax(ciliAdvertisementService.insertCiliAdvertisement(ciliAdvertisement));
    }

    /**
     * 修改广告
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:edit')")
    @Log(title = "广告", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliAdvertisement ciliAdvertisement) {
        return toAjax(ciliAdvertisementService.updateCiliAdvertisement(ciliAdvertisement));
    }

    /**
     * 修改广告状态
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:status')")
    @Log(title = "广告状态", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/status")
    public AjaxResult updateStatus(@PathVariable Long id, @RequestParam String status) {
        return toAjax(ciliAdvertisementService.updateCiliAdvertisementStatus(id, status));
    }

    /**
     * 删除广告
     */
    @PreAuthorize("@ss.hasPermi('cili:advertisement:remove')")
    @Log(title = "广告", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliAdvertisementService.deleteCiliAdvertisementByIds(ids));
    }

    /**
     * 获取广告位置列表
     */
    @GetMapping("/positions")
    public AjaxResult positions() {
        return success(ciliAdvertisementService.getAdvertisementPositions());
    }
}
