package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliAdvertisement;

/**
 * 广告管理Mapper接口
 *
 */
public interface CiliAdvertisementMapper {

    /**
     * 查询广告管理
     *
     * @param id 广告管理主键
     * @return 广告管理
     */
    public CiliAdvertisement selectCiliAdvertisementById(Long id);

    /**
     * 查询广告管理列表
     *
     * @param ciliAdvertisement 广告管理
     * @return 广告管理集合
     */
    public List<CiliAdvertisement> selectCiliAdvertisementList(CiliAdvertisement ciliAdvertisement);

    /**
     * 新增广告管理
     *
     * @param ciliAdvertisement 广告管理
     * @return 结果
     */
    public int insertCiliAdvertisement(CiliAdvertisement ciliAdvertisement);

    /**
     * 修改广告管理
     *
     * @param ciliAdvertisement 广告管理
     * @return 结果
     */
    public int updateCiliAdvertisement(CiliAdvertisement ciliAdvertisement);

    /**
     * 批量删除广告管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliAdvertisementByIds(Long[] ids);

    /**
     * 删除广告管理信息
     *
     * @param id 广告管理主键
     * @return 结果
     */
    public int deleteCiliAdvertisementById(Long id);
}
