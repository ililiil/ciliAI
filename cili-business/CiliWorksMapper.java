package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliWorks;

/**
 * 作品管理Mapper接口
 *
 */
public interface CiliWorksMapper {

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
}
