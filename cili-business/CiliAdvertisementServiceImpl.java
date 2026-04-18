package com.ruoyi.system.service.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.system.mapper.CiliAdvertisementMapper;
import com.ruoyi.system.domain.CiliAdvertisement;
import com.ruoyi.system.service.ICiliAdvertisementService;

/**
 * 广告管理Service业务层处理
 *
 */
@Service
public class CiliAdvertisementServiceImpl implements ICiliAdvertisementService {

    @Autowired
    private CiliAdvertisementMapper ciliAdvertisementMapper;

    /**
     * 查询广告管理
     *
     * @param id 广告管理主键
     * @return 广告管理
     */
    @Override
    public CiliAdvertisement selectCiliAdvertisementById(Long id) {
        return ciliAdvertisementMapper.selectCiliAdvertisementById(id);
    }

    /**
     * 查询广告管理列表
     *
     * @param ciliAdvertisement 广告管理
     * @return 广告管理
     */
    @Override
    public List<CiliAdvertisement> selectCiliAdvertisementList(CiliAdvertisement ciliAdvertisement) {
        return ciliAdvertisementMapper.selectCiliAdvertisementList(ciliAdvertisement);
    }

    /**
     * 新增广告管理
     *
     * @param ciliAdvertisement 广告管理
     * @return 结果
     */
    @Override
    public int insertCiliAdvertisement(CiliAdvertisement ciliAdvertisement) {
        ciliAdvertisement.setCreateTime(new Date());
        return ciliAdvertisementMapper.insertCiliAdvertisement(ciliAdvertisement);
    }

    /**
     * 修改广告管理
     *
     * @param ciliAdvertisement 广告管理
     * @return 结果
     */
    @Override
    public int updateCiliAdvertisement(CiliAdvertisement ciliAdvertisement) {
        ciliAdvertisement.setUpdateTime(new Date());
        return ciliAdvertisementMapper.updateCiliAdvertisement(ciliAdvertisement);
    }

    /**
     * 修改广告状态
     *
     * @param id 广告ID
     * @param status 状态
     * @return 结果
     */
    @Override
    public int updateCiliAdvertisementStatus(Long id, String status) {
        CiliAdvertisement advertisement = ciliAdvertisementMapper.selectCiliAdvertisementById(id);
        if (advertisement == null) {
            throw new ServiceException("广告不存在");
        }
        advertisement.setStatus(status);
        advertisement.setUpdateTime(new Date());
        return ciliAdvertisementMapper.updateCiliAdvertisement(advertisement);
    }

    /**
     * 批量删除广告管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    @Override
    public int deleteCiliAdvertisementByIds(Long[] ids) {
        return ciliAdvertisementMapper.deleteCiliAdvertisementByIds(ids);
    }

    /**
     * 删除广告管理信息
     *
     * @param id 广告管理主键
     * @return 结果
     */
    @Override
    public int deleteCiliAdvertisementById(Long id) {
        return ciliAdvertisementMapper.deleteCiliAdvertisementById(id);
    }

    /**
     * 获取广告位置列表
     *
     * @return 广告位置列表
     */
    @Override
    public List<Map<String, Object>> getAdvertisementPositions() {
        List<Map<String, Object>> positions = new ArrayList<>();
        Map<String, Object> homeTop = new HashMap<>();
        homeTop.put("value", "home_top");
        homeTop.put("label", "首页顶部");
        positions.add(homeTop);

        Map<String, Object> homeBottom = new HashMap<>();
        homeBottom.put("value", "home_bottom");
        homeBottom.put("label", "首页底部");
        positions.add(homeBottom);

        Map<String, Object> sidebar = new HashMap<>();
        sidebar.put("value", "sidebar");
        sidebar.put("label", "侧边栏");
        positions.add(sidebar);

        Map<String, Object> popup = new HashMap<>();
        popup.put("value", "popup");
        popup.put("label", "弹窗");
        positions.add(popup);

        return positions;
    }
}
