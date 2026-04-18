package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliProject;

/**
 * 项目管理Mapper接口
 *
 */
public interface CiliProjectMapper {

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
}
