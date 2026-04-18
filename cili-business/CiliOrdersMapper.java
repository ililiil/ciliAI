package com.ruoyi.system.mapper;

import java.util.List;
import com.ruoyi.system.domain.CiliOrders;

/**
 * 订单管理Mapper接口
 *
 */
public interface CiliOrdersMapper {

    /**
     * 查询订单管理
     *
     * @param id 订单管理主键
     * @return 订单管理
     */
    public CiliOrders selectCiliOrdersById(Long id);

    /**
     * 查询订单管理列表
     *
     * @param ciliOrders 订单管理
     * @return 订单管理集合
     */
    public List<CiliOrders> selectCiliOrdersList(CiliOrders ciliOrders);

    /**
     * 新增订单管理
     *
     * @param ciliOrders 订单管理
     * @return 结果
     */
    public int insertCiliOrders(CiliOrders ciliOrders);

    /**
     * 修改订单管理
     *
     * @param ciliOrders 订单管理
     * @return 结果
     */
    public int updateCiliOrders(CiliOrders ciliOrders);

    /**
     * 批量删除订单管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteCiliOrdersByIds(Long[] ids);

    /**
     * 删除订单管理信息
     *
     * @param id 订单管理主键
     * @return 结果
     */
    public int deleteCiliOrdersById(Long id);
}
