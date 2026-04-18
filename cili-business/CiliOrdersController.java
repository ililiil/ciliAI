package com.ruoyi.web.controller.system;

import java.util.List;
import java.util.Map;
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
import com.ruoyi.system.domain.CiliOrders;
import com.ruoyi.system.service.ICiliOrdersService;

/**
 * 订单管理Controller
 *
 */
@RestController
@RequestMapping("/system/orders")
public class CiliOrdersController extends BaseController {

    @Autowired
    private ICiliOrdersService ciliOrdersService;

    /**
     * 查询订单列表
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliOrders ciliOrders) {
        startPage();
        List<CiliOrders> list = ciliOrdersService.selectCiliOrdersList(ciliOrders);
        return getDataTable(list);
    }

    /**
     * 导出订单列表
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:export')")
    @Log(title = "订单", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliOrders ciliOrders) {
        List<CiliOrders> list = ciliOrdersService.selectCiliOrdersList(ciliOrders);
        ExcelUtil<CiliOrders> util = new ExcelUtil<CiliOrders>(CiliOrders.class);
        util.exportExcel(response, list, "订单数据");
    }

    /**
     * 获取订单详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliOrdersService.selectCiliOrdersById(id));
    }

    /**
     * 新增订单
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:add')")
    @Log(title = "订单", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliOrders ciliOrders) {
        return toAjax(ciliOrdersService.insertCiliOrders(ciliOrders));
    }

    /**
     * 修改订单
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:edit')")
    @Log(title = "订单", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliOrders ciliOrders) {
        return toAjax(ciliOrdersService.updateCiliOrders(ciliOrders));
    }

    /**
     * 修改订单状态
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:status')")
    @Log(title = "订单状态", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/status")
    public AjaxResult updateStatus(@PathVariable Long id, @RequestParam String status) {
        return toAjax(ciliOrdersService.updateCiliOrdersStatus(id, status));
    }

    /**
     * 退款处理
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:refund')")
    @Log(title = "订单退款", businessType = BusinessType.UPDATE)
    @PutMapping("/{id}/refund")
    public AjaxResult refund(@PathVariable Long id, @RequestParam(required = false) String reason) {
        Map<String, Object> result = ciliOrdersService.refundOrder(id, reason);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 删除订单
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:remove')")
    @Log(title = "订单", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliOrdersService.deleteCiliOrdersByIds(ids));
    }

    /**
     * 获取订单统计
     */
    @PreAuthorize("@ss.hasPermi('cili:orders:statistics')")
    @GetMapping("/statistics")
    public AjaxResult statistics() {
        return success(ciliOrdersService.getOrderStatistics());
    }
}
