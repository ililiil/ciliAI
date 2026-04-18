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
import com.ruoyi.system.domain.CiliInviteCode;
import com.ruoyi.system.service.ICiliInviteCodeService;

/**
 * 邀请码管理Controller
 *
 */
@RestController
@RequestMapping("/system/invitecode")
public class CiliInviteCodeController extends BaseController {

    @Autowired
    private ICiliInviteCodeService ciliInviteCodeService;

    /**
     * 查询邀请码列表
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliInviteCode ciliInviteCode) {
        startPage();
        List<CiliInviteCode> list = ciliInviteCodeService.selectCiliInviteCodeList(ciliInviteCode);
        return getDataTable(list);
    }

    /**
     * 导出邀请码列表
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:export')")
    @Log(title = "邀请码", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliInviteCode ciliInviteCode) {
        List<CiliInviteCode> list = ciliInviteCodeService.selectCiliInviteCodeList(ciliInviteCode);
        ExcelUtil<CiliInviteCode> util = new ExcelUtil<CiliInviteCode>(CiliInviteCode.class);
        util.exportExcel(response, list, "邀请码数据");
    }

    /**
     * 获取邀请码详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliInviteCodeService.selectCiliInviteCodeById(id));
    }

    /**
     * 新增邀请码
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:add')")
    @Log(title = "邀请码", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliInviteCode ciliInviteCode) {
        return toAjax(ciliInviteCodeService.insertCiliInviteCode(ciliInviteCode));
    }

    /**
     * 修改邀请码
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:edit')")
    @Log(title = "邀请码", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliInviteCode ciliInviteCode) {
        return toAjax(ciliInviteCodeService.updateCiliInviteCode(ciliInviteCode));
    }

    /**
     * 删除邀请码
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:remove')")
    @Log(title = "邀请码", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliInviteCodeService.deleteCiliInviteCodeByIds(ids));
    }

    /**
     * 验证邀请码（用户端使用）
     */
    @PostMapping("/validate")
    public AjaxResult validate(@RequestParam String code, @RequestParam Long userId) {
        Map<String, Object> result = ciliInviteCodeService.useInviteCode(code, userId);
        if ((boolean) result.get("success")) {
            return success(result);
        } else {
            return error((String) result.get("message"));
        }
    }

    /**
     * 批量生成邀请码
     */
    @PreAuthorize("@ss.hasPermi('cili:invitecode:add')")
    @Log(title = "批量生成邀请码", businessType = BusinessType.INSERT)
    @PostMapping("/batchGenerate")
    public AjaxResult batchGenerate(
            @RequestParam int count,
            @RequestParam String expiresAt,
            @RequestParam(defaultValue = "1") int maxUses,
            @RequestParam(required = false) String batchNo) {
        if (StringUtils.isEmpty(batchNo)) {
            batchNo = "BATCH" + System.currentTimeMillis();
        }
        List<String> codes = ciliInviteCodeService.batchGenerateInviteCodes(
            count, getUserId(), expiresAt, maxUses, batchNo);
        return success(codes);
    }

    // 导入 StringUtils
    private static final org.springframework.util.StringUtils StringUtils =
        new org.springframework.util.StringUtils() {};
}
