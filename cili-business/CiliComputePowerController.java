package com.ruoyi.web.controller.system;

import java.math.BigDecimal;
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
import com.ruoyi.system.domain.CiliComputePower;
import com.ruoyi.system.service.ICiliComputePowerService;

/**
 * 用户算力管理Controller
 *
 */
@RestController
@RequestMapping("/system/computepower")
public class CiliComputePowerController extends BaseController {

    @Autowired
    private ICiliComputePowerService ciliComputePowerService;

    /**
     * 查询用户算力列表
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliComputePower ciliComputePower) {
        startPage();
        List<CiliComputePower> list = ciliComputePowerService.selectCiliComputePowerList(ciliComputePower);
        return getDataTable(list);
    }

    /**
     * 导出用户算力列表
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:export')")
    @Log(title = "用户算力", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliComputePower ciliComputePower) {
        List<CiliComputePower> list = ciliComputePowerService.selectCiliComputePowerList(ciliComputePower);
        ExcelUtil<CiliComputePower> util = new ExcelUtil<CiliComputePower>(CiliComputePower.class);
        util.exportExcel(response, list, "用户算力数据");
    }

    /**
     * 获取用户算力详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliComputePowerService.selectCiliComputePowerById(id));
    }

    /**
     * 根据用户ID获取算力
     */
    @GetMapping("/user/{userId}")
    public AjaxResult getByUserId(@PathVariable("userId") Long userId) {
        return success(ciliComputePowerService.selectCiliComputePowerByUserId(userId));
    }

    /**
     * 新增用户算力
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:add')")
    @Log(title = "用户算力", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliComputePower ciliComputePower) {
        return toAjax(ciliComputePowerService.insertCiliComputePower(ciliComputePower));
    }

    /**
     * 修改用户算力
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:edit')")
    @Log(title = "用户算力", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliComputePower ciliComputePower) {
        return toAjax(ciliComputePowerService.updateCiliComputePower(ciliComputePower));
    }

    /**
     * 充值算力
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:recharge')")
    @Log(title = "算力充值", businessType = BusinessType.UPDATE)
    @PostMapping("/recharge/{userId}")
    public AjaxResult recharge(@PathVariable Long userId, @RequestParam BigDecimal amount) {
        Map<String, Object> result = ciliComputePowerService.rechargePower(userId, amount);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 消费算力
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:consume')")
    @Log(title = "算力消费", businessType = BusinessType.UPDATE)
    @PostMapping("/consume/{userId}")
    public AjaxResult consume(@PathVariable Long userId, @RequestParam BigDecimal amount) {
        Map<String, Object> result = ciliComputePowerService.consumePower(userId, amount);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 删除用户算力
     */
    @PreAuthorize("@ss.hasPermi('cili:computepower:remove')")
    @Log(title = "用户算力", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliComputePowerService.deleteCiliComputePowerByIds(ids));
    }
}
