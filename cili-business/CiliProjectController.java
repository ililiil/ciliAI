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
import com.ruoyi.system.domain.CiliProject;
import com.ruoyi.system.service.ICiliProjectService;

/**
 * 项目管理Controller
 *
 */
@RestController
@RequestMapping("/system/project")
public class CiliProjectController extends BaseController {

    @Autowired
    private ICiliProjectService ciliProjectService;

    /**
     * 查询项目列表
     */
    @PreAuthorize("@ss.hasPermi('cili:project:list')")
    @GetMapping("/list")
    public TableDataInfo list(CiliProject ciliProject) {
        startPage();
        List<CiliProject> list = ciliProjectService.selectCiliProjectList(ciliProject);
        return getDataTable(list);
    }

    /**
     * 导出项目列表
     */
    @PreAuthorize("@ss.hasPermi('cili:project:export')")
    @Log(title = "项目", businessType = BusinessType.EXPORT)
    public void export(HttpServletResponse response, CiliProject ciliProject) {
        List<CiliProject> list = ciliProjectService.selectCiliProjectList(ciliProject);
        ExcelUtil<CiliProject> util = new ExcelUtil<CiliProject>(CiliProject.class);
        util.exportExcel(response, list, "项目数据");
    }

    /**
     * 获取项目详细信息
     */
    @PreAuthorize("@ss.hasPermi('cili:project:query')")
    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id) {
        return success(ciliProjectService.selectCiliProjectById(id));
    }

    /**
     * 新增项目
     */
    @PreAuthorize("@ss.hasPermi('cili:project:add')")
    @Log(title = "项目", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody CiliProject ciliProject) {
        return toAjax(ciliProjectService.insertCiliProject(ciliProject));
    }

    /**
     * 修改项目
     */
    @PreAuthorize("@ss.hasPermi('cili:project:edit')")
    @Log(title = "项目", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@Validated @RequestBody CiliProject ciliProject) {
        return toAjax(ciliProjectService.updateCiliProject(ciliProject));
    }

    /**
     * 删除项目
     */
    @PreAuthorize("@ss.hasPermi('cili:project:remove')")
    @Log(title = "项目", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids) {
        return toAjax(ciliProjectService.deleteCiliProjectByIds(ids));
    }

    /**
     * 获取项目统计
     */
    @PreAuthorize("@ss.hasPermi('cili:project:statistics')")
    @GetMapping("/statistics")
    public AjaxResult statistics() {
        return success(ciliProjectService.getProjectStatistics());
    }
}
