package com.ruoyi.system.service;

import java.util.List;
import java.util.Map;
import com.ruoyi.system.domain.CiliProject;

/**
 * 项目管理Service接口
 *
 */
public interface ICiliProjectService {

    /**
     * 查询项目管理
     *
     * @param id 项目管理主键
     * @return 项目管理
     */
    public CiliProject selectCiliProjectById(Long id);

    /**
     * 查询项目管理列表
     *
     * @param ciliProject 项目管理
     * @return 项目管理集合
     */
    public List<CiliProject> selectCiliProjectList(CiliProject ciliProject);

    /**
     * 新增项目管理
     *
     * @param ciliProject 项目管理
     * @return 结果
     */
    public int insertCiliProject(CiliProject ciliProject);

    /**
     * 修改项目管理
     *
     * @param ciliProject 项目管理
     * @return 结果
     */
    public int updateCiliProject(CiliProject ciliProject);

    /**
     * 批量删除项目管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliProjectByIds(Long[] ids);

    /**
     * 删除项目管理信息
     *
     * @param id 项目管理主键
     * @return 结果
     */
    public int deleteCiliProjectById(Long id);

    /**
     * 获取项目统计
     *
     * @return 统计数据
     */
    public Map<String, Object> getProjectStatistics();
}
