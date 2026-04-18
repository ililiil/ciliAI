package com.ruoyi.system.service;

import java.util.List;
import com.ruoyi.system.domain.CiliWorks;

/**
 * 作品管理Service接口
 *
 */
public interface ICiliWorksService {

    /**
     * 查询作品管理
     *
     * @param id 作品管理主键
     * @return 作品管理
     */
    public CiliWorks selectCiliWorksById(Long id);

    /**
     * 查询作品管理列表
     *
     * @param ciliWorks 作品管理
     * @return 作品管理集合
     */
    public List<CiliWorks> selectCiliWorksList(CiliWorks ciliWorks);

    /**
     * 新增作品管理
     *
     * @param ciliWorks 作品管理
     * @return 结果
     */
    public int insertCiliWorks(CiliWorks ciliWorks);

    /**
     * 修改作品管理
     *
     * @param ciliWorks 作品管理
     * @return 结果
     */
    public int updateCiliWorks(CiliWorks ciliWorks);

    /**
     * 批量删除作品管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliWorksByIds(Long[] ids);

    /**
     * 删除作品管理信息
     *
     * @param id 作品管理主键
     * @return 结果
     */
    public int deleteCiliWorksById(Long id);

    /**
     * 审核作品
     *
     * @param id 作品ID
     * @param status 审核状态
     * @param reason 审核理由
     * @return 结果
     */
    public int auditWorks(Long id, String status, String reason);

    /**
     * 设置作品置顶
     *
     * @param id 作品ID
     * @param isTop 是否置顶
     * @return 结果
     */
    public int setWorksTop(Long id, Boolean isTop);
}
