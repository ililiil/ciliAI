package com.ruoyi.system.service.impl;

import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.system.mapper.CiliWorksMapper;
import com.ruoyi.system.domain.CiliWorks;
import com.ruoyi.system.service.ICiliWorksService;

/**
 * 作品管理Service业务层处理
 *
 */
@Service
public class CiliWorksServiceImpl implements ICiliWorksService {

    @Autowired
    private CiliWorksMapper ciliWorksMapper;

    /**
     * 查询作品管理
     *
     * @param id 作品管理主键
     * @return 作品管理
     */
    @Override
    public CiliWorks selectCiliWorksById(Long id) {
        return ciliWorksMapper.selectCiliWorksById(id);
    }

    /**
     * 查询作品管理列表
     *
     * @param ciliWorks 作品管理
     * @return 作品管理
     */
    @Override
    public List<CiliWorks> selectCiliWorksList(CiliWorks ciliWorks) {
        return ciliWorksMapper.selectCiliWorksList(ciliWorks);
    }

    /**
     * 新增作品管理
     *
     * @param ciliWorks 作品管理
     * @return 结果
     */
    @Override
    public int insertCiliWorks(CiliWorks ciliWorks) {
        ciliWorks.setCreateTime(new Date());
        return ciliWorksMapper.insertCiliWorks(ciliWorks);
    }

    /**
     * 修改作品管理
     *
     * @param ciliWorks 作品管理
     * @return 结果
     */
    @Override
    public int updateCiliWorks(CiliWorks ciliWorks) {
        ciliWorks.setUpdateTime(new Date());
        return ciliWorksMapper.updateCiliWorks(ciliWorks);
    }

    /**
     * 批量删除作品管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    @Override
    public int deleteCiliWorksByIds(Long[] ids) {
        return ciliWorksMapper.deleteCiliWorksByIds(ids);
    }

    /**
     * 删除作品管理信息
     *
     * @param id 作品管理主键
     * @return 结果
     */
    @Override
    public int deleteCiliWorksById(Long id) {
        return ciliWorksMapper.deleteCiliWorksById(id);
    }

    /**
     * 审核作品
     *
     * @param id 作品ID
     * @param status 审核状态
     * @param reason 审核理由
     * @return 结果
     */
    @Override
    public int auditWorks(Long id, String status, String reason) {
        CiliWorks works = ciliWorksMapper.selectCiliWorksById(id);
        if (works == null) {
            throw new ServiceException("作品不存在");
        }
        works.setStatus(status);
        works.setAuditReason(reason);
        works.setAuditTime(new Date());
        works.setUpdateTime(new Date());
        return ciliWorksMapper.updateCiliWorks(works);
    }

    /**
     * 设置作品置顶
     *
     * @param id 作品ID
     * @param isTop 是否置顶
     * @return 结果
     */
    @Override
    public int setWorksTop(Long id, Boolean isTop) {
        CiliWorks works = ciliWorksMapper.selectCiliWorksById(id);
        if (works == null) {
            throw new ServiceException("作品不存在");
        }
        works.setIsTop(isTop ? 1 : 0);
        works.setUpdateTime(new Date());
        return ciliWorksMapper.updateCiliWorks(works);
    }
}
